"""Remove ads page object. ponytail: stub."""
from .base_page import BasePage


class RemoveAdsPage(BasePage):
    name = "remove_ads"

    def is_open(self):
        return self.seen("remove_ads_title")
