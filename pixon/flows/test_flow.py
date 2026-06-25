"""Flow orchestration: go_home_clean, run_step, close_all_popups.

Review delta: lifted OUT of common/ into its own layer ABOVE pages. Flows may
import pages; common may NOT import pages/flows. This breaks the latent
common -> pages -> common cycle the original tree had.
ponytail: bodies are stubs wired to page objects; fill as pages get real selectors.
"""
from pixon.common.log import get_logger
from pixon.common import sync

log = get_logger("flow")


def close_all_popups(home_page):
    """Dismiss any stacked popups until the home screen is reachable."""
    with sync.suppress_watchdogs():           # we drive popups ourselves here
        # ponytail: stub — loop home_page.popup handlers until none seen.
        raise NotImplementedError


def go_home_clean(home_page):
    """Return the app to a known-clean home state."""
    close_all_popups(home_page)
    raise NotImplementedError


def run_step(name, fn, *args, **kw):
    """Run one labelled step with logging; lets reports read like a script."""
    log.info("STEP: %s", name)
    return fn(*args, **kw)
