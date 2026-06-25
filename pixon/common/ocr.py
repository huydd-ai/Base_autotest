"""OCR text checking via pytesseract (isolated — heavy/optional engine).

Install: `pip install -r requirements-ocr.txt` AND the tesseract binary
(https://github.com/UB-Mannheim/tesseract/wiki on Windows). Point at it with
env TESSERACT_CMD if it's not on PATH.

API:
    read_text(region)            -> recognized string (region = (x1,y1,x2,y2) or None)
    text_present(sub, region)    -> bool, normalized substring match
    assert_text(sub, region)     -> raises AssertionError if not present (a CODE failure)

ponytail: pytesseract only. Swap to easyocr/paddle here if accuracy needs it —
callers don't change.
"""
import os
import re

from . import config

_pytesseract = None
_Image = None


def _engine():
    """Lazy-load pytesseract + PIL; clear error if absent."""
    global _pytesseract, _Image
    if _pytesseract is None:
        try:
            import pytesseract
            from PIL import Image
        except ImportError as e:
            raise RuntimeError(
                "OCR needs pytesseract + Pillow: pip install -r requirements-ocr.txt"
            ) from e
        cmd = os.environ.get("TESSERACT_CMD")
        if cmd:
            pytesseract.pytesseract.tesseract_cmd = cmd
        _pytesseract, _Image = pytesseract, Image
    return _pytesseract, _Image


def _device_screen():
    from airtest.core.helper import G
    if G.DEVICE is None:
        raise RuntimeError("no device connected — OCR needs a live screen")
    return G.DEVICE.snapshot()          # BGR ndarray


def _crop(bgr, region):
    if region is None:
        return bgr
    x1, y1, x2, y2 = region
    return bgr[y1:y2, x1:x2]


def _normalize(s):
    """lowercase + collapse whitespace — for forgiving comparisons."""
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def _match(substring, text):
    return _normalize(substring) in _normalize(text)


def read_text(region=None, threshold=None, lang="eng"):
    """Recognize text in `region` (or full screen). Words below the confidence
    floor (threshold, default config.OCR_THRESHOLD) are dropped."""
    pt, Image = _engine()
    threshold = config.OCR_THRESHOLD if threshold is None else threshold
    bgr = _crop(_device_screen(), region)
    rgb = bgr[:, :, ::-1]               # BGR -> RGB
    data = pt.image_to_data(Image.fromarray(rgb), lang=lang,
                            output_type=pt.Output.DICT)
    words = [w for w, c in zip(data["text"], data["conf"])
             if w.strip() and float(c) >= threshold * 100]
    return " ".join(words)


def text_present(substring, region=None, threshold=None, lang="eng"):
    return _match(substring, read_text(region, threshold, lang))


def assert_text(substring, region=None, threshold=None, lang="eng"):
    found = read_text(region, threshold, lang)
    assert _match(substring, found), \
        f"expected text {substring!r} not found; OCR read: {found!r}"
