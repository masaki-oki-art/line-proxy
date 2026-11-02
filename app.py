import time
import logging
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

latest_message = None

@app.route("/", methods=["GET"])
def index():
    return "Render Flask is running"

@app.route("/notify", methods=["POST"])
def callback():
    global latest_message

    data = request.get_json()
    logging.info("Raw data: %s", data)

    try:
        if "events" in data:
            event = data["events"][0]

            if event["type"] == "message":
                latest_message = {
                    "message": event["message"]["text"],
                    "timestamp": time.time()
                }
                logging.info(
                    "Message stored: %s",
                    latest_message
                )

    except Exception as e:
        logging.error(e)

    return "OK", 200


@app.route("/poll", methods=["GET"])
def poll():

    global latest_message

    if latest_message is None:
        return jsonify({
            "message": None
        })

    age = time.time() - latest_message["timestamp"]

    # 30分以上古いなら破棄
    if age > 600:

        logging.info(
            "Old message discarded: %s",
            latest_message["message"]
        )

        latest_message = None

        return jsonify({
            "message": None
        })

    msg = latest_message["message"]

    latest_message = None

    return jsonify({
        "message": msg
    })