"""BasePage — common interactions every page object inherits.

Pages depend DOWN on common.actions only. No flows/Test imports.
ponytail: thin. Add shared helpers (assert_visible, back, etc.) as pages need them.
"""
from pixon.common import actions as a
from pixon.common.log import get_logger


class BasePage:
    name = "base"

    def __init__(self):
        self.log = get_logger(f"page.{self.name}")

    # convenience pass-throughs so pages read cleanly
    def tap(self, target, timeout=None):
        return a.tap(target, timeout=timeout)

    def wait_for(self, target, timeout=None):
        return a.wait_for(target, timeout=timeout)

    def seen(self, target):
        return a.seen(target)
