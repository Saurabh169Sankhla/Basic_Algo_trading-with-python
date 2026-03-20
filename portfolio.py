# simple portfolio implementation that can track multiple open positions
# keyed by symbol.  each entry stores exchange/token so LTP lookups are
# efficient and entry price/quantity for PnL calculations.

positions = {}


def open_position(symbol, price, quantity, exchange=None, token=None):
    """Record a new long position.

    Parameters
    ----------
    symbol : str
        Stock ticker.
    price : float
        Entry price.
    quantity : int
        Number of shares.
    exchange : str, optional
        Exchange code (e.g. 'NSE').
    token : str, optional
        Broker-specific token.
    """
    positions[symbol] = {
        "entry": price,
        "qty": quantity,
        "exchange": exchange,
        "token": token,
    }


def close_position(symbol):
    """Remove an open position and return its details.

    Returns
    -------
    dict or None
        The position info that was closed, or ``None`` if there was no
        position for *symbol*.
    """
    return positions.pop(symbol, None)


def get_position(symbol):
    """Return the open position for *symbol* or ``None``.
    """
    return positions.get(symbol)


def has_position(symbol):
    """Return ``True`` if a position for *symbol* is currently open."""
    return symbol in positions
