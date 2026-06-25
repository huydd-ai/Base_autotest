"""ADB helpers for minitouch/minicap: ABI detection + binary push. ponytail: stubs.

Review flag: minicap is unmaintained and breaks on Android 10+. LDPlayer's older
Android is usually fine; keep airtest-touch (actions.tap) as the fallback path.
"""
from airtest.core.api import shell


def detect_abi(device=None):
    """Return device ABI (armeabi-v7a / arm64-v8a / x86 ...) to pick the right binary."""
    return shell("getprop ro.product.cpu.abi").strip()


def push_binary(local_path, remote_path, device=None):
    """Push a minitouch/minicap binary and chmod +x. Stub."""
    raise NotImplementedError("wire adb push + chmod for the selected ABI binary")
