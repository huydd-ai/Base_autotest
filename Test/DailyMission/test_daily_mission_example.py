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
    page = DailyMissionPage()
    assert page.wait_for("daily_mission_title", timeout=10)
    # OCR text check (needs tesseract). region = (x1,y1,x2,y2) of the header.
    page.assert_text("daily mission", region=(0, 0, 1080, 300))
