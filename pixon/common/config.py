"""Framework config — per-game profiles. Pick a game with the GAME env var.

A game is a folder under games/<name>/ holding game.json:
    {"package": "...", "device_uri": "...", "images_dir": "images"}
Shared page objects + per-game image packs => same code drives any game.

Resolution order for each value: explicit env var > game.json > built-in default.
"""
import json
import os

_HERE = os.path.dirname(__file__)
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
GAMES_DIR = os.path.join(_ROOT, "games")


def _load_dotenv():
    """Minimal .env loader — no python-dotenv dep. Existing env wins."""
    path = os.path.join(_ROOT, ".env")
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

GAME = os.environ.get("GAME", "demo")
_GAME_DIR = os.path.join(GAMES_DIR, GAME)


def _load_profile():
    path = os.path.join(_GAME_DIR, "game.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


_PROFILE = _load_profile()


def _val(env_key, profile_key, default):
    return os.environ.get(env_key) or _PROFILE.get(profile_key) or default


DEVICE_URI = _val("DEVICE_URI", "device_uri",
                  "Android://127.0.0.1:5037/127.0.0.1:5555")
APP_PACKAGE = _val("APP_PACKAGE", "package", "com.example.puzzle")

# images_dir in game.json is relative to the game folder.
_images = os.environ.get("IMAGE_DIR") or os.path.join(
    _GAME_DIR, _PROFILE.get("images_dir", "images"))
IMAGE_DIR = _images

RESULTS_DIR = os.environ.get("RESULTS_DIR", os.path.join(_ROOT, "results"))
OCR_THRESHOLD = float(os.environ.get("OCR_THRESHOLD", "0.7"))
DEFAULT_TIMEOUT = float(os.environ.get("DEFAULT_TIMEOUT", "10"))


def require_game():
    """Call from device fixtures: fail loud if the selected game isn't set up."""
    if not _PROFILE:
        raise RuntimeError(
            f"game '{GAME}' not found under {GAMES_DIR}. "
            f"Run: python scripts/add_game.py {GAME} --package <pkg>")
    if not os.path.isdir(IMAGE_DIR):
        raise RuntimeError(f"images dir missing for game '{GAME}': {IMAGE_DIR}")
