import logging
from flask import Flask, request
import requests

# ログ設定（Renderのログ画面に出力される）
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# LINE通知関数（Render → LINE）
def send_line_reply(reply_text):
    payload = {"message": reply_text}
    headers = {"Host": "line-proxy-dkvy.onrender.com"}

    try:
        res = requests.post("https://line-proxy-dkvy.onrender.com/notify", json=payload, headers=headers, timeout=10)
        logging.info("LINE通知ステータス: %s", res.status_code)
    except Exception as e:
        logging.error("LINE通知エラー: %s", e)

@app.route("/notify", methods=["POST"])
def callback():
    data = request.get_json()
    logging.info("Raw data: %s", data)

    try:
        if "events" in data:
            event = data["events"][0]
            if event["type"] == "message" and "text" in event["message"]:
                message = event["message"]["text"]
                logging.info("LINE message: %s", message)

                # Pico Wへ送信
                pico_url = "http://192.168.1.16:80"
                try:
                    res = requests.post(pico_url, json=data, timeout=5)
                    logging.info("Pico response: %s", res.status_code)
                    send_line_reply("送信OK" if res.status_code == 200 else "送信NG")
                except Exception as e:
                    logging.error("Pico W送信エラー: %s", e)
                    send_line_reply("送信NG")
            else:
                logging.info("非テキストメッセージを受信しました")
                send_line_reply("未対応メッセージ")
        else:
            logging.warning("LINE形式ではないデータを受信: %s", data)
    except Exception as e:
        logging.error("Error parsing message: %s", e)
        send_line_reply("送信NG")

    return "OK", 200