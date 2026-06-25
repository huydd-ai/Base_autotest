"""Heart system page object. ponytail: stub."""
from .base_page import BasePage


class HeartSystemPage(BasePage):
    name = "heart_system"

    def is_open(self):
        return self.seen("heart_panel")
