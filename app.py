import logging
import threading
from flask import Flask, request
import requests

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# LINE通知関数
def send_line_message(user_id, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer rrH3WhwKaEfMmKZonTs95+4OZIj1GxObEHCEugdrJUzDPRaNDigD3lPAQNbZojMgjA8Pd599qrRxl6cYLXVU8GWHQRmAudHAEvzT2juBRX2Cur1GFJ9MFINSdNJK/C1G8y6vqdjfpyFWaLg5kxM3hgdB04t89/1O/w1cDnyilFU="
    }
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": text}]
    }
    try:
        res = requests.post(
            "https://api.line.me/v2/bot/message/push",
            json=payload,
            headers=headers,
            timeout=10
        )
        logging.info("LINE通知ステータス: %s", res.status_code)
    except Exception as e:
        logging.error("LINE通知エラー: %s", e)

def send_line_message_async(user_id, text):
    threading.Thread(target=send_line_message, args=(user_id, text)).start()

# Pico が取りに来るメッセージ保存領域
latest_message = None

@app.route("/", methods=["GET"])
def index():
    return "Render Flask is running"

# LINE Webhook
@app.route("/notify", methods=["POST"])
def callback():
    global latest_message

    data = request.get_json()
    logging.info("Raw data: %s", data)

    try:
        if "events" in data:
            event = data["events"][0]

            if event["type"] == "message" and "text" in event["message"]:
                message = event["message"]["text"]
                user_id = event["source"]["userId"]

                logging.info("LINE message: %s", message)
                logging.info("LINE user ID: %s", user_id)

                # 🔵 Pico が取りに来れるように保存
                latest_message = message

    except Exception as e:
        logging.error("Error parsing message: %s", e)

    return "OK", 200

# 🔵 Pico がポーリングする API
@app.route("/poll", methods=["GET"])
def poll():
    global latest_message
    return {"message": latest_message}
