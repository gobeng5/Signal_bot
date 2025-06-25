from flask import Flask, render_template, request, jsonify
from deriv_api import get_prices
from signal_logic import generate_signals
from telegram_bot import send_top_signal

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        prices = get_prices()
        signals = generate_signals(prices)
        if not signals:
            return jsonify({"error": "No signals generated"}), 200
        top_signal = max(signals, key=lambda s: s.get("confidence", 0))
        send_top_signal(top_signal)
        return jsonify(signals)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    prices = get_prices()
    signals = generate_signals(prices)
    if signals:
        top_signal = max(signals, key=lambda s: s.get("confidence", 0))
        send_top_signal(top_signal)
    app.run(host="0.0.0.0", port=81)
