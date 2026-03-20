from config import *

def calculate_position(balance, price):
    """Return number of shares to buy based on current *balance* and
    *price*.  Guarantees at least one share but never spends more than the
    available cash."""
    if price <= 0:
        return 0

    risk_amount = balance * RISK_PER_TRADE
    quantity = int(risk_amount / price)
    if quantity < 1:
        quantity = 1
    # don't size a position that costs more than the balance
    max_affordable = int(balance / price)
    return min(quantity, max_affordable)


def stop_loss(entry_price):

    return entry_price * (1 - STOP_LOSS_PERCENT)


def take_profit(entry_price):

    return entry_price * (1 + TAKE_PROFIT_PERCENT)