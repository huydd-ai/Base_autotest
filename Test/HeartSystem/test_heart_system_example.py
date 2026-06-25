"""Example Heart System case. Copy this for the real 31 cases. ponytail: 1 shipped."""
import pytest

from pixon.pages.home_page import HomePage
from pixon.pages.heart_system_page import HeartSystemPage


@pytest.mark.heart_system
def test_open_heart_system(app):
    HomePage().wait_for("main_menu", timeout=30)
    assert HeartSystemPage().wait_for("heart_panel", timeout=10)
