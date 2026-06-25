"""Example Daily Mission case. Copy this for the real 33 cases.

ponytail: 1 example shipped, not 33 empty stubs. Real cases need real screen crops.
"""
import pytest

from pixon.pages.home_page import HomePage
from pixon.pages.daily_mission import DailyMissionPage


@pytest.mark.daily_mission
def test_open_daily_mission(app):
    home = HomePage()
    home.wait_for("main_menu", timeout=30)
    # ... navigate to daily mission, then:
    assert DailyMissionPage().wait_for("daily_mission_title", timeout=10)
