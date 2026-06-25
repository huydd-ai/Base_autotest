"""Logging — cross-cutting, split out of the old god `wrappers.py`."""
import logging
import os

from . import config

_FMT = "%(asctime)s %(levelname)s %(name)s | %(message)s"


def get_logger(name="pixon"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter(_FMT))
        logger.addHandler(h)
        logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    return logger
