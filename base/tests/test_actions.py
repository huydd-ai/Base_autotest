"""No-device checks for the base. Fail if target-resolution or the infra/code
boundary logic breaks."""
import os

import pytest

import actions as a
import config


def test_resolves_image_name():
    # placeholder.png ships in images/; name accepted with or without .png
    assert a._resolve("placeholder").filename.endswith("placeholder.png")
    assert a._resolve("placeholder.png").filename == os.path.join(
        config.IMAGES_DIR, "placeholder.png"
    )


def test_passthrough_non_string():
    pos = (100, 200)
    assert a._resolve(pos) is pos        # raw coord untouched


def test_missing_image_raises():
    with pytest.raises(FileNotFoundError):
        a._resolve("does_not_exist_xyz")


def test_infra_vs_code_classification():
    assert a.is_infra_error(RuntimeError("adb server connection closed"))   # device drop
    assert a.is_infra_error(OSError("device offline"))
    assert not a.is_infra_error(AssertionError("board not found"))          # real test fail
    assert not a.is_infra_error(ValueError("bad puzzle move"))
