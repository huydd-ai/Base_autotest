"""Player profile page object.

LEGACY (per reference tree). Review flag: don't enshrine legacy in a fresh tree.
Kept only to back Test/player-profile/. Port to current selectors or delete once
those 2 cases are migrated. ponytail: stub.
"""
from .base_page import BasePage


class PlayerProfilePage(BasePage):
    name = "player_profile"

    def is_open(self):
        return self.seen("profile_title")
