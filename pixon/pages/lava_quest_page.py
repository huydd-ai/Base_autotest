"""Lava Quest event page object. ponytail: stub."""
from .base_page import BasePage


class LavaQuestPage(BasePage):
    name = "lava_quest"

    def is_open(self):
        return self.seen("lava_quest_title")
