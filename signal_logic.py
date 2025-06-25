import pandas as pd
import numpy as np
from pattern_recognition import detect_candlestick_patterns, detect_chart_patterns

def generate_signals(price_data):
    signals = []
    for item in price_data:
        df = item.get("ohlc")
        if df is None or "close" not in df:
            continue

        instrument = item["instrument"]
        df["returns"] = df["close"].pct_change()
        df["ma_20"] = df["close"].rolling(window=20).mean()

        candle_patterns = detect_candlestick_patterns(df)
        chart_patterns = detect_chart_patterns(df)

        for pattern in candle_patterns + chart_patterns:
            signal = {
                "instrument": instrument,
                "type": "pattern",
                "pattern": pattern["pattern"],
                "confidence": pattern["confidence"],
                "entry": pattern["entry"],
                "exit": pattern["exit"]
            }
            signals.append(signal)

    return signals
