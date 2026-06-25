"""Root pytest fixtures: device connect, app lifecycle, infra boundary, watchdog suppression."""
import json
import os
import time

import pytest

from airtest.core.api import connect_device, start_app, stop_app

from pixon.common import actions, config, sync


@pytest.fixture(scope="session")
def device():
    """Connect to the emulator once for the whole run."""
    config.require_game()          # fail loud if GAME profile/images missing
    return connect_device(config.DEVICE_URI)


@pytest.fixture
def app(device):
    """Fresh app launch per test; stop on teardown."""
    start_app(config.APP_PACKAGE)
    yield
    stop_app(config.APP_PACKAGE)


@pytest.fixture
def suppress_popups():
    """Pause watchdogs inside a test block: `with suppress_popups(): assert ...`."""
    return sync.suppress_watchdogs


def _record_drop(nodeid, exc):
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    safe = nodeid.replace("/", "_").replace("::", "__")
    rec = {"test": nodeid, "reason": repr(exc), "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    with open(os.path.join(config.RESULTS_DIR, "drops.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    try:
        actions.shot(os.path.join(config.RESULTS_DIR, safe + ".png"))
    except Exception:
        pass  # device gone — jsonl record already preserved the case


@pytest.fixture(autouse=True)
def infra_guard(request):
    """adb/device loss -> save evidence + SKIP (not a code failure). Real asserts still fail."""
    try:
        yield
    except Exception as e:
        if actions.is_infra_error(e):
            _record_drop(request.node.nodeid, e)
            pytest.skip(f"INFRA DROP (device/adb, not code): {e}")
        raise
