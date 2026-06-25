"""Settings page object. ponytail: stub."""
from .base_page import BasePage


class SettingPage(BasePage):
    name = "setting"

    def is_open(self):
        return self.seen("settings_title")
