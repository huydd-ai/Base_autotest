"""Framework config. Override any value via env var of the same name (or .env)."""
import os

_HERE = os.path.dirname(__file__)


def _load_dotenv():
    """Minimal .env loader — no python-dotenv dep. Repo-root .env, existing env wins."""
    path = os.path.join(_HERE, "..", "..", ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


_load_dotenv()

# LDPlayer instance 0 over adb. Instance 1 -> 127.0.0.1:5557, etc.
DEVICE_URI = os.environ.get("DEVICE_URI", "Android://127.0.0.1:5037/127.0.0.1:5555")

# Package name of the Unity puzzle game under test.
APP_PACKAGE = os.environ.get("APP_PACKAGE", "com.example.puzzle")

# Template images for Airtest screenshot matching.
IMAGE_DIR = os.environ.get("IMAGE_DIR", os.path.join(_HERE, "..", "pages", "images"))

# Infra-drop evidence (jsonl + screenshots).
RESULTS_DIR = os.environ.get("RESULTS_DIR", os.path.join(_HERE, "..", "..", "results"))

# OCR match confidence floor (used by common.ocr). ponytail: only matters once OCR lands.
OCR_THRESHOLD = float(os.environ.get("OCR_THRESHOLD", "0.7"))

# Default waits (seconds).
DEFAULT_TIMEOUT = float(os.environ.get("DEFAULT_TIMEOUT", "10"))
