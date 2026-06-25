"""No-device checks for the base framework. Fail if core logic breaks.
One real check per moving part: template resolution, infra classifier,
input lock reentrancy, watchdog suppression."""
import os

import pytest

from pixon.common import actions as a
from pixon.common import config, sync, ocr


# ---- template resolution ----
def test_resolves_image_name():
    # placeholder.png ships in pages/images/
    assert a._resolve("placeholder").filename.endswith("placeholder.png")


def test_passthrough_non_string():
    pos = (10, 20)
    assert a._resolve(pos) is pos


def test_missing_image_raises():
    with pytest.raises(FileNotFoundError):
        a._resolve("does_not_exist_xyz")


# ---- infra vs code ----
def test_infra_vs_code_classification():
    assert a.is_infra_error(RuntimeError("adb server connection closed"))
    assert a.is_infra_error(OSError("device offline"))
    assert not a.is_infra_error(AssertionError("board not found"))
    assert not a.is_infra_error(ValueError("bad puzzle move"))


# ---- concurrency seam ----
def test_input_lock_is_reentrant():
    with sync.input_lock():
        with sync.input_lock():   # RLock — nested acquire must not deadlock
            assert True


def test_suppress_watchdogs_pauses_and_resumes():
    class FakeWD:
        def __init__(self): self.paused = False
        def pause(self): self.paused = True
        def resume(self): self.paused = False

    wd = FakeWD()
    sync.register_watchdog(wd)
    try:
        with sync.suppress_watchdogs():
            assert wd.paused is True
        assert wd.paused is False
    finally:
        sync.unregister_watchdog(wd)


# ---- full action surface present ----
def test_action_surface_exposed():
    for fn in ("tap", "double_tap", "swipe", "touch", "pinch", "key", "type_text",
               "wait_for", "seen", "shot", "wait", "exists", "snapshot",
               "start_app", "stop_app", "shell", "read_text", "text_present", "assert_text"):
        assert callable(getattr(a, fn)), f"missing action: {fn}"


# ---- OCR pure logic (no engine, no device) ----
def test_ocr_normalize_and_match():
    assert ocr._normalize("  Hello   WORLD\n") == "hello world"
    assert ocr._match("hello world", "...Hello   WORLD...")
    assert not ocr._match("game over", "you win")
