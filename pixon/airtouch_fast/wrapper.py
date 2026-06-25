"""MinitouchWrapper — socket-based gesture injection (faster than adb input).

Must serialize with the rest of the framework: every send goes through
sync.input_lock so watchdog threads and the test thread never interleave taps.
ponytail: stub socket plumbing; fill connect()/send() against minitouch protocol.
"""
from pixon.common import sync
from pixon.common.log import get_logger

log = get_logger("minitouch")


class MinitouchWrapper:
    def __init__(self, device=None):
        self._device = device
        self._sock = None

    def connect(self):
        """Push binary (utils.push_binary), start minitouch, open the socket. Stub."""
        raise NotImplementedError

    def tap(self, x, y):
        with sync.input_lock():
            self._send(f"d 0 {x} {y} 50\nc\nu 0\nc\n")

    def swipe(self, x1, y1, x2, y2, steps=10):
        with sync.input_lock():
            # ponytail: linear interpolation stub; refine timing if gestures misfire.
            self._send(f"d 0 {x1} {y1} 50\nc\n")
            for i in range(1, steps + 1):
                ix = x1 + (x2 - x1) * i // steps
                iy = y1 + (y2 - y1) * i // steps
                self._send(f"m 0 {ix} {iy} 50\nc\n")
            self._send("u 0\nc\n")

    def _send(self, payload):
        if self._sock is None:
            raise RuntimeError("minitouch socket not connected — call connect()")
        self._sock.send(payload.encode())
