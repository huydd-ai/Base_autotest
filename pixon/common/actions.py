"""Airtest action facade: tap/swipe/wait_for/seen/shot over templates, plus
the infra-vs-code classifier. Every input goes through `sync.input_lock` so
watchdog threads and the test thread never tear each other's gestures.

Template-aware wrappers accept a bare image name ("btn_play") OR a raw airtest
target (a (x, y) pos or a Template). String -> IMAGE_DIR/<name>.png.
"""
import os

from airtest.core.api import (
    Template, touch, swipe as _swipe, wait, exists, snapshot, sleep,
    keyevent, text, home, double_click,
)

from . import config
from .sync import input_lock


def _resolve(target):
    """str -> IMAGE_DIR/<name>.png Template; pos tuple / Template passed through."""
    if isinstance(target, str):
        name = target if target.endswith(".png") else target + ".png"
        path = os.path.join(config.IMAGE_DIR, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"template image missing: {path}")
        return Template(path)
    return target


def wait_for(target, timeout=None):
    return wait(_resolve(target), timeout=timeout or config.DEFAULT_TIMEOUT)


def tap(target, timeout=None):
    pos = wait(_resolve(target), timeout=timeout or config.DEFAULT_TIMEOUT) \
        if isinstance(target, str) else _resolve(target)
    with input_lock():
        return touch(pos)


def swipe(start, end, **kw):
    with input_lock():
        return _swipe(_resolve(start), _resolve(end), **kw)


def seen(target):
    return bool(exists(_resolve(target)))


def shot(path):
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
    ponytail: known classes first, then a message heuristic; tighten hints if it misfires."""
    if isinstance(exc, AssertionError):
        return False
    if _DEVICE_ERRORS and isinstance(exc, _DEVICE_ERRORS):
        return True
    msg = str(exc).lower()
    return any(h in msg for h in _INFRA_HINTS)
