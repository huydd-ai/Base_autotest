"""Home screen page object. ponytail: stub selectors — replace image names with real crops."""
from .base_page import BasePage


class HomePage(BasePage):
    name = "home"

    def is_open(self):
        return self.seen("main_menu")

    def play(self):
        self.tap("btn_play")
