from flask import Flask, request
import os
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "LINE Proxy is running!"

@app.route("/callback", methods=["POST"])
def callback():
    print("=== LINE Webhook Received ===", flush=True)
    raw_body = request.data.decode("utf-8")
    print("Raw body:", raw_body, flush=True)

    try:
        data = request.get_json(silent=True)
        if not data or "events" not in data:
            print("Invalid JSON structure", flush=True)
            return "Bad Request", 400

        event = data["events"][0]
        if event.get("type") == "message" and event["message"].get("type") == "text":
            message = event["message"]["text"].lower()
            print("User message:", message, flush=True)

            if message in ["test1", "test2"]:
                send_to_pico(message)
            else:
                print("Unknown command", flush=True)
        else:
            print("Non-text message received", flush=True)
    except Exception as e:
        print("Error parsing message:", type(e), e, flush=True)

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
