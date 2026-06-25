"""In-game page object. ponytail: stub."""
from .base_page import BasePage


class GamePage(BasePage):
    name = "game"

    def board_visible(self):
        return self.seen("board")
