const BACKEND_URL = "http://localhost:5000";

async function processReminder() {
  const input = document.getElementById('userInput').value.trim();
  if (!input) {
    document.getElementById('userInput').focus();
    return;
  }

  const voiceId = document.getElementById('voiceSelect').value;

  // Reset UI
  document.getElementById('result').classList.add('hidden');
  document.getElementById('error').classList.add('hidden');
  document.getElementById('loading').classList.remove('hidden');

  try {
    const response = await fetch(`${BACKEND_URL}/speak`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: input, voice_id: voiceId })
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(data.error || 'Server error');
    }

    renderResult(data);

  } catch (e) {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('errorMsg').textContent = `⚠️ ${e.message}`;
    document.getElementById('error').classList.remove('hidden');
    console.error(e);
  }
}

function renderResult(data) {
  document.getElementById('loading').classList.add('hidden');

  const reminder = data.reminder;
  const audio = data.audio;

  // Audio player
  document.getElementById('spokenText').textContent = `🗣️ "${audio.spoken_text}"`;
  const audioEl = document.getElementById('audioEl');
  audioEl.src = audio.audio_url;
  audioEl.load();
  // Auto-play
  audioEl.play().catch(() => {});

  // Cards
  const fields = [
    { label: '🎯 Task', value: reminder.task },
    { label: '🕐 Time', value: reminder.time },
    { label: '📅 Date', value: reminder.date },
    { label: '🔁 Recurrence', value: reminder.recurrence },
    { label: '⏱ Delay (mins)', value: reminder.delay_minutes }
  ];

  document.getElementById('cards').innerHTML = fields.map(f => `
    <div class="card">
      <div class="card-label">${f.label}</div>
      <div class="card-value ${f.value === null || f.value === undefined ? 'null-val' : ''}">
        ${f.value !== null && f.value !== undefined ? f.value : 'null'}
      </div>
    </div>
  `).join('');

  document.getElementById('jsonOutput').textContent = JSON.stringify(reminder, null, 2);
  document.getElementById('result').classList.remove('hidden');
}

function copyJSON() {
  const text = document.getElementById('jsonOutput').textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector('.copy-btn');
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy JSON', 1500);
  });
}

function fillExample(text) {
  document.getElementById('userInput').value = text;
  document.getElementById('userInput').focus();
}

// Ctrl+Enter to submit
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('userInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) processReminder();
  });
});
// 🎤 Voice Input Feature
document.addEventListener("DOMContentLoaded", () => {
  const micBtn = document.getElementById("micBtn");

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    micBtn.textContent = "❌ Voice not supported";
    micBtn.disabled = true;
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";

  micBtn.addEventListener("click", () => {
    micBtn.textContent = "🎙 Listening...";
    recognition.start();
  });

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;

    // Put text into input box
    document.getElementById("userInput").value = transcript;

    micBtn.textContent = "🎤 Speak";

    // Auto process
    processReminder();
  };

  recognition.onerror = function () {
    micBtn.textContent = "🎤 Speak";
    alert("Voice recognition error. Try again.");
  };

  recognition.onend = function () {
    micBtn.textContent = "🎤 Speak";
  };
});
