import pandas as pd
from strategy import generate_signal

FILES = [
    "RELIANCE_5min_data.csv",
    "TCS_5min_data.csv",
    "HDFCBANK_5min_data.csv"
]

STARTING_BALANCE = 100000


def calculate_drawdown(equity_curve):

    peak = equity_curve[0]
    max_dd = 0

    for value in equity_curve:

        if value > peak:
            peak = value

        drawdown = peak - value

        if drawdown > max_dd:
            max_dd = drawdown

    return max_dd


results = []

for file in FILES:

    symbol = file.split("_")[0]

    df = pd.read_csv(file)

    balance = STARTING_BALANCE
    position = None
    entry_price = 0

    trades = []
    equity_curve = []

    for index, row in df.iterrows():

        price = row["close"]

        signal = generate_signal(symbol, price)

        if signal == "BUY" and position is None:

            position = "LONG"
            entry_price = price

        elif signal == "SELL" and position == "LONG":

            pnl = price - entry_price
            balance += pnl
            trades.append(pnl)

            position = None

        equity_curve.append(balance)

    total_profit = balance - STARTING_BALANCE
    total_trades = len(trades)

    wins = len([t for t in trades if t > 0])
    losses = len([t for t in trades if t <= 0])

    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0

    gross_profit = sum([t for t in trades if t > 0])
    gross_loss = abs(sum([t for t in trades if t < 0]))

    profit_factor = (gross_profit / gross_loss) if gross_loss != 0 else 0

    max_drawdown = calculate_drawdown(equity_curve)

    # Strategy score
    score = (total_profit * 0.4) + (win_rate * 0.4) + (profit_factor * 20) - (max_drawdown * 0.1)

    results.append({
        "symbol": symbol,
        "profit": total_profit,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "drawdown": max_drawdown,
        "score": score
    })


print("\n===== Backtest Summary =====\n")

best_stock = None
best_score = -999999

for r in results:

    print("Stock:", r["symbol"])
    print("Profit:", round(r["profit"],2))
    print("Win Rate:", round(r["win_rate"],2),"%")
    print("Profit Factor:", round(r["profit_factor"],2))
    print("Max Drawdown:", round(r["drawdown"],2))
    print("Score:", round(r["score"],2))
    print()

    if r["score"] > best_score:
        best_score = r["score"]
        best_stock = r["symbol"]


print("================================")
print("Best Stock To Trade:", best_stock)
print("Score:", round(best_score,2))
print("================================")