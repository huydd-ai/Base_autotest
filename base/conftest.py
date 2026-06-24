"""pytest fixtures: connect to LDPlayer once per session, start/stop the app,
and guard every test against device/adb drops."""
import json
import os
import time

import pytest

from airtest.core.api import connect_device, start_app, stop_app

import actions
import config


@pytest.fixture(scope="session")
def device():
    """Connect to the emulator for the whole test run."""
    return connect_device(config.DEVICE_URI)


@pytest.fixture
def app(device):
    """Fresh app launch per test; stop it on teardown."""
    start_app(config.APP_PACKAGE)
    yield
    stop_app(config.APP_PACKAGE)


def _record_drop(nodeid, exc):
    """Save evidence so a device-drop test isn't lost: a jsonl line + best-effort shot."""
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    safe = nodeid.replace("/", "_").replace("::", "__")
    rec = {"test": nodeid, "reason": repr(exc),
           "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(os.path.join(config.RESULTS_DIR, "drops.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    try:
        actions.shot(os.path.join(config.RESULTS_DIR, safe + ".png"))
    except Exception:
        pass  # device is gone — the jsonl record already preserved the case


@pytest.fixture(autouse=True)
def infra_guard(request):
    """Boundary: if a test dies from adb/device loss (not its own asserts),
    save evidence and SKIP it — keeps real failures and infra drops separate."""
    try:
        yield
    except Exception as e:
        if actions.is_infra_error(e):
            _record_drop(request.node.nodeid, e)
            pytest.skip(f"INFRA DROP (device/adb, not code): {e}")
        raise
