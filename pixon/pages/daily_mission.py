"""Daily mission page object. ponytail: stub."""
from .base_page import BasePage


class DailyMissionPage(BasePage):
    name = "daily_mission"

    def is_open(self):
        return self.seen("daily_mission_title")
