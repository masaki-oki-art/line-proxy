import logging
import threading
from flask import Flask, request
import requests

# ログ設定（Renderのログ画面に出力される）
logging.basicConfig(level=logging.INFO)

# Flaskアプリケーションの定義
app = Flask(__name__)

# LINE通知関数（Messaging APIのPush通知）
def send_line_message(user_id, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer rrH3WhwKaEfMmKZonTs95+4OZIj1GxObEHCEugdrJUzDPRaNDigD3lPAQNbZojMgjA8Pd599qrRxl6cYLXVU8GWHQRmAudHAEvzT2juBRX2Cur1GFJ9MFINSdNJK/C1G8y6vqdjfpyFWaLg5kxM3hgdB04t89/1O/w1cDnyilFU="
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }
    try:
        res = requests.post("https://api.line.me/v2/bot/message/push", json=payload, headers=headers, timeout=10)
        logging.info("LINE通知ステータス: %s", res.status_code)
    except Exception as e:
        logging.error("LINE通知エラー: %s", e)


# 非同期でLINE通知を送る関数
def send_line_message_async(user_id, text):
    threading.Thread(target=send_line_message, args=(user_id, text)).start()

# 動作確認用エンドポイント
@app.route("/", methods=["GET"])
def index():
    return "Render Flask is running"

# LINE Webhook専用エンドポイント
@app.route("/notify", methods=["POST"])
def callback():
    data = request.get_json()
    logging.info("Raw data: %s", data)

    try:
        # LINE Webhook形式かどうかを判定
        if "events" in data:
            event = data["events"][0]
            if event["type"] == "message" and "text" in event["message"]:
                message = event["message"]["text"]
                user_id = event["source"]["userId"]
                logging.info("LINE message: %s", message)
                logging.info("LINE user ID: %s", user_id)

                # Pico Wにメッセージを転送
                pico_url = "http://133.207.116.194:7072"  # ← 最新のIPに置き換えてください
                res = requests.post(pico_url, json=data, timeout=30)
                logging.info("Pico response: %s", res.status_code)

                # Picoが200 OKを返したらLINE通知（非同期）
                if res.status_code == 200:
                    send_line_message_async(user_id, "Picoが正常に受信しました（200 OK）")
            else:
                logging.info("非テキストメッセージを受信しました")
        else:
            logging.info("LINE形式ではないPOSTを受信しました")
    except Exception as e:
        logging.error("Error parsing message: %s", e)

    return "OK", 200