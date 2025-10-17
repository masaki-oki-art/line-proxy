from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def webhook():
    data = request.json
    user_message = data["events"][0]["message"]["text"].strip()

    # PICOにそのままメッセージを渡す
    try:
        requests.post("http://192.168.1.16", json={"message": user_message})
    except Exception as e:
        print("PICO転送エラー:", e)

    return "OK"

@app.route("/")
def index():
    return "Flask app is running."