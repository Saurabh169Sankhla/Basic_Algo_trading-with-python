import pandas as pd

price_history = {}

def rsi(series, period=14):

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100/(1+rs))


def generate_signal(symbol, price):

    if symbol not in price_history:
        price_history[symbol] = []

    price_history[symbol].append(price)
    # keep recent history only
    if len(price_history[symbol]) > 1000:
        price_history[symbol].pop(0)

    data = pd.Series(price_history[symbol])

    if len(data) < 30:
        return "WAIT"

    short_ma = data.rolling(5).mean().iloc[-1]
    long_ma = data.rolling(20).mean().iloc[-1]

    rsi_val = rsi(data).iloc[-1]

    if short_ma > long_ma and rsi_val < 70:
        return "BUY"

    if short_ma < long_ma and rsi_val > 30:
        return "SELL"

    return "HOLD"