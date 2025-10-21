from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# LINE通知関数
def send_line(text):
    payload = {"message": text}
    headers = {"Host": "line-proxy-dkvy.onrender.com"}

    try:
        res = requests.post("https://line-proxy-dkvy.onrender.com/notify", json=payload, headers=headers, timeout=5)
        print("LINE通知ステータス:", res.status_code)
    except Exception as e:
        print("LINE通知エラー:", e)

# Pico Wへの送信処理
def send_to_pico(message):
    try:
        res = requests.post("http://192.168.1.16:80", json={"message": message}, timeout=5)
        print("Pico W応答ステータス:", res.status_code)
        return res.status_code == 200
    except Exception as e:
        print("Pico W送信エラー:", e)
        return False

# LINEからのメッセージ受信エンドポイント
@app.route("/notify", methods=["POST"])
def notify():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        print("LINE message:", message)

        # Pico Wへ送信
        success = send_to_pico(message)

        # 成否に応じてLINE通知
        if success:
            send_line("送信OK")
        else:
            send_line("送信NG")

        return jsonify({"status": "done"}), 200

    except Exception as e:
        print("全体処理エラー:", e)
        send_line("送信NG")
        return jsonify({"status": "error"}), 500

# ヘルスチェック用
@app.route("/", methods=["GET", "HEAD"])
def index():
    return "Flask is running", 200