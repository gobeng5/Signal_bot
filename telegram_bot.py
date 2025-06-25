import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_top_signal(signal):
    if not TOKEN or not CHAT_ID:
        print("❌ Telegram token or chat ID not set.")
        return

    msg = (
        f"📈 *Signal Alert*

"
        f"Instrument: {signal['instrument']}
"
        f"Pattern: {signal.get('pattern', 'N/A')}
"
        f"Confidence: {signal['confidence'] * 100:.1f}%
"
        f"Entry: {signal['entry']}
"
        f"Exit: {signal['exit']}"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }

    res = requests.post(url, data=data)
    print(f"Telegram response: {res.status_code} - {res.text}")
