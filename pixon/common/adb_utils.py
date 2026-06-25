"""ADB helpers: cold/warm start, cheat endpoints. ponytail: stubs — fill with
your game's real package + cheat URLs/intents."""
from airtest.core.api import start_app, stop_app, shell

from . import config
from .log import get_logger

log = get_logger("adb")


def cold_start(pkg=None):
    """Force-stop then launch — guarantees a fresh process."""
    pkg = pkg or config.APP_PACKAGE
    stop_app(pkg)
    start_app(pkg)


def warm_start(pkg=None):
    """Launch without force-stop — resumes if already running."""
    start_app(pkg or config.APP_PACKAGE)


def cheat(endpoint, **params):
    """Hit a debug/cheat endpoint (intent/deeplink/http). Stub.
    Implement against your build's cheat surface, e.g.:
        shell(f'am broadcast -a com.yourgame.CHEAT --es cmd "{endpoint}"')"""
    raise NotImplementedError("cheat endpoint not wired for this build")
