# Algo Trading System

This simple Python project contains a backtester and a very basic live
trading skeleton.  It is **not** production ready and is provided for
educational purposes only.

## Components

* `config.py` - credentials, risk parameters, and watchlist.
* `strategy.py` - moving average + RSI signal generator.
* `scanner.py` - iterates watchlist and returns BUY/SELL alerts.
* `risk_manager.py` - position sizing, stop‑loss and take‑profit helpers.
* `portfolio.py` - keeps track of open positions (can hold multiple symbols).
* `broker.py` - wrapper around SmartAPI (login, ltp, balance, place order).
* `backtester.py` - run historical data files and calculate performance metrics.
* `live_trader.py` - enhanced live loop that places orders, logs trades,
  handles both BUY and SELL signals, and manages stop‑loss/take‑profit.

## Running

1. Install required packages (`pandas`, `SmartApi`, `pyotp`, etc.).
2. Populate `config.py` with valid credentials and watchlist tokens.
3. Run `python backtester.py` to evaluate strategy on historical CSVs.
4. Run `python live_trader.py` to start the live trading loop (paper trade).

> ⚠️ **Warning:**  This code does not handle real exchange throttling,
> partial fills, slippage, or order confirmations.  Always test in a
> sandbox/paper environment before risking real money.
