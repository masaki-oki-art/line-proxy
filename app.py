import requests

def send_to_pico(message_text):
    pico_ip = "http://192.168.1.14"  # Pico WのIP
    payload = {
        "events": [
            {
                "message": {
                    "text": message_text
                }
            }
        ]
    }
    try:
        res = requests.post(pico_ip, json=payload, timeout=2)
        print("Pico response:", res.text)
    except Exception as e:
        print("Error sending to Pico:", e)
