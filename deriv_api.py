import websocket
import json
import time
import pandas as pd

SYMBOLS = {
    "Volatility 10 Index": "R_10",
    "Volatility 25 Index": "R_25",
    "Volatility 75 Index": "R_75"
}

def fetch_ohlc(symbol):
    ws = websocket.create_connection("wss://ws.derivws.com/websockets/v3?app_id=1089")
    request = {
        "candles": symbol,
        "count": 100,
        "granularity": 60
    }
    ws.send(json.dumps(request))
    response = json.loads(ws.recv())
    ws.close()
    if response.get("error"):
        print(f"❌ Failed to fetch OHLC data: {response}")
        return None
    candles = response.get("candles", [])
    return pd.DataFrame(candles)

def get_prices():
    price_data = []
    for name, symbol in SYMBOLS.items():
        df = fetch_ohlc(symbol)
        if df is not None:
            price_data.append({
                "instrument": name,
                "symbol": symbol,
                "ohlc": df
            })
        time.sleep(1)
    return price_data
