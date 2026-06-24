"""Single facade over airtest actions. Import this in the base AND in testcases.

Two things live here:
1. Every action you need (tap, swipe, wait_for, seen, key/text/home...) in ONE place,
   so a testcase only ever does `import actions as a`.
2. `is_infra_error()` — tells a device/adb drop apart from a real test failure,
   used by conftest to skip-not-fail when the emulator dies. Reusable in cases too.

Template-aware wrappers accept a bare image name ("btn_play") OR a raw airtest
target (a (x, y) pos or a Template). String -> images/<name>.png.
"""
import os

# Re-exported raw airtest actions — use directly with coords when no image fits.
from airtest.core.api import (
    Template, touch, swipe as _swipe, wait, exists, snapshot, sleep,
    keyevent, text, home, double_click,
)

import config


# ---- target resolution -------------------------------------------------------

def _resolve(target):
    """str -> images/<name>.png Template; pos tuple / Template passed through."""
    if isinstance(target, str):
        name = target if target.endswith(".png") else target + ".png"
        path = os.path.join(config.IMAGES_DIR, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"template image missing: {path}")
        return Template(path)
    return target


# ---- template-aware wrappers -------------------------------------------------

def wait_for(target, timeout=10):
    """Block until target appears; returns match position."""
    return wait(_resolve(target), timeout=timeout)


def tap(target, timeout=10):
    """Wait for an image target then tap; tap a raw pos immediately."""
    if isinstance(target, str):
        return touch(wait(_resolve(target), timeout=timeout))
    return touch(_resolve(target))


def swipe(start, end, **kw):
    """Swipe between two targets (image names, positions, or Templates)."""
    return _swipe(_resolve(start), _resolve(end), **kw)


def seen(target):
    """True if target is on screen right now (no wait)."""
    return bool(exists(_resolve(target)))


def shot(path):
    """Screenshot to an absolute path (airtest resolves relative against LOG_DIR)."""
    return snapshot(filename=path if path.endswith(".png") else path + ".png")


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

    ponytail: known airtest/adb classes first, then a message heuristic.
    Tighten _INFRA_HINTS if it ever misclassifies a real failure.
    """
    if isinstance(exc, (AssertionError,)):
        return False
    if _DEVICE_ERRORS and isinstance(exc, _DEVICE_ERRORS):
        return True
    msg = str(exc).lower()
    return any(h in msg for h in _INFRA_HINTS)
