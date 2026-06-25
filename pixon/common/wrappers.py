"""Compat facade for the tree's `wrappers.py` name.

Review delta: the old wrappers.py mixed actions + OCR + logging (low cohesion).
Those are now split into `actions`, `ocr`, `log`. This module just re-exports
them so existing `from pixon.common.wrappers import tap` style imports keep working.
Prefer importing the specific module in new code.
"""
from .actions import (  # noqa: F401
    tap, swipe, wait_for, seen, shot, is_infra_error,
    Template, touch, wait, exists, snapshot, sleep, keyevent, text, home, double_click,
)
from .ocr import read_text  # noqa: F401
from .log import get_logger  # noqa: F401
