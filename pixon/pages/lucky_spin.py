"""Lucky spin page object. ponytail: stub."""
from .base_page import BasePage


class LuckySpinPage(BasePage):
    name = "lucky_spin"

    def is_open(self):
        return self.seen("lucky_spin_title")
