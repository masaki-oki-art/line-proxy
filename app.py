import logging
from flask import Flask, request
import requests

# ログ設定（Renderのログ画面に出力される）
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# LINE通知関数（Pico受信成功をLINEへ通知）
def send_line_message(text):
    payload = {"message": text}
    headers = {"Content-Type": "application/json"}
    try:
        # LINE通知は別エンドポイント（/line-notify）を使うことでループを防ぐ
        res = requests.post("http://line-proxy-dkvy.onrender.com/line-notify", json=payload, headers=headers, timeout=5)
        logging.info("LINE通知ステータス: %s", res.status_code)
    except Exception as e:
        logging.error("LINE通知エラー: %s", e)

@app.route("/", methods=["GET"])
def index():
    return "Render Flask is running"

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

                # PicoのグローバルIP＋ポート7072に送信
                pico_url = "http://133.207.116.194:7072"  # ← 最新のIPに置き換えてください
                res = requests.post(pico_url, json=data, timeout=30)
                logging.info("Pico response: %s", res.status_code)

                # Picoが200 OKを返したらLINE通知
                if res.status_code == 200:
                    send_line_message("Picoが正常に受信しました（200 OK）")
            else:
                logging.info("非テキストメッセージを受信しました")
        else:
            logging.info("LINE形式ではないPOSTを受信しました")
    except Exception as e:
        logging.error("Error parsing message: %s", e)

    return "OK", 200

# LINE通知受信用のダミーエンドポイント（ループ防止用）
@app.route("/line-notify", methods=["POST"])
def line_notify():
    data = request.get_json()
    logging.info("LINE通知受信: %s", data)
    return "OK", 200