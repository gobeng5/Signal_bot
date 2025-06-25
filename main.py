from flask import Flask, render_template, request, jsonify
from deriv_api import get_prices
from signal_logic import generate_signals
from telegram_bot import send_top_signal
import os
import datetime

app = Flask(__name__)

# In-memory counter to limit signals
daily_signals_sent = []

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    global daily_signals_sent
    today = datetime.date.today()
    daily_signals_sent = [t for t in daily_signals_sent if t == today]

    try:
        prices = get_prices()
        signals = generate_signals(prices)

        if not signals:
            return jsonify({"error": "No signals generated"}), 200

        signals = sorted(signals, key=lambda s: s.get("confidence", 0), reverse=True)
        signals = [s for s in signals if s.get("confidence", 0) >= 0.8][:10 - len(daily_signals_sent)]

        if not signals:
            return jsonify({"message": "No high-confidence signals remaining for today"}), 200

        for signal in signals:
            send_top_signal(signal)
            daily_signals_sent.append(today)

        return jsonify(signals)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
