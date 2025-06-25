import pandas as pd
import talib

def detect_candlestick_patterns(df):
    patterns = {
        "Hammer": talib.CDLHAMMER,
        "Doji": talib.CDLDOJI,
        "Engulfing": talib.CDLENGULFING,
        "Morning Star": talib.CDLMORNINGSTAR
    }
    results = []
    for name, func in patterns.items():
        out = func(df["open"], df["high"], df["low"], df["close"])
        if out.iloc[-1] != 0:
            results.append(name)
    return results

def detect_chart_pattern(df):
    recent_highs = df["high"].rolling(window=5).max()
    recent_lows = df["low"].rolling(window=5).min()
    if df["high"].iloc[-1] >= recent_highs.iloc[-1]:
        return "Possible Breakout"
    elif df["low"].iloc[-1] <= recent_lows.iloc[-1]:
        return "Possible Breakdown"
    return None

def generate_signals(price_data):
    signals = []
    for instrument in price_data:
        try:
            df = pd.DataFrame(instrument["ohlc"])
            df = df.astype(float)

            candlestick_patterns = detect_candlestick_patterns(df)
            chart_pattern = detect_chart_pattern(df)

            signal = {
                "instrument": instrument["instrument"],
                "type": "pattern_analysis",
                "patterns": candlestick_patterns,
                "chart_pattern": chart_pattern,
                "confidence": 0.85,
                "entry": df["close"].iloc[-1],
                "exit": df["close"].iloc[-1] * 1.02
            }
            signals.append(signal)
        except Exception as e:
            print("Error processing:", instrument["instrument"], e)
    return signals
