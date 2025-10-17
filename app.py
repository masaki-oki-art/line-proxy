import logging
from flask import Flask, request
import requests

# ログ設定（Renderやローカルで見やすく）
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# LINE API設定（環境変数や設定ファイルで管理するのが理想）
LINE_TOKEN = "rrH3WhwKaEfMmKZonTs95+4OZIj1GxObEHCEugdrJUzDPRaNDigD3lPAQNbZojMgjA8Pd599qrRxl6cYLXVU8GWHQRmAudHAEvzT2juBRX2Cur1GFJ9MFINSdNJK/C1G8y6vqdjfpyFWaLg5kxM3hgdB04t89/1O/w1cDnyilFU="
LINE_TO = "U885d15c80574144fd7628355631c480f"  # LINEのユーザーID

# PICOのグローバルIPとポート
PICO_URL = "http://133.207.116.194:7072"  # ← 最新のIPに置き換えてください

@app.route("/", methods=["GET"])
def index():
    return "Flask is running"

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    logging.info("Raw data: %s", data)

    try:
        event = data["events"][0]
        if event["type"] == "message" and "text" in event["message"]:
            message = event["message"]["text"]
            logging.info("LINE message: %s", message)

            # PICOに送信
            try:
                pico_res = requests.post(PICO_URL, json=data, timeout=2)
                logging.info("PICO response: %s", pico_res.status_code)

                if pico_res.status_code == 200:
                    notify_line(f"PICOにメッセージを送信しました: {message}")
                else:
                    notify_line(f"PICOから異常応答: {pico_res.status_code}")
            except Exception as e:
                logging.error("PICO送信エラー: %s", e)
                notify_line(f"PICOへの送信に失敗しました: {e}")
        else:
            logging.info("非テキストメッセージを受信しました")
            notify_line("テキスト以外のメッセージを受信しました")
    except Exception as e:
        logging.error("LINEメッセージ解析エラー: %s", e)
        notify_line(f"LINEメッセージ解析エラー: {e}")

    return "OK", 200

def notify_line(text):
    """LINEにPush通知を送る"""
    headers = {
        "Authorization": "Bearer " + LINE_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "to": LINE_TO,
        "messages": [{"type": "text", "text": str(text).strip()}]
    }
    try:
        res = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
        logging.info("LINE通知ステータス: %s", res.status_code)
    except Exception as e:
        logging.error("LINE通知エラー: %s", e)

