from flask import Flask, request
import requests

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    user_message = data["events"][0]["message"]["text"]

#If you send 'ON' via LINE, it will command the Pico W via HTTP.
    #<pico_IPはローカルIPに書き換え>
    
    if user_message.upper() == "ON":
        requests.post("http://<PICO_IP>/led/on")
    elif user_message.upper() == "OFF":
        requests.post("http://<PICO_IP>/led/off")

    return "OK"

#if __name__ == "__main__":   #開発用コードのためコメントアウト
#    app.run()