import os
import time
from datetime import datetime

from broker import login, get_ltp, get_balance, place_order
from scanner import scan_market
from portfolio import open_position, close_position, has_position, get_position, positions
from risk_manager import calculate_position, stop_loss, take_profit

# log directory and file
LOG_DIR = os.path.join("logs")
LOG_FILE = os.path.join(LOG_DIR, "trades.log")


def _ensure_log():
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "a").close()


def log(msg):
    _ensure_log()
    ts = datetime.utcnow().isoformat()
    line = f"{ts} {msg}\n"
    print(line, end="")
    with open(LOG_FILE, "a") as f:
        f.write(line)


# --- startup --------------------------------------------------------------

login()

balance = get_balance()
log(f"starting account balance={balance}")

# continuously scan the market and manage any open positions
while True:
    try:
        alerts = scan_market()

        # act on each alert independently
        for stock, price, signal in alerts:
            symbol = stock["symbol"]

            if signal == "BUY" and not has_position(symbol):
                qty = calculate_position(balance, price)
                log(f"BUY signal {symbol} price={price} qty={qty}")
                # send order to broker (market order for simplicity)
                try:
                    place_order(stock.get("exchange"), stock.get("token"), "BUY", qty)
                except Exception as e:
                    log(f"order error for {symbol}: {e}")
                    continue
                open_position(
                    symbol,
                    price,
                    qty,
                    exchange=stock.get("exchange"),
                    token=stock.get("token"),
                )

            elif signal == "SELL" and has_position(symbol):
                pos = get_position(symbol)
                # when a sell signal occurs we treat it as a manual exit
                exit_price = price
                pnl = (exit_price - pos["entry"]) * pos["qty"]
                log(f"SELL signal {symbol} price={exit_price} pnl={pnl}")
                try:
                    place_order(stock.get("exchange"), stock.get("token"), "SELL", pos["qty"])
                except Exception as e:
                    log(f"order error on exit {symbol}: {e}")
                close_position(symbol)
                balance = get_balance()
                log(f"updated balance={balance}")

        # iterate over current open positions
        for symbol, pos in list(positions.items()):
            try:
                ltp = get_ltp(pos["exchange"], symbol, pos.get("token"))
            except Exception as e:
                log(f"error fetching LTP for {symbol}: {e}")
                continue

            if ltp <= stop_loss(pos["entry"]):
                log(f"STOP LOSS HIT {symbol} entry={pos['entry']} ltp={ltp}")
                try:
                    place_order(pos["exchange"], pos.get("token"), "SELL", pos["qty"])
                except Exception as e:
                    log(f"order error on stop-loss {symbol}: {e}")
                close_position(symbol)
                balance = get_balance()
                log(f"balance after stop loss={balance}")

            elif ltp >= take_profit(pos["entry"]):
                log(f"TAKE PROFIT HIT {symbol} entry={pos['entry']} ltp={ltp}")
                try:
                    place_order(pos["exchange"], pos.get("token"), "SELL", pos["qty"])
                except Exception as e:
                    log(f"order error on take-profit {symbol}: {e}")
                close_position(symbol)
                balance = get_balance()
                log(f"balance after take profit={balance}")

    except Exception as exc:
        # catch all so the loop doesn't die; log and keep going
        log(f"unexpected error: {exc}")

    # sleep before next scan; align to interval if desired
    time.sleep(60)
