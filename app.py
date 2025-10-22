@app.route("/notify", methods=["POST"])
def callback():
    data = request.get_json()
    logging.info("Raw data: %s", data)

    try:
        if "events" in data:
            event = data["events"][0]
            if event["type"] == "message" and "text" in event["message"]:
                message = event["message"]["text"]
                logging.info("LINE message: %s", message)

                pico_url = "http://133.207.116.194:7072"
                res = requests.post(pico_url, json=data, timeout=30)
                logging.info("Pico response: %s", res.status_code)

                if res.status_code == 200:
                    send_line_message("Picoが正常に受信しました（200 OK）")
        else:
            logging.info("LINE形式ではないPOSTを受信しました")
    except Exception as e:
        logging.error("Error parsing message: %s", e)

    return "OK", 200

@app.route("/line-notify", methods=["POST"])
def line_notify():
    data = request.get_json()
    logging.info("LINE通知受信: %s", data)
    return "OK", 200