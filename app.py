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
    print("Raw request data:", request.data)  # ← 追加
    print("Parsed JSON:", data)               # ← 追加

    try:
        event = data["events"][0]
        if event["type"] == "message" and event["message"]["type"] == "text":
            message = event["message"]["text"]
            print("User message:", message)

            if message == "test1":
                print("Calling send_to_pico with test1")
                send_to_pico("test1")
            elif message == "test2":
                print("Calling send_to_pico with test2")
                send_to_pico("test2")
            else:
                print("Unknown command")
        else:
            print("Non-text message received, skipping")
    except Exception as e:
        print("Error parsing message:", e)

    return "OK", 200

def send_to_pico(command):
    pico_ip = "http://192.168.1.14"
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
        res = requests.post(pico_ip, json=payload, headers={"Content-Type": "application/json"}, timeout=2)
        print("Status code:", res.status_code)
        print("Response text:", res.text)
    except Exception as e:
        print("Failed to send to Pico:", e)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
