from SmartApi import SmartConnect
import pyotp
from config import *

smartApi = SmartConnect(api_key=API_KEY)

def login():

    totp = pyotp.TOTP(TOTP_SECRET).now()

    data = smartApi.generateSession(
        CLIENT_CODE,
        PASSWORD,
        totp
    )

    return smartApi


def get_ltp(exchange, symbol, token):

    ltp = smartApi.ltpData(exchange, symbol, token)

    return ltp["data"]["ltp"]


def get_balance():
    """Return available cash from the broker account."""
    rms = smartApi.rmsLimit()
    return rms["data"]["availablecash"]


def place_order(exchange, symbol, transaction_type, quantity, price=None):
    """Submit a (simulated) order to the broker.

    For now this is a thin wrapper around the SmartAPI call; it logs the
    request and returns whatever the API returns.  ``price`` may be omitted
    for market orders.
    """
    order_params = {
        "exchange": exchange,
        "token": symbol,
        "transaction_type": transaction_type,
        "quantity": quantity,
    }
    if price is not None:
        order_params["price"] = price

    print("placing order", order_params)
    try:
        result = smartApi.placeOrder(order_params)
        return result
    except Exception as e:
        print("order failed", e)
        raise
