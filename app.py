import logging
from flask import Flask, request
import requests

# ログ設定（Renderのログ画面に出力される）
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Render Flask is running"

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    logging.info("Raw data: %s", data)

    try:
        event = data["events"][0]
        if event["type"] == "message" and "text" in event["message"]:
            message = event["message"]["text"]
            logging.info("LINE message: %s", message)

            # PicoのグローバルIP＋ポート7072に送信
            pico_url = "http://117.74.28.188:8080"  # ← 最新のIPに置き換えてください
            res = requests.post(pico_url, json=data, timeout=2)
            logging.info("Pico response: %s", res.status_code)
        else:
            logging.info("非テキストメッセージを受信しました")
    except Exception as e:
        logging.error("Error parsing message: %s", e)

    return "OK", 200