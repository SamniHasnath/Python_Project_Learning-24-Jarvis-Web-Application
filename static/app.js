const transcriptEl = document.getElementById("transcript");
const micBtn       = document.getElementById("micBtn");
const textForm     = document.getElementById("textForm");
const textInput    = document.getElementById("textInput");
const statusEl     = document.getElementById("status");
const player       = document.getElementById("player");

const SpeechRecognitionImpl = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let listening = false;

function addMessage(text, who) {
  const div = document.createElement("div");
  div.className = `msg ${who}`;
  div.textContent = text;
  transcriptEl.appendChild(div);
  transcriptEl.scrollTop = transcriptEl.scrollHeight;
}

function speak(text) {
  if (!("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  window.speechSynthesis.speak(utterance);
}

function setStatus(text) {
  statusEl.textContent = text;
}

function handleAction(action) {
  if (!action) return;

  switch (action.type) {
    case "open_url":
      window.open(action.url, "_blank");
      break;

    case "play_audio":
      player.src = action.url;
      player.play().catch(() => {});
      break;

    case "stop_audio":
      player.pause();
      break;

    case "set_timer":
      setStatus(`Timer running: ${action.label}...`);
      setTimeout(() => {
        const msg = `Timer done! ${action.label} are up!`;
        addMessage(msg, "assistant");
        speak(msg);
        setStatus("");
      }, action.seconds * 1000);
      break;

    case "end_session":
      if (recognition && listening) recognition.stop();
      break;
  }
}

async function sendCommand(text) {
  if (!text.trim()) return;
  addMessage(text, "user");

  try {
    const resp = await fetch("/api/command", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await resp.json();
    addMessage(data.reply, "assistant");
    speak(data.reply);
    handleAction(data.action);
  } catch (err) {
    addMessage("Sorry, I couldn't reach the server.", "assistant");
  }
}

// ── text input ─────────────────────────────────────────────────────────────

textForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = textInput.value;
  textInput.value = "";
  sendCommand(text);
});

// ── voice input (Web Speech API) ──────────────────────────────────────────────

if (SpeechRecognitionImpl) {
  recognition = new SpeechRecognitionImpl();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    listening = true;
    micBtn.textContent = "🎙️ Listening...";
    micBtn.classList.add("listening");
    setStatus("Listening...");
  };

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    sendCommand(text);
  };

  recognition.onerror = (event) => {
    setStatus(`Mic error: ${event.error}`);
  };

  recognition.onend = () => {
    listening = false;
    micBtn.textContent = "🎤 Start Listening";
    micBtn.classList.remove("listening");
    setStatus("");
  };

  micBtn.addEventListener("click", () => {
    if (listening) {
      recognition.stop();
    } else {
      recognition.start();
    }
  });
} else {
  micBtn.disabled = true;
  micBtn.textContent = "🎤 Mic not supported in this browser";
  setStatus("Try Chrome or Edge for voice input, or use the text box below.");
}

// ── greet on load ──────────────────────────────────────────────────────────

(async function init() {
  try {
    const resp = await fetch("/api/greet");
    const data = await resp.json();
    addMessage(data.reply, "assistant");
    speak(data.reply);
  } catch (err) {
    addMessage("Hello! (Couldn't reach the server for a proper greeting.)", "assistant");
  }
})();
