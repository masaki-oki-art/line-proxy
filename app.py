from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 最新メッセージを保存する変数（グローバル）
latest_message = {"text": ""}

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
                latest_message["text"] = message  # 保存
                print("Message stored:", message, flush=True)
            else:
                print("Unknown command", flush=True)
        else:
            print("Non-text message received", flush=True)
    except Exception as e:
        print("Error parsing message:", type(e), e, flush=True)

    return "OK", 200

@app.route("/latest", methods=["GET"])
def latest():
    return jsonify(latest_message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)