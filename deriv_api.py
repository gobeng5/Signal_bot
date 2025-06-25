import websocket, json, time

SYMBOLS = {
    "Volatility 10 Index": "R_10",
    "Volatility 25 Index": "R_25",
    "Volatility 75 Index": "R_75"
}

def get_prices():
    prices = []
    for name, symbol in SYMBOLS.items():
        ws = websocket.create_connection("wss://ws.derivws.com/websockets/v3?app_id=1089")
        req = {"ticks_history": symbol, "adjust_start_time": 1, "count": 100, "granularity": 60, "style": "candles"}
        ws.send(json.dumps(req))
        res = json.loads(ws.recv())
        if "candles" in res:
            prices.append({
                "instrument": name,
                "symbol": symbol,
                "ohlc": res["candles"]
            })
        ws.close()
        time.sleep(1)
    return prices
