from flask import Flask, request
import requests

app = Flask(__name__)

LINE_TOKEN = "rrH3WhwKaEfMmKZonTs95+4OZIj1GxObEHCEugdrJUzDPRaNDigD3lPAQNbZojMgjA8Pd599qrRxl6cYLXVU8GWHQRmAudHAEvzT2juBRX2Cur1GFJ9MFINSdNJK/C1G8y6vqdjfpyFWaLg5kxM3hgdB04t89/1O/w1cDnyilFU="
LINE_TO = "U71acf266adcc910ec114580ae9746b13"

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()
    message = data.get("message", "（メッセージなし）")

    headers = {
        "Authorization": "Bearer " + LINE_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "to": LINE_TO,
        "messages": [{"type": "text", "text": message}]
    }

    res = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
    print("LINE送信ステータス:", res.status_code)
    return "OK"
