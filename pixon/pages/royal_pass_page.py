"""Royal Pass battle-pass page object. ponytail: stub."""
from .base_page import BasePage


class RoyalPassPage(BasePage):
    name = "royal_pass"

    def is_open(self):
        return self.seen("royal_pass_title")
