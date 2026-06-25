"""The one Airtest facade — every action the project uses, in one import.

- Gesture actions (touch/tap, swipe, double_tap, pinch, key, type_text) are routed
  through `sync.input_lock` so watchdog threads and the test thread never interleave.
- Non-input airtest actions (screenshot, wait, exists, app lifecycle, shell, ...) are
  re-exported as-is.
- Template-aware wrappers accept a bare image name ("btn_play") OR a raw target
  (a (x, y) pos or a Template). String -> IMAGE_DIR/<name>.png.

Use `import pixon.common.actions as a` in pages and tests.
"""
import os

# Raw airtest API. Gesture ones get aliased and re-wrapped below; the rest pass through.
from airtest.core.api import (
    Template,
    touch as _touch, swipe as _swipe, double_click as _double_click,
    pinch as _pinch, keyevent as _keyevent, text as _text,
    # non-input — re-exported directly
    wait, exists, find_all, snapshot, sleep,
    home, wake, start_app, stop_app, clear_app, install, uninstall,
    shell, connect_device, device,
    assert_exists, assert_not_exists,
)

from . import config
from .sync import input_lock

__all__ = [
    # template-aware
    "tap", "swipe", "double_tap", "wait_for", "seen", "shot",
    # locked raw gestures
    "touch", "pinch", "key", "type_text",
    # passthrough
    "Template", "wait", "exists", "find_all", "snapshot", "sleep",
    "home", "wake", "start_app", "stop_app", "clear_app", "install", "uninstall",
    "shell", "connect_device", "device", "assert_exists", "assert_not_exists",
    # OCR (re-exported from common.ocr for one-stop import)
    "read_text", "text_present", "assert_text",
    # infra
    "is_infra_error",
]


# ---- target resolution -------------------------------------------------------

def _resolve(target):
    """str -> IMAGE_DIR/<name>.png Template; pos tuple / Template passed through."""
    if isinstance(target, str):
        name = target if target.endswith(".png") else target + ".png"
        path = os.path.join(config.IMAGE_DIR, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"template image missing: {path}")
        return Template(path)
    return target


def _pos(target, timeout):
    """Resolve an image target to a screen pos (waiting), or pass a raw pos through."""
    if isinstance(target, str):
        return wait(_resolve(target), timeout=timeout or config.DEFAULT_TIMEOUT)
    return _resolve(target)


# ---- template-aware gestures (locked) ----------------------------------------

def tap(target, timeout=None):
    with input_lock():
        return _touch(_pos(target, timeout))


def double_tap(target, timeout=None):
    with input_lock():
        return _double_click(_pos(target, timeout))


def swipe(start, end, **kw):
    with input_lock():
        return _swipe(_resolve(start), _resolve(end), **kw)


def wait_for(target, timeout=None):
    return wait(_resolve(target), timeout=timeout or config.DEFAULT_TIMEOUT)


def seen(target):
    return bool(exists(_resolve(target)))


def shot(path):
    return snapshot(filename=path if path.endswith(".png") else path + ".png")


# ---- raw gestures, locked ----------------------------------------------------

def touch(target, **kw):
    with input_lock():
        return _touch(_resolve(target), **kw)


def pinch(*args, **kw):
    with input_lock():
        return _pinch(*args, **kw)


def key(name):
    with input_lock():
        return _keyevent(name)


def type_text(content, **kw):
    with input_lock():
        return _text(content, **kw)


# ---- OCR (defined in common.ocr; surfaced here for one-stop import) ----------

from .ocr import read_text, text_present, assert_text  # noqa: E402,F401


# ---- infra vs code failure ---------------------------------------------------

def _infra_error_types():
    types = []
    for mod, name in (("airtest.core.error", "AdbError"),
                      ("airtest.core.error", "DeviceConnectionError"),
                      ("adbutils.errors", "AdbError")):
        try:
            types.append(getattr(__import__(mod, fromlist=[name]), name))
        except Exception:
            pass
    return tuple(types)


_DEVICE_ERRORS = _infra_error_types()
_INFRA_HINTS = ("adb", "device offline", "device not found", "closed",
                "not responding", "connection", "broken pipe")


def is_infra_error(exc):
    """True when exc looks like emulator/adb loss, not a test assertion.
    ponytail: known classes first, then a message heuristic; tighten hints if it misfires."""
    if isinstance(exc, AssertionError):
        return False
    if _DEVICE_ERRORS and isinstance(exc, _DEVICE_ERRORS):
        return True
    msg = str(exc).lower()
    return any(h in msg for h in _INFRA_HINTS)
