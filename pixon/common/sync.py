"""Concurrency seam between the test thread and the watchdog threads.

Both popup_watchdog and autoplay_watchdog drive the SAME device + minitouch
socket as the running test. Two guards:

- `input_lock()`  : one global lock every gesture writer acquires. Serializes taps.
- `suppress_watchdogs()` : context manager that pauses registered watchdogs so a
  watchdog can't dismiss the very dialog a test is asserting on.

ponytail: global input lock, not per-region. Fine — only one screen, one finger.
Upgrade to per-region only if multi-touch gestures ever run concurrently.
"""
import threading
from contextlib import contextmanager

_INPUT_LOCK = threading.RLock()
_REGISTRY = []          # watchdogs registered for global suppression
_REGISTRY_LOCK = threading.Lock()


@contextmanager
def input_lock():
    _INPUT_LOCK.acquire()
    try:
        yield
    finally:
        _INPUT_LOCK.release()


def register_watchdog(wd):
    """wd must expose .pause() and .resume()."""
    with _REGISTRY_LOCK:
        _REGISTRY.append(wd)


def unregister_watchdog(wd):
    with _REGISTRY_LOCK:
        if wd in _REGISTRY:
            _REGISTRY.remove(wd)


@contextmanager
def suppress_watchdogs():
    """Pause all registered watchdogs for the duration of the block."""
    with _REGISTRY_LOCK:
        active = list(_REGISTRY)
    for wd in active:
        wd.pause()
    try:
        yield
    finally:
        for wd in active:
            wd.resume()
