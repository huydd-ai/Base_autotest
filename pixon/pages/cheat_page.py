"""Debug/cheat panel page object. ponytail: stub."""
from .base_page import BasePage


class CheatPage(BasePage):
    name = "cheat"

    def is_open(self):
        return self.seen("cheat_panel")
