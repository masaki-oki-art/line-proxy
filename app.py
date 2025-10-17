from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def webhook():
    data = request.json
    user_message = data["events"][0]["message"]["text"]

    # <pico_IPはローカルIPに書き換え>
    if user_message.upper() == "ON":
        requests.post("http://192.161.1.16/led/on")
    elif user_message.upper() == "OFF":
        requests.post("http://192.161.1.16/led/off")

    return "OK"

@app.route("/")
def index():
    return "Flask app is running."

# if __name__ == "__main__":
#     app.run()  # 開発用サーバー起動は本番環境では不要