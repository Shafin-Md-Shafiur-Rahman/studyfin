
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAR2UzO6fHMBPJVNZAPcObZAgNn8oV1BsD9rkNnD36dQFCZBCCdnJEtUcNbsV4Dla0RHmqf1sDWDGYunwZBdiQaqwPH1oY2naaH7xjA8blCBle3dnJzE6DNwoxXZCbYRyvRGE7yRA5UnBBwzsSLUoiIG880boOEI9OKlhwQPn89V4EX8cIhnWGSUdDgAZCx0UZAbZAR0AX6t06wK2aZAETcfBF2iuZCzw5l4CadGBcNz33CvLHrMZBZAIOxBQuvwEAZDZD"
PHONE_NUMBER_ID = "709386708930343"
VERIFY_TOKEN = "mysecrettoken"

def send_whatsapp_reply(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": text
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print("Send response:", response.status_code, response.text)

@app.route("/", methods=["GET"])
def home():
    return "StudyBot is live!"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        user_msg = message['text']['body'].strip()
        from_number = message['from']

        print(f"Incoming: {user_msg} from {from_number}")

        response_map = {
            "1": "🇫🇮 Apply via https://studyinfo.fi\n📚 আবেদন করতে হবে Studyinfo.fi ওয়েবসাইটে।",
            "2": "📝 Documents: Passport, certificates, IELTS, CV.\n📂 প্রয়োজনীয় ডকুমেন্ট: পাসপোর্ট, সার্টিফিকেট, IELTS, সিভি।",
            "3": "✅ Yes, IELTS 6.0+ is needed.\n✅ IELTS 6.0 বা তার বেশি দরকার।",
            "4": "💰 Tuition: €6,000–€13,000/year\n💵 টিউশন ফি বছরে প্রায় ৬০০০–১৩০০০ ইউরো।",
            "5": "🎓 Scholarships cover 50–100% tuition.\n🧾 অনেক স্কলারশিপ ৫০–১০০% ফি কাভার করে।"
        }

        reply_text = response_map.get(user_msg, 
            "👋 Welcome to StudyBot 🇫🇮\nPlease choose a topic:\n"
            "1. Apply Process\n2. Required Documents\n3. IELTS Requirement\n"
            "4. Tuition Fees\n5. Scholarships\n\nবাংলায় উত্তর পেতে উপরের নাম্বার লিখুন।"
        )

        send_whatsapp_reply(from_number, reply_text)

    except Exception as e:
        print("Error:", e)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
