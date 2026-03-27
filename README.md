# ⏰ Voice Reminder Assistant (Murf AI + Telegram Integration)

## 🎥 Demo Video

👉 Watch full demo here:
🔗 https://your-video-link-here

---

## 🚀 Overview

This project is a Voice-based Reminder Assistant that allows users to input reminders through a web interface.
The system intelligently parses the reminder, generates a voice response using Murf AI, and sends real-time notifications via Telegram at the scheduled time.

---

## 🎯 Key Features

* 🧠 Smart Reminder Parsing

  * Understands natural language inputs like:

    * “Remind me to drink water at 5 PM”
    * “Remind me in 10 minutes”

* 🔊 Voice Output (Murf AI)

  * Converts reminder confirmation into speech
  * Uses Murf AI Text-to-Speech API

* 🔔 Real-Time Telegram Notifications

  * Sends reminders directly to your Telegram chat and notification too
  * Works with exact scheduled timing

* ⏱ Scheduler Integration

  * Uses background scheduler to trigger reminders
  * Supports delay-based and time-based reminders

* 🌐 Web Interface

  * Simple and interactive UI
  * Displays parsed reminder + plays audio

---

## 🧩 System Architecture

User Input → Flask Backend → Reminder Parsing →
→ Murf AI (Voice Generation) → Scheduler → Telegram Bot → Notification

---

## 🛠️ Tech Stack

* Frontend: HTML, CSS, JavaScript
* Backend: Flask (Python)
* APIs:

  * Murf AI (Text-to-Speech)
  * Telegram Bot API
* Scheduler: APScheduler

---

## 🔐 Environment Setup (IMPORTANT)

### Step 1: Create a `.env` file in project root

### Step 2: Add the following:

MURF_API_KEY=your_murf_api_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

### ⚠️ Important Notes

* Never upload `.env` to GitHub
* Keep your API keys private

---

## 📄 `.gitignore` Setup

Create a file named `.gitignore` and add:

.env
**pycache**/
*.pyc

---

## ⚙️ Setup Instructions

### 1. Clone the Project

git clone <your-repo-link>
cd reminder-final

---

### 2. Install Dependencies

pip install -r requirements.txt

---

### 3. Run Backend

python app.py

---

### 4. Run Frontend

Open:

index.html

(or use Live Server)

---

## 🧪 Usage

1. Enter or speak a reminder 🎤
2. Click “Parse & Speak”
3. System will:

   * Parse reminder
   * Play voice response
   * Schedule notification
4. At the exact time → Telegram sends reminder 🔔

---

## 📡 API Endpoints

Method | Endpoint | Description
POST | /speak | Parse reminder + generate audio + schedule
GET | /health | Check server status

---

## 💡 Example Input

Remind me to drink water at 5 PM

---

## 📤 Example Output

* Voice: “Reminder set for drink water”
* Telegram:

🔔 Reminder: drink water

---

## ⚠️ Limitations

* Server must be running continuously
* Reminders are not stored (no database yet)
* Basic NLP (rule-based parsing)

---

## 🚀 Future Improvements

* 📦 Add database (SQLite / Firebase)
* 🔁 Recurring reminders
* ☁️ Deploy backend (Render / AWS)
  
---

## 🧠 Project Highlights

* Combines AI (TTS) + Real-time scheduling + messaging systems
* Demonstrates full-stack integration
* Suitable for hackathons / academic projects

---

## ⭐ Conclusion

This project showcases how modern applications can combine AI APIs + automation + messaging platforms to create intelligent and practical solutions for everyday use.
