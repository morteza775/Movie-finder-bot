
import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ["BOT_TOKEN"]
SECRET = os.environ["WEBHOOK_SECRET"]

API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=20
    )

@app.route("/")
def home():
    return "Movie Finder Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token"
    ) != SECRET:
        return "Unauthorized", 403

    data = request.get_json()
    message = data.get("message", {})

    chat = message.get("chat", {})
    text = message.get("text", "")

    if chat and text:
        if text == "/start":
            reply = "سلام! 🎬 اسم فیلم موردنظرت رو بفرست."
        else:
            reply = f"درخواست فیلم شما دریافت شد: {text}\nبه‌زودی جست‌وجو می‌کنم!"

        send_message(chat["id"], reply)

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
