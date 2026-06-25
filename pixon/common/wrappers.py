"""Compat facade for the tree's `wrappers.py` name.

Review delta: the old wrappers.py mixed actions + OCR + logging (low cohesion).
Now split into `actions` (which also surfaces OCR) and `log`. This re-exports the
full action surface so `from pixon.common.wrappers import tap` keeps working.
Prefer importing `pixon.common.actions as a` directly in new code.
"""
from .actions import *        # noqa: F401,F403  (full action + OCR surface)
from .log import get_logger   # noqa: F401
