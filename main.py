from flask import Flask, request
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from io import StringIO

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds_json = os.environ.get("GOOGLE_CREDS")
creds_dict = json.loads(creds_json)
creds_file = StringIO(json.dumps(creds_dict))

creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
client = gspread.authorize(creds)
sheet = client.open("WhatsApp Replies").messages

@app.route('/', methods=['GET'])
def verify():
    verify_token = "EAAUGNtMZA7RIBO53DLRb9KUFcZBSPQpZAkVQcfQmzNGp5nTFR0YlRiX8owZAvLpqxwa4OOMYZAgZBscyuR96QypLOOzZBrNx0QYk4UmvtGvKhHZBvGGULJqsZBZBb6m5GZCknwUfWMqUfBbdyr4XSl6aGIZCvIDExZCimE2vodLhNTKlKqRqer4ZCT0k3T5OYU8d72M4i8EUIBUlRoCZBokEZATnTDt5YwjGbL174sWZCq6EmdRnrdbKaZCZBRzd6Ob"
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
    try:
        messages = data['entry'][0]['changes'][0]['value']['messages']
        for msg in messages:
            phone = msg['from']
            message = msg['text']['body']
            msg_id = msg['id']
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([timestamp, phone, message, msg_id])
    except KeyError:
        pass

    # In production, you can add code here to forward to Google Sheets
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
