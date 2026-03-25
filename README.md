# ⏰ Voice Reminder Assistant (Murf AI Only — No Anthropic)

## 📁 Project Structure
```
reminder-final/
├── app.py           → Flask backend (rule-based parser + Murf TTS)
├── index.html       → Frontend UI
├── app.js           → Frontend JS (calls Flask backend)
├── style.css        → Dark theme styles
├── .env             → Your Murf API key
└── requirements.txt → Python dependencies
```

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your Murf API key in `.env`
```
MURF_API_KEY=your_murf_api_key_here
```

### 3. Start Flask backend
```bash
python app.py
```
Backend runs at: `http://localhost:5000`

### 4. Open the frontend
Open `index.html` in your browser (or serve with Live Server).

---

## 📡 API Endpoints

| Method | Endpoint          | Description                        |
|--------|-------------------|------------------------------------|
| POST   | `/speak`          | ⭐ Parse reminder + generate audio  |
| POST   | `/parse-reminder` | Parse only → JSON (no audio)       |
| GET    | `/voices`         | List all Murf voice IDs            |
| GET    | `/health`         | Health check                       |

### POST `/speak` — Example
**Request:**
```json
{ "text": "Remind me to drink water at 5 PM every day", "voice_id": "en-US-natalie" }
```
**Response:**
```json
{
  "success": true,
  "reminder": {
    "task": "drink water",
    "time": "05:00 PM",
    "date": null,
    "recurrence": "daily",
    "delay_minutes": null,
    "original_text": "Remind me to drink water at 5 PM every day"
  },
  "audio": {
    "spoken_text": "Reminder: drink water, at 05:00 PM, repeating daily.",
    "audio_url": "https://...",
    "duration_secs": 3.2,
    "voice_id": "en-US-natalie"
  }
}
```

---

## ✅ What Changed vs Old Project
| Old | New |
|-----|-----|
| Used Anthropic Claude API (paid) | ❌ Removed — not needed |
| Frontend called Anthropic directly (exposed key!) | ✅ Frontend calls Flask backend |
| No audio playback in UI | ✅ Audio player with autoplay |
| No voice selector | ✅ Voice dropdown added |
| `anthropic` in requirements | ✅ Removed |

---

## 🎙️ Available Voice IDs
| Voice ID        | Description      |
|-----------------|------------------|
| en-US-natalie   | US Female        |
| en-US-marcus    | US Male          |
| en-UK-ruby      | UK Female        |
| en-IN-isha      | Indian Female    |
| en-IN-arjun     | Indian Male      |
