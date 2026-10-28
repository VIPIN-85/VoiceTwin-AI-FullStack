# VoiceTwin AI — Windows full-stack starter

This project contains a browser frontend and a Python FastAPI backend. **Real voice cloning is integrated with Sarvam AI's hosted Instant Voice Cloning API.** No local AI model is needed for this feature; the provider performs inference in its cloud.

## Requirements
- Windows 10/11
- Python 3.10 or newer (3.11 recommended)
- Internet connection
- Sarvam account and API key
- A clean 10–15 second audio sample of a voice you own or have permission to clone

## Quick start (Windows)

1. Install Python from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Extract this ZIP to a folder such as `C:\VoiceTwin-AI`.
3. Open Command Prompt and run:

```bat
cd C:\VoiceTwin-AI\backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
notepad .env
```

4. In the `.env` file, replace `put_your_sarvam_api_key_here` with your Sarvam API key. Save and close Notepad.
5. Start the backend:

```bat
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

6. Open a second Command Prompt, go to the extracted `frontend` folder, and run:

```bat
cd C:\VoiceTwin-AI\frontend
python -m http.server 5500
```

7. Open http://127.0.0.1:5500 in your browser. The status should say the backend is connected and Sarvam configured.

## Get a Sarvam API key
- Create/sign into an account at https://dashboard.sarvam.ai/
- Open Key Management and create a key.
- Add it only to `backend\.env`; do not place it in frontend JavaScript or commit it to Git.
- Voice cloning docs: https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview

## What the real integration does
- `POST /api/generate/voice`: accepts the uploaded reference recording and text, calls Sarvam's `POST /voices/create`, then `POST /voices/clone`, decodes the returned WAV audio, and returns a local playback URL.
- `GET /api/health`: reports whether provider keys are configured.
- `POST /api/generate/avatar`: optional HeyGen integration (details below).
- `GET /api/jobs/{job_id}`: checks the HeyGen job status.

Sarvam's voice-cloning API is currently documented as beta. The reference audio for direct inline generation is limited to 10 MB and 15 seconds; saved voice creation accepts up to 50 MB. Text generation accepts 1–1000 characters per request. A free plan keeps up to 5 cloned voices. Pricing/credits may change: check the current Sarvam dashboard and pricing before production use. API errors (including insufficient credits or account-tier limits) are shown in the frontend status area.

## Optional HeyGen avatar video
Avatar video is separate from Sarvam voice cloning and may require paid HeyGen API credits. To enable it:
1. Get an API key from https://developers.heygen.com/.
2. Obtain a valid `avatar_id` and `voice_id` from your HeyGen account.
3. Add `HEYGEN_API_KEY`, `HEYGEN_AVATAR_ID`, and `HEYGEN_VOICE_ID` to `.env`.
4. Restart Uvicorn.

The starter avatar endpoint generates a HeyGen video from script text using the configured HeyGen avatar and voice. It accepts the portrait field for frontend compatibility but does not yet upload/use that portrait as a custom avatar. It returns a job ID; status checks use HeyGen's status API. A public HTTPS deployment and additional asset-upload work are required for a production custom-photo workflow.

## What is NOT installed locally
No voice-cloning model files, GPU, CUDA, or local speech model installation is required for Sarvam or HeyGen: they are hosted APIs. The FastAPI server is a thin secure bridge. The browser animation is decorative only; generated audio is real provider output.

## Security and production notes
- Never expose API keys in frontend files.
- Do not deploy the development server with `--reload` to the public internet.
- Add authentication, rate limits, per-user quotas, storage cleanup, and HTTPS before public deployment.
- Get explicit permission before cloning or animating anyone's voice or likeness.
- Audio files are written to `backend/outputs/`. Delete these files when no longer needed.
- The development CORS policy allows only localhost frontend origins. Update it intentionally if deploying the frontend elsewhere.
