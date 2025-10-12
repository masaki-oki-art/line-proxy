from flask import Flask, request
import os
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "LINE Proxy is running!"

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    print("=== LINE Webhook Received ===")
    print("Body:", data)

    try:
        message = data["events"][0]["message"]["text"]
        print("User message:", message)

        # メッセージに応じてPicoに送信
        if message == "test1":
            send_to_pico("test1")
        elif message == "test2":
            send_to_pico("test2")
        else:
            print("Unknown command")

    except Exception as e:
        print("Error parsing message:", e)

    return "OK", 200

def send_to_pico(command):
    pico_ip = "http://192.168.1.14"  # ← Pico WのIPアドレスに置き換えてください
    payload = {
        "events": [
            {
                "message": {
                    "text": command
                }
            }
        ]
    }
    try:
        res = requests.post(pico_ip, json=payload, timeout=2)
        print("Pico response:", res.text)
    except Exception as e:
        print("Failed to send to Pico:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
