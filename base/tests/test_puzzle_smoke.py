"""Example puzzle testcase. Copy this pattern for real cases.

ponytail: the ONLY thing you must supply is the cropped screenshots in images/
(main_menu.png, btn_play.png, board.png). Re-crop them from your own game.
All actions come from one place: `import actions as a`.
"""
import pytest

import actions as a


@pytest.mark.smoke
def test_launch_to_board(app):
    a.wait_for("main_menu", timeout=30)   # app finished loading
    a.tap("btn_play")                     # start a puzzle
    # wait_for, not seen: scene transition takes frames; seen() would race.
    assert a.wait_for("board", timeout=10), "puzzle board did not appear after tapping Play"
