from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Render is running"

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json(silent=True)
    if not data or "events" not in data:
        return "Bad Request", 400

    message = data["events"][0]["message"]["text"]
    print("LINE message:", message)

    # PicoのグローバルIP＋ポート7072に送信
    pico_url = "http://133.207.116.194:7072"  # ← ここを最新IPに変更
    try:
        res = requests.post(pico_url, json=data, timeout=2)
        print("Pico response:", res.status_code)
    except Exception as e:
        print("Error sending to Pico:", e)

    return "OK", 200

if __name__ == "__main__":
    app.run()