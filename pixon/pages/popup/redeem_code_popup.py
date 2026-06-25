"""Redeem-code popup handler. ponytail: stub selectors."""
from pixon.common import actions as a


def handle_redeem_code():
    if a.seen("popup_redeem_code"):
        a.tap("popup_redeem_close")
        return True
    return False
