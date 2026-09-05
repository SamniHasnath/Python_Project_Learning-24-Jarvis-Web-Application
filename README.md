# 🤖 Jarvis Web - Personal AI Voice Assistant

A browser-based **Jarvis-style AI voice assistant** built with **FastAPI, JavaScript, and the Web Speech API**.

Jarvis Web allows users to interact with an intelligent assistant using **voice or text directly from a web browser**. Speech recognition and text-to-speech run entirely in the browser, while the backend handles command processing, external APIs, and optional OpenAI-powered responses.

🔗 **Live Demo:** https://jarvisweb-ryua.onrender.com

> ⏳ **Note:** The live demo is hosted on Render's free tier. If the service has been inactive, it may take approximately **30–60 seconds** to wake up.
---
## 📸 Preview

![Jarvis Web Preview](https://github.com/user-attachments/assets/5df6f701-b028-41d1-9719-5f4350201ed2)

---

# ✨ Features

## 🎙️ Voice Interaction

Talk naturally with Jarvis using your microphone.

* Browser-based speech recognition
* No desktop application required
* Works best with Chrome and Edge
* Voice commands are converted into text automatically

---

## 🔊 Text-to-Speech

Jarvis can speak its responses aloud.

* Uses the browser's Speech Synthesis API
* No server-side audio processing required
* Responses can be heard directly through the device

---

## ⌨️ Text Chat

Voice input isn't always available, so Jarvis also provides a text-based interface.

You can simply type a command and receive a response.

---

# 🧠 Intelligent Command System

Jarvis recognizes different types of commands and routes them to the appropriate functionality.

### 🌦️ Weather

Ask questions such as:

```text
What's the weather in Tokyo?
```

Jarvis retrieves weather information and returns the result.

---

### 📰 News

Get the latest headlines from BBC News.

Example:

```text
What's the latest news?
```

---

### 😂 Jokes

Ask Jarvis for a random joke.

```text
Tell me a joke
```

---

### 💬 Motivational Quotes

Get an inspirational quote whenever you need motivation.

```text
Give me a motivational quote
```

---

### 📖 Wikipedia

Jarvis can provide Wikipedia-based summaries.

Examples:

```text
Who is Albert Einstein?
```

```text
What is artificial intelligence?
```

---

### 🔍 Google Search

Jarvis can open Google search results automatically.

Example:

```text
Search Google for Python tutorials
```

The results open in a new browser tab.

---

### ▶️ YouTube Search

Search for YouTube videos using voice commands.

Example:

```text
Search YouTube for JavaScript tutorials
```

---

### 🌐 Open Websites

Jarvis can open websites directly.

Example:

```text
Open github.com
```

---

### 🎵 Music Player

Jarvis can play local audio files stored inside:

```text
static/music/
```

Supported formats include:

```text
.mp3
.wav
.ogg
```

Example:

```text
Play music
```

---

### ⏱️ Voice Timers

Create timers using natural language.

Example:

```text
Set a timer for 5 minutes
```

When the timer finishes, Jarvis provides an alert and spoken notification.

---

### 🪙 Coin Flip

Ask Jarvis to randomly flip a coin.

```text
Flip a coin
```

---

### 🎲 Dice Roll

Roll a random dice value.

```text
Roll a dice
```

---

### 🕒 Time & Date

Jarvis can provide the current time and date.

Examples:

```text
What time is it?
```

```text
What's today's date?
```

> ⚠️ These values are based on the **server's timezone**, not necessarily the user's local timezone.

---

# 🤖 OpenAI AI Fallback

If Jarvis doesn't recognize a command, it can send the request to **OpenAI** as a fallback.

For example:

```text
Explain recursion in simple terms
```

Instead of requiring a predefined command, Jarvis can use the AI model to generate a response.

### Optional Configuration

OpenAI integration requires an API key.

```env
OPENAI_API_KEY=your_api_key_here
```

The application can still run without an OpenAI API key, but AI fallback functionality will not be available.

---

# 🏗️ System Architecture

Jarvis Web separates browser functionality from backend functionality.

```text
                    ┌──────────────────────┐
                    │      User Browser    │
                    │                      │
                    │  Voice / Text Input  │
                    │         │            │
                    │         ▼            │
                    │  Web Speech API      │
                    │         │            │
                    │         ▼            │
                    │    JavaScript UI     │
                    └──────────┬───────────┘
                               │
                               │ HTTP Request
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │      Backend         │
                    │                      │
                    │  Command Routing     │
                    │  Weather             │
                    │  News                │
                    │  Wikipedia           │
                    │  Jokes               │
                    │  Quotes              │
                    │  Random Tools        │
                    │  OpenAI Fallback     │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
          External APIs      OpenAI       Application
                                          Services
```

---

# 🌐 Browser vs Backend Responsibilities

Because a server doesn't have access to the user's microphone, speakers, desktop applications, or screen, functionality is divided between the browser and server.

## Browser

The browser handles:

* 🎙️ Speech recognition
* 🔊 Text-to-speech
* ⌨️ Text input
* 🌐 Opening websites
* 🔍 Google searches
* ▶️ YouTube searches
* 🎵 Local music playback
* ⏱️ Timers
* User interface interactions

---

## Backend

FastAPI handles:

* Command routing
* Weather requests
* News retrieval
* Jokes
* Motivational quotes
* Wikipedia summaries
* Coin flips
* Dice rolls
* OpenAI fallback
* API endpoints

---

# 🆚 Jarvis Web vs Desktop Jarvis

This project is designed as the web-based version of the original desktop/terminal Jarvis assistant.

The original project remains untouched.

### Desktop Version

The desktop version can interact with the local machine.

### Web Version

The browser version focuses on functionality that can safely operate through a web browser.

### Removed from the Web Version

The following desktop-specific functionality was removed:

* Opening desktop applications
* Screenshots
* Battery information
* CPU information
* RAM information
* Local IP information
* Direct desktop control

These features would provide information about the **server**, rather than the user's own computer.

---

# 🛠️ Technology Stack

## Frontend

* HTML5
* CSS3
* JavaScript
* Web Speech API
* Speech Synthesis API

## Backend

* Python
* FastAPI
* Uvicorn

## AI

* OpenAI API

## External Services

* Weather API
* BBC News
* Wikipedia

## Deployment

* Docker
* Render

---

# 📂 Project Structure

```text
jarvis-web/
│
├── app/
│   ├── main.py
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   ├── music/
│   └── ...
│
├── templates/
│   └── index.html
│
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 🚀 Run Locally

## 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Navigate into the project:

```bash
cd jarvis-web
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Copy the example environment file.

### Windows

```bash
copy .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

Then add your OpenAI API key if you want AI fallback functionality:

```env
OPENAI_API_KEY=your_api_key_here
```

> 🔐 Never commit your `.env` file or API keys to GitHub.

---

## 5. Start the Application

Run:

```bash
uvicorn app.main:app --reload --port 8000
```

Then open:

```text
http://localhost:8000
```

---

# 🎙️ Using Voice Input

For microphone functionality, use a browser with Web Speech API support.

Recommended browsers:

* Google Chrome
* Microsoft Edge

When prompted, allow microphone access.

If voice recognition isn't available, use the text input instead.

---

# 📚 FastAPI Documentation

FastAPI automatically provides interactive API documentation.

Once the application is running, visit:

```text
http://localhost:8000/docs
```

You can use the documentation to:

* View available endpoints
* Test API requests
* Inspect request parameters
* Inspect API responses

---

# 🎵 Adding Music

To enable local music playback, place audio files inside:

```text
static/music/
```

Example:

```text
static/
└── music/
    ├── song1.mp3
    ├── song2.wav
    └── song3.ogg
```

Supported formats:

```text
MP3
WAV
OGG
```

---

# 🐳 Run with Docker

Docker allows Jarvis Web to run inside a container without manually configuring the Python environment.

## Build the Image

```bash
docker build -t jarvis-web .
```

## Run the Container

```bash
docker run -p 8000:8000 --env-file .env jarvis-web
```

Then open:

```text
http://localhost:8000
```

---

# ☁️ Deploy to Render

Jarvis Web can be deployed using Docker on Render.

## Step 1 — Push to GitHub

Push the project to a GitHub repository.

## Step 2 — Create a Render Web Service

Go to Render and create:

```text
New → Web Service
```

Connect your GitHub repository.

## Step 3 — Select Docker

Render should detect the project's:

```text
Dockerfile
```

Select Docker as the environment.

No separate build or start command is required when using the Docker configuration.

## Step 4 — Add Environment Variables

In Render's environment settings, add:

```env
OPENAI_API_KEY=your_api_key_here
```

This is optional.

## Step 5 — Deploy

Start the deployment and Render will:

```text
GitHub
   ↓
Render
   ↓
Docker Build
   ↓
Container
   ↓
FastAPI
   ↓
Public HTTPS URL
```

---

# 🔐 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Example environment template:

```env
OPENAI_API_KEY=
```

Keep secrets out of source control.

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
```

---

# 🔄 How a Voice Command Works

For example, the user says:

```text
What's the weather in Tokyo?
```

The flow is:

```text
🎙️ User speaks
       ↓
🧠 Browser Speech Recognition
       ↓
📝 Speech converted to text
       ↓
🌐 Request sent to FastAPI
       ↓
🔀 Command Router
       ↓
🌦️ Weather Service
       ↓
📦 Response returned
       ↓
🖥️ Browser displays response
       ↓
🔊 Speech Synthesis reads response
```

---

# 🧠 AI Fallback Flow

When a command isn't recognized:

```text
User Question
      ↓
Command Router
      ↓
Known Command?
   ↙       ↘
 YES       NO
  ↓         ↓
Execute   OpenAI
Command   API
            ↓
        AI Response
            ↓
        Browser UI
            ↓
       Text-to-Speech
```

---

# 📡 API

The FastAPI backend exposes endpoints for browser communication.

You can inspect and test all available endpoints using:

```text
/docs
```

FastAPI's interactive Swagger documentation makes it easy to understand the API without using an additional API client.

---

# 🧪 Testing

You can test the application using:

### Browser

Test:

* Voice input
* Text input
* Spoken responses
* Website opening
* Google search
* YouTube search
* Timers
* Music playback

### FastAPI Swagger UI

Open:

```text
http://localhost:8000/docs
```

### Docker

Verify that the application works inside the container:

```bash
docker build -t jarvis-web .
docker run -p 8000:8000 --env-file .env jarvis-web
```

---

# 🛡️ Security Considerations

This project should not expose API keys directly in frontend JavaScript.

Sensitive credentials should be stored using environment variables:

```env
OPENAI_API_KEY=...
```

Do not commit:

```text
.env
```

to GitHub.

For production deployments, additional protections such as authentication, rate limiting, validation, logging, and secure secret management should be considered.

---

# 🚧 Current Limitations

* Web Speech API support varies between browsers.
* Microphone permissions are required for voice interaction.
* OpenAI fallback requires an API key.
* Render free-tier deployments can experience cold starts.
* Server-side time/date values depend on the server timezone.
* Local music files are tied to the deployed filesystem.
* Browser security restrictions can affect some web-opening behavior.

---

# 🔮 Future Improvements

Possible future enhancements include:

* 🌍 User timezone detection
* 👤 User authentication
* 💾 Conversation history
* 🧠 Persistent AI memory
* 🎤 Improved voice recognition
* 🗣️ Multiple voice options
* 🌐 Multi-language support
* 📱 Better mobile UI
* 🎨 Custom Jarvis themes
* 🔐 Authentication and authorization
* 🗄️ Database integration
* 📊 Usage analytics
* ⚡ WebSocket-based real-time communication
* 🤖 AI-powered task planning
* 🧩 Plugin/tool architecture
* 📁 User-uploaded knowledge sources
* 🔎 RAG-based question answering

---

# 🎯 Learning Objectives

This project demonstrates practical concepts including:

* Building REST APIs with FastAPI
* Connecting frontend and backend applications
* JavaScript browser APIs
* Speech recognition
* Text-to-speech
* API integration
* AI API integration
* Environment variables
* Command routing
* Docker containerization
* Cloud deployment
* GitHub-based development
* Handling browser/server responsibilities
* Designing an AI assistant architecture

---

# 💡 Why This Project?

Jarvis Web combines several modern software engineering concepts into a single project.

Instead of building only a simple chatbot, this project demonstrates how a real application can combine:

```text
Frontend
   +
Backend
   +
External APIs
   +
Browser APIs
   +
AI
   +
Docker
   +
Cloud Deployment
```

This makes it a useful project for learning **full-stack development, API development, AI integration, and deployment**.

---

# 👨‍💻 Original Desktop Version

Jarvis Web is the browser-based companion to the original:

```text
jarvis-assistant/
```

The desktop version is kept separate and remains untouched.

---

# 📌 Project Status

🟢 **Working**

The application currently supports:

* Voice interaction
* Text interaction
* Weather
* News
* Jokes
* Motivational quotes
* Wikipedia
* Google search
* YouTube search
* Website opening
* Music playback
* Timers
* Coin flip
* Dice roll
* Time/date
* Optional OpenAI fallback
* Docker deployment
* Render deployment

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 👤 Author

**Samni Hasnath**

Software Engineering Undergraduate

🔗 GitHub: [SamniHasnath](https://github.com/SamniHasnath)

🔗 LinkedIn: [Samni Hasnath](https://linkedin.com/in/samni-hasnath03)

---

# 🚀 Quick Start

For experienced users, the entire local setup can be summarized as:

```bash
git clone <your-repository-url>
cd jarvis-web

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env

uvicorn app.main:app --reload --port 8000
```

Then open:

```text
http://localhost:8000
```

🎙️ **Allow microphone access and start talking to Jarvis!**
