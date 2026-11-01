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
                latest_message = event["message"]["text"]

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

    msg = latest_message
    latest_message = None

    return jsonify({
        "message": msg
    })