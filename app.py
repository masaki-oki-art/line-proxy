import time
import logging
import requests
from flask import Flask, request, jsonify

LINE_CHANNEL_ACCESS_TOKEN = "rrH3WhwKaEfMmKZonTs95+4OZIj1GxObEHCEugdrJUzDPRaNDigD3lPAQNbZojMgjA8Pd599qrRxl6cYLXVU8GWHQRmAudHAEvzT2juBRX2Cur1GFJ9MFINSdNJK/C1G8y6vqdjfpyFWaLg5kxM3hgdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "U885d15c80574144fd7628355631c480f"

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

latest_message = None
def send_line_push(text):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + LINE_CHANNEL_ACCESS_TOKEN
    }

    payload = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    try:
        res = requests.post(
            "https://api.line.me/v2/bot/message/push",
            json=payload,
            headers=headers,
            timeout=10
        )

        logging.info(
            "LINE Push status: %s",
            res.status_code
        )

    except Exception as e:
        logging.error(
            "LINE Push Error: %s",
            e
        )


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

    # line10分以上古いなら破棄
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



#↓line返送追加
@app.route("/pico_notify", methods=["POST"])
def pico_notify():

    data = request.get_json()

    logging.info("Pico Notify: %s", data)

    message = data.get("message")

    if message:
        send_line_push(message)

    return "OK", 200