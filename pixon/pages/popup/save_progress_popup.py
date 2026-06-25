"""Save-progress popup handler. ponytail: stub selectors."""
from pixon.common import actions as a


def handle_save_progress():
    if a.seen("popup_save_progress"):
        a.tap("popup_save_progress_dismiss")
        return True
    return False
