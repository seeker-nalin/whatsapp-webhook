from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    verify_token = "biozia_token"
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == verify_token:
        return challenge, 200
    else:
        return "Verification failed", 403

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print(f"Received data: {data}")
    # In production, you can add code here to forward to Google Sheets
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
