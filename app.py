from flask import Flask, request
import requests
import os

app = Flask(__name__)

# LINEチャネルアクセストークン（環境変数から取得）
LINE_TOKEN = os.environ.get("LINE_TOKEN")

# LINEユーザーID（Push通知先）← 固定でもOK、複数対応も可能
USER_ID = os.environ.get("LINE_USER_ID")

@app.route("/", methods=["GET", "HEAD"])
def index():
    return "Render Flask is running", 200

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    text = data.get("text", "通知内容なし")

    # LINE Push通知
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": text}]
    }

    try:
        res = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
        print("LINE Pushステータス:", res.status_code)
        print("LINE Pushレスポンス:", res.text)
        return {"status": "sent", "code": res.status_code}, 200
    except Exception as e:
        print("LINE送信エラー:", e)
        return {"status": "error", "message": str(e)}, 500