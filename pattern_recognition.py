def detect_candlestick_patterns(df):
    signals = []
    if len(df) < 2:
        return signals
    last = df.iloc[-1]
    prev = df.iloc[-2]
    if prev["close"] < prev["open"] and last["close"] > last["open"] and last["close"] > prev["open"]:
        signals.append({
            "pattern": "Bullish Engulfing",
            "confidence": 0.85,
            "entry": last["close"],
            "exit": last["close"] + 2 * abs(last["close"] - last["open"])
        })
    return signals

def detect_chart_patterns(df):
    signals = []
    if len(df) < 20:
        return signals
    recent = df["close"].tail(20).values
    if recent[-1] > max(recent[:-1]):
        signals.append({
            "pattern": "Breakout",
            "confidence": 0.8,
            "entry": recent[-1],
            "exit": recent[-1] + (recent[-1] - min(recent))
        })
    return signals
