"""Background thread that dismisses unexpected popups during a test.

Layer note: a watchdog must NOT import pixon.pages (that's an upward edge ->
cycle). It is given popup handlers via dependency injection. It also registers
with `sync` so tests can pause it (suppress_watchdogs) while asserting on a dialog.
ponytail: stub loop; plug real screenshot+match in _scan().
"""
import threading

from .log import get_logger
from . import sync

log = get_logger("popup-wd")


class PopupWatchdog(threading.Thread):
    def __init__(self, handlers, interval=2.0):
        """handlers: list of callables that try to detect+close one popup,
        returning True if they acted. Injected — no pages import here."""
        super().__init__(daemon=True)
        self._handlers = list(handlers)
        self._interval = interval
        self._stop = threading.Event()
        self._paused = threading.Event()

    def pause(self):
        self._paused.set()

    def resume(self):
        self._paused.clear()

    def stop(self):
        self._stop.set()

    def run(self):
        sync.register_watchdog(self)
        try:
            while not self._stop.wait(self._interval):
                if self._paused.is_set():
                    continue
                self._scan()
        finally:
            sync.unregister_watchdog(self)

    def _scan(self):
        for handler in self._handlers:
            try:
                if handler():        # handler grabs sync.input_lock() itself
                    log.info("closed popup via %s", getattr(handler, "__name__", handler))
            except Exception as e:    # never let a watchdog crash the run
                log.debug("popup handler error: %s", e)
