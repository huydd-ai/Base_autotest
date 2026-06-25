"""Confirm dialog handler. Returns a callable usable as a watchdog handler.

The handler grabs sync.input_lock itself so it's safe to run from a watchdog thread.
ponytail: stub selectors.
"""
from pixon.common import actions as a


def handle_confirm():
    """Detect+accept a generic confirm dialog. True if it acted."""
    if a.seen("popup_confirm"):
        a.tap("popup_confirm_ok")   # tap takes the input lock
        return True
    return False
