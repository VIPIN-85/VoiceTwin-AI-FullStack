# ✨ VoiceTwin AI — Full-Stack Voice Studio

**VoiceTwin AI** is a full-stack AI voice application that allows users to generate speech using a voice sample. It combines a modern web interface with a Python FastAPI backend and cloud-based AI services.

The project integrates **Sarvam AI** for voice cloning and speech generation, with optional **HeyGen** integration for talking-avatar video generation.

## 🚀 Features

- 🎙️ **AI Voice Cloning** — Generate speech using an authorized reference voice recording.
- 🗣️ **Multilingual Speech** — Choose from supported Indian languages, including English, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, and Assamese.
- ✍️ **Custom Text-to-Speech** — Enter your own script and generate spoken audio.
- 🎚️ **Voice Controls** — Configure speaking style, language, and speech speed.
- 🔊 **Audio Playback** — Listen to generated audio directly in your browser.
- 📥 **Audio Download** — Download generated speech as a WAV file.
- 🧑‍💻 **Optional Talking Avatar** — Integrate HeyGen for avatar video generation.
- ⚡ **FastAPI Backend** — Connect the frontend to external AI services through a Python API.
- 🔐 **Environment-Based Configuration** — Keep API credentials on the backend instead of exposing them in frontend JavaScript.
- 🎨 **Modern Web Interface** — A clean, responsive voice-generation studio.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| HTML5 | Application structure |
| CSS3 | Styling and responsive interface |
| JavaScript | Frontend interactions |
| Python | Backend development |
| FastAPI | REST API |
| Uvicorn | Development server |
| Sarvam AI | Voice cloning and speech generation |
| HeyGen | Optional avatar video generation |
| HTTPX | Requests to external APIs |

## 📁 Project Structure

```text
VoiceTwin-AI-FullStack/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   └── outputs/
│       └── .gitkeep
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```

## ⚙️ Prerequisites

Before running the project, install:

- Python 3.10 or newer
- A modern web browser
- An internet connection
- A Sarvam AI API key
- Optional: a HeyGen API key and valid avatar and voice IDs

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/VoiceTwin-AI-FullStack.git
cd VoiceTwin-AI-FullStack
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Set up the backend

Open a terminal in the project directory:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example configuration file:

```powershell
Copy-Item .env.example .env
```

Open `backend/.env` and add your Sarvam AI API key:

```env
SARVAM_API_KEY=your_sarvam_api_key
HEYGEN_API_KEY=
HEYGEN_AVATAR_ID=
HEYGEN_VOICE_ID=
PUBLIC_BASE_URL=http://127.0.0.1:8000
```

Obtain a Sarvam API key from the [Sarvam AI Dashboard](https://dashboard.sarvam.ai/).

For optional avatar generation, configure the appropriate HeyGen credentials.

**Security:** Never commit your actual `.env` file or publish API keys.

### 4. Start the backend server

From the `backend` directory, run:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The backend will run at:

`http://127.0.0.1:8000`

Interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

### 5. Start the frontend

Open a second terminal in the project root:

```bash
cd frontend
python -m http.server 5500
```

Open the application in your browser:

`http://127.0.0.1:5500`

Keep both servers running while using the application.

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check backend and provider configuration |
| POST | `/api/generate/voice` | Generate speech using a reference voice |
| POST | `/api/generate/avatar` | Request talking-avatar video generation |
| GET | `/api/jobs/{job_id}` | Check the status of an avatar-generation job |

The avatar endpoints require appropriate HeyGen configuration. Voice generation requires a valid Sarvam API key and an account with the necessary API access.

## 🔄 How It Works

1. Start the frontend and backend servers.
2. Upload a clean reference recording of a voice you own or have permission to use.
3. Enter the text you want to generate.
4. Select a language, speaking style, and speech speed.
5. Submit the request to the FastAPI backend.
6. The backend communicates with Sarvam AI to create the voice and generate speech.
7. Listen to the generated audio and download the resulting WAV file.

The optional avatar workflow uses HeyGen's configured avatar and voice to request a video-generation job.

## 🔒 Security and Responsible Use

- Clone only your own voice or a voice you have explicit permission to use.
- Never expose API keys in client-side code or public repositories.
- Keep `.env` files and generated private recordings out of version control.
- Use HTTPS, authentication, request limits, and appropriate access controls before public deployment.
- Review the privacy policies, usage requirements, and pricing of the external AI providers.
- Delete generated audio files when they are no longer needed.

## ⚠️ Important Notes

- Voice cloning and avatar generation depend on external cloud APIs and valid credentials.
- Some provider features may require paid credits or specific account permissions.
- The optional avatar integration uses configured HeyGen avatar and voice IDs; uploading a portrait does not currently create a custom avatar automatically.
- This project is a development starter and requires additional security and deployment configuration before production use.

## 🗺️ Future Improvements

Potential future enhancements include:

- User authentication and personalized voice libraries
- Voice-generation history and improved file management
- Background job processing and generation progress indicators
- Production deployment with HTTPS
- Improved error handling, usage limits, and monitoring
- Expanded voice and avatar customization

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork this repository.
2. Create a feature branch.
3. Make and test your changes.
4. Submit a pull request with a clear description.

## 📄 License

No license has been specified yet. Add a suitable open-source license before permitting others to reuse, modify, or distribute this project.

---

**Built with Python, FastAPI, JavaScript, and AI-powered voice technology.**
