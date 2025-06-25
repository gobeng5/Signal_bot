import requests, os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_top_signal(signal):
    if not TOKEN or not CHAT_ID:
        print("Missing token or chat ID")
        return
    msg = (
        f"📈 Signal Alert\n\n"
        f"Instrument: {signal.get('instrument')}\n"
        f"Patterns: {', '.join(signal.get('patterns', []))}\n"
        f"Chart Pattern: {signal.get('chart_pattern')}\n"
        f"Confidence: {signal.get('confidence')*100:.1f}%\n"
        f"Entry: {signal.get('entry')}\n"
        f"Exit: {signal.get('exit')}"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    requests.post(url, data=data)
