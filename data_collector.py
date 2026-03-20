from SmartApi import SmartConnect
import pyotp
import pandas as pd
import time
from datetime import datetime, timedelta
from config import *

WATCHLIST = [
    {"symbol":"RELIANCE","token":"2885","exchange":"NSE"},
    {"symbol":"TCS","token":"11536","exchange":"NSE"},
    {"symbol":"HDFCBANK","token":"1333","exchange":"NSE"}
]

smartApi = SmartConnect(api_key=API_KEY)

def login():

    totp = pyotp.TOTP(TOTP_SECRET).now()

    data = smartApi.generateSession(
        CLIENT_CODE,
        PASSWORD,
        totp
    )

    if data["status"]:
        print("Login Successful")
    else:
        print("Login failed:", data)
        exit()

login()

start_date = datetime(2024,1,1)
end_date = datetime(2026,3,12)

for stock in WATCHLIST:

    symbol = stock["symbol"]
    token = stock["token"]
    exchange = stock["exchange"]

    print("\nDownloading:", symbol)

    all_candles = []
    current = start_date

    while current < end_date:

        batch_end = current + timedelta(days=5)

        params = {
            "exchange": exchange,
            "symboltoken": token,
            "interval": "FIVE_MINUTE",
            "fromdate": current.strftime("%Y-%m-%d 09:15"),
            "todate": batch_end.strftime("%Y-%m-%d 15:30")
        }

        response = smartApi.getCandleData(params)

        print("API status:", response["status"])

        if response["status"]:

            candles = response["data"]

            if candles:
                print("Downloaded", len(candles))
                all_candles.extend(candles)
            else:
                print("No candles returned")

        else:
            print("API Error:", response)

        current = batch_end

        time.sleep(2)

    if len(all_candles) == 0:
        print("No data for", symbol)
        continue

    df = pd.DataFrame(
        all_candles,
        columns=["time","open","high","low","close","volume"]
    )

    filename = f"{symbol}_5min_data.csv"

    df.to_csv(filename,index=False)

    print("Saved:", filename, "Rows:", len(df))