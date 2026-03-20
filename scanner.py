from broker import get_ltp
from strategy import generate_signal
from config import WATCHLIST


def scan_market():
    """Walk the watchlist and generate signals.

    Returns
    -------
    list of tuples
        Each tuple is ``(stock_dict, price, signal)`` where *signal* is one
        of ``"BUY"``, ``"SELL"``, ``"HOLD"`` or ``"WAIT"``.  Only
        non‑HOLD/WAIT signals are returned so callers can act on them.
    """
    alerts = []

    for stock in WATCHLIST:
        try:
            price = get_ltp(
                stock["exchange"],
                stock["symbol"],
                stock["token"]
            )
        except Exception as e:
            # log failure and skip this stock
            print("failed to fetch LTP for", stock["symbol"], e)
            continue

        signal = generate_signal(stock["symbol"], price)

        print(stock["symbol"], price, signal)

        if signal in ("BUY", "SELL"):
            alerts.append((stock, price, signal))

    return alerts
