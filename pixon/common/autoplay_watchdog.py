"""Background thread detecting autoplay stalls and nudging recovery.

Same layer rule as popup_watchdog: no pages import; recovery action injected.
ponytail: stuck-detection is a stub (screen-unchanged-for-N-checks). Tune later.
"""
import threading

from .log import get_logger
from . import sync

log = get_logger("autoplay-wd")


class AutoplayWatchdog(threading.Thread):
    def __init__(self, recover, interval=5.0, stuck_after=3):
        """recover: callable invoked when stuck. stuck_after: consecutive
        no-progress checks before recovering."""
        super().__init__(daemon=True)
        self._recover = recover
        self._interval = interval
        self._stuck_after = stuck_after
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
        misses = 0
        try:
            while not self._stop.wait(self._interval):
                if self._paused.is_set():
                    continue
                if self._is_stuck():
                    misses += 1
                    if misses >= self._stuck_after:
                        log.warning("autoplay stuck — recovering")
                        try:
                            self._recover()
                        except Exception as e:
                            log.debug("recover error: %s", e)
                        misses = 0
                else:
                    misses = 0
        finally:
            sync.unregister_watchdog(self)

    def _is_stuck(self):
        # ponytail: stub. Real impl: compare consecutive screenshots / a progress signal.
        return False
