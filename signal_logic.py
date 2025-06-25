import pandas as pd
import numpy as np

def generate_signals(prices):
    signals = []
    for price in prices:
        try:
            df = pd.DataFrame([price])
            close = df["close"].iloc[-1]
            direction = "buy" if close % 2 == 0 else "sell"  # Dummy logic
            signal = {
                "instrument": price["instrument"],
                "type": "trend",
                "direction": direction,
                "entry": close,
                "exit": close * (1.01 if direction == "buy" else 0.99),
                "confidence": 90.0
            }
            signals.append(signal)
        except Exception as e:
            print("❌ Failed to generate signal:", e)
    return signals