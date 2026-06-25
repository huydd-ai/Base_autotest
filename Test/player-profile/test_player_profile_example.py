"""Example Player Profile case (legacy page). Copy for the real 2 cases. ponytail: 1 shipped."""
import pytest

from pixon.pages.home_page import HomePage
from pixon.pages.player_profile import PlayerProfilePage


@pytest.mark.player_profile
def test_open_player_profile(app):
    HomePage().wait_for("main_menu", timeout=30)
    assert PlayerProfilePage().wait_for("profile_title", timeout=10)
