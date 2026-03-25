from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import re
from datetime import date, timedelta, datetime
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

# Load env
load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔑 ENV VARIABLES
MURF_API_KEY = os.getenv("MURF_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

MURF_TTS_URL = "https://api.murf.ai/v1/speech/generate"

# ✅ Safe Validation (DON'T CRASH APP)
if not MURF_API_KEY:
    print("⚠️ MURF_API_KEY missing")
if not TELEGRAM_TOKEN or not CHAT_ID:
    print("⚠️ Telegram config missing")

# 🔄 Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# ─────────────────────────────────────────────
# 🔔 TELEGRAM FUNCTION
# ─────────────────────────────────────────────

def send_telegram_message(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("⚠️ Telegram not configured")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        res = requests.post(url, json=payload)
        print("Telegram status:", res.status_code)
    except Exception as e:
        print("Telegram Error:", e)

# ─────────────────────────────────────────────
# 🧠 REMINDER PARSER
# ─────────────────────────────────────────────

def get_next_weekday(weekday_name: str) -> str:
    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    today = date.today()
    target = days.index(weekday_name.lower())
    days_ahead = (target - today.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    return (today + timedelta(days=days_ahead)).isoformat()

def parse_reminder(text: str) -> dict:
    t = text.lower().strip()

    task = re.sub(r"^(please\s+)?(remind me to|remind me|remember to|don't forget to|)\s*", "", t).strip()
    task = re.sub(r"\s+(at|every|in|on|tomorrow|today|tonight).*", "", task).strip() or task

    # ⏱ Delay
    delay_match = re.search(r"\bin\s+(\d+)\s*(minute|min|hour|hr)", t)
    if delay_match:
        mins = int(delay_match.group(1))
        if "hour" in delay_match.group(2):
            mins *= 60
        return {
            "task": task,
            "time": None,
            "date": None,
            "delay_minutes": mins
        }

    # 🕐 Time
    time_val = None
    time_match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)", t)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2) or 0)
        period = time_match.group(3)

        if period == "pm" and hour != 12:
            hour += 12
        if period == "am" and hour == 12:
            hour = 0

        time_val = f"{hour:02d}:{minute:02d}"

    # 📅 Date
    date_val = None
    today = date.today()

    if "tomorrow" in t:
        date_val = (today + timedelta(days=1)).isoformat()
    else:
        for d in ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
            if d in t:
                date_val = get_next_weekday(d)

    return {
        "task": task,
        "time": time_val,
        "date": date_val,
        "delay_minutes": None
    }

# ─────────────────────────────────────────────
# 🔊 MURF TTS
# ─────────────────────────────────────────────

def call_murf(text, voice_id="en-IN-isha"):
    if not MURF_API_KEY:
        return None

    headers = {
        "api-key": MURF_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voiceId": voice_id
    }

    try:
        response = requests.post(MURF_TTS_URL, headers=headers, json=payload)
        print("Murf status:", response.status_code)
        response.raise_for_status()
        return response.json().get("audioFile")
    except Exception as e:
        print("Murf Error:", e)
        return None

# ─────────────────────────────────────────────
# ⏰ SCHEDULER LOGIC
# ─────────────────────────────────────────────

def schedule_reminder(reminder):
    try:
        if reminder["delay_minutes"]:
            run_time = datetime.now() + timedelta(minutes=reminder["delay_minutes"])
        elif reminder["date"] and reminder["time"]:
            run_time = datetime.strptime(
                f"{reminder['date']} {reminder['time']}",
                "%Y-%m-%d %H:%M"
            )
        else:
            print("⚠️ No valid time → not scheduled")
            return

        scheduler.add_job(
            send_telegram_message,
            'date',
            run_date=run_time,
            args=[f"🔔 Reminder: {reminder['task']}"]
        )

        print("✅ Scheduled at:", run_time)

    except Exception as e:
        print("Scheduler Error:", e)

# ─────────────────────────────────────────────
# 🚀 ROUTES
# ─────────────────────────────────────────────

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    text = data.get("text")
    voice_id = data.get("voice_id", "en-IN-isha")

    reminder = parse_reminder(text)

    # 🔔 Schedule Telegram reminder
    schedule_reminder(reminder)

    spoken = f"Reminder set for {reminder['task']}"
    audio_url = call_murf(spoken, voice_id)

    return jsonify({
        "success": True,
        "reminder": reminder,
        "audio": {
            "spoken_text": spoken,
            "audio_url": audio_url
        }
    })

@app.route("/health")
def health():
    return {"status": "ok"}

# Serve frontend
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

# ─────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)