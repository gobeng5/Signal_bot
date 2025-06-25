import websocket
import json
import time

SYMBOLS = {
    "Volatility 10 Index": "R_10",
    "Volatility 25 Index": "R_25",
    "Volatility 75 Index": "R_75"
}

def fetch_live_prices():
    prices = []
    for name, symbol in SYMBOLS.items():
        try:
            ws = websocket.create_connection("wss://ws.derivws.com/websockets/v3?app_id=1089")
            request = {
                "ticks": symbol,
                "subscribe": 1
            }
            ws.send(json.dumps(request))
            data = json.loads(ws.recv())
            quote = float(data["tick"]["quote"])
            prices.append({
                "instrument": name,
                "symbol": symbol,
                "close": quote
            })
            ws.close()
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error fetching price for {name}: {e}")
    return prices