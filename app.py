from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    user_text = data["events"][0]["message"]["text"]
    reply_token = data["events"][0]["replyToken"]

    # Pico Wに指令を送信
    try:
        res = requests.post("http://192.168.1.16/control", json={"text": user_text}, timeout=3)
        if res.status_code == 200:
            reply_text = "Pico Wに指令を送信しました"
        else:
            reply_text = f"Pico Wが応答しませんでした（コード: {res.status_code}） "
    except Exception as e:
        reply_text = f"Pico Wへの送信に失敗しました\nエラー: {str(e)}"

    # LINEに返信
    headers = {
        "Authorization": "Bearer rrH3WhwKaEfMmKZonTs95+4OZIj1GxObEHCEugdrJUzDPRaNDigD3lPAQNbZojMgjA8Pd599qrRxl6cYLXVU8GWHQRmAudHAEvzT2juBRX2Cur1GFJ9MFINSdNJK/C1G8y6vqdjfpyFWaLg5kxM3hgdB04t89/1O/w1cDnyilFU=",
        "Content-Type": "application/json"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": reply_text}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=payload)

    return "OK"