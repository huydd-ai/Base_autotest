"""OCR — isolated because the engine (paddle/tesseract) is a heavy, flaky dep.

ponytail: stub. Image templates cover most cases; OCR only for dynamic text
(scores, counters). Wire a real engine here when a test actually needs it —
don't pull the dependency before then.
"""
from . import config


def read_text(region=None, threshold=None):
    """Return recognized text in `region` (x1,y1,x2,y2) or full screen.
    threshold defaults to config.OCR_THRESHOLD."""
    raise NotImplementedError(
        "OCR engine not wired. Add paddleocr/pytesseract here when a test needs text."
    )
