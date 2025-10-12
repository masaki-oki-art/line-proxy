from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "LINE Proxy is running!"

@app.route("/callback", methods=["POST"])
def callback():
    # LINEからのWebhookを受け取ってログに出力
    print("=== LINE Webhook Received ===")
    print("Headers:", dict(request.headers))
    print("Body:", request.get_data(as_text=True))
    return "OK", 200

if __name__ == "__main__":
    # Renderが割り当てるポート番号を取得して起動
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)