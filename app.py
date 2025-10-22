import logging
import threading
from flask import Flask, request
import requests

# ログ設定（Renderのログ画面に出力される）
logging.basicConfig(level=logging.INFO)

# Flaskアプリケーションの定義
app = Flask(__name__)

# LINE通知関数（Pico受信成功をLINEへ通知）
def send_line_message(text):
    payload = {"message": text}
    headers = {"Content-Type": "application/json"}
    try:
        # 通知は /line-notify に送ることで /notify へのループを防ぐ
        res = requests.post("http://line-proxy-dkvy.onrender.com/line-notify", json=payload, headers=headers, timeout=10)
        logging.info("LINE通知ステータス: %s", res.status_code)
    except Exception as e:
        logging.error("LINE通知エラー: %s", e)

# 非同期でLINE通知を送る関数
def send_line_message_async(text):
    threading.Thread(target=send_line_message, args=(text,)).start()

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
                logging.info("LINE message: %s", message)

                # Pico Wにメッセージを転送
                pico_url = "http://133.207.116.194:7072"  # ← 最新のIPに置き換えてください
                res = requests.post(pico_url, json=data, timeout=30)
                logging.info("Pico response: %s", res.status_code)

                # Picoが200 OKを返したらLINE通知（非同期）
                if res.status_code == 200:
                    send_line_message_async("Picoが正常に受信しました（200 OK）")
            else:
                logging.info("非テキストメッセージを受信しました")
        else:
            logging.info("LINE形式ではないPOSTを受信しました")
    except Exception as e:
        logging.error("Error parsing message: %s", e)

    return "OK", 200

# LINE通知専用エンドポイント（通知ループ防止用）
@app.route("/line-notify", methods=["POST"])
def line_notify():
    data = request.get_json()
    logging.info("LINE通知受信: %s", data)
    return "OK", 200