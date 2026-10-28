
import base64
import os
import re
import uuid
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "").strip()
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY", "").strip()
HEYGEN_AVATAR_ID = os.getenv("HEYGEN_AVATAR_ID", "").strip()
HEYGEN_VOICE_ID = os.getenv("HEYGEN_VOICE_ID", "").strip()
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

app = FastAPI(title="VoiceTwin AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500",
                   "http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
app.mount("/outputs", StaticFiles(directory=str(OUTPUTS)), name="outputs")


class Health(BaseModel):
    status: str
    sarvam_configured: bool
    heygen_configured: bool


@app.get("/api/health", response_model=Health)
def health():
    return Health(status="ok", sarvam_configured=bool(SARVAM_API_KEY),
                  heygen_configured=bool(HEYGEN_API_KEY and HEYGEN_AVATAR_ID and HEYGEN_VOICE_ID))


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-")
    return (cleaned or "voice")[:50]


@app.post("/api/generate/voice")
async def generate_voice(
    reference_audio: UploadFile = File(...),
    text: str = Form(...),
    language: str = Form("en-IN"),
    style: str = Form("conversational"),
    speed: float = Form(1.0),
    voice_name: str = Form("my-voice"),
):
    """Creates a saved Sarvam clone and synthesizes the requested text."""
    if not SARVAM_API_KEY:
        raise HTTPException(503, "SARVAM_API_KEY is missing. Copy .env.example to .env and add your key.")
    if not text.strip() or len(text) > 1000:
        raise HTTPException(400, "Text must contain 1–1000 characters.")
    if not 0.5 <= speed <= 2:
        raise HTTPException(400, "Speed must be between 0.5 and 2.0.")

    raw = await reference_audio.read()
    if not raw:
        raise HTTPException(400, "The reference audio file is empty.")
    if len(raw) > 50 * 1024 * 1024:
        raise HTTPException(413, "Reference audio must be 50 MB or smaller.")
    mime = reference_audio.content_type or "application/octet-stream"
    filename = Path(reference_audio.filename or "reference.wav").name

    headers = {"api-subscription-key": SARVAM_API_KEY}
    timeout = httpx.Timeout(180.0, connect=30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            create = await client.post(
                "https://api.sarvam.ai/voices/create",
                headers=headers,
                files={"file": (filename, raw, mime)},
                data={"name": safe_name(voice_name), "language": language, "style": style},
            )
            if create.is_error:
                raise HTTPException(create.status_code, f"Sarvam voice creation failed: {create.text[:700]}")
            created = create.json()
            voice_id = (created.get("data") or {}).get("voice_id")
            if not voice_id:
                raise HTTPException(502, f"Unexpected voice-create response: {str(created)[:500]}")

            generated = await client.post(
                "https://api.sarvam.ai/voices/clone",
                headers=headers,
                data={"voice_id": voice_id, "text": text.strip(),
                      "language_code": language, "pace": str(speed), "output_audio_codec": "wav"},
            )
            if generated.is_error:
                raise HTTPException(generated.status_code, f"Sarvam speech generation failed: {generated.text[:700]}")
            result = generated.json()
        except httpx.TimeoutException:
            raise HTTPException(504, "Sarvam timed out. Try a shorter script or retry.")
        except httpx.RequestError as exc:
            raise HTTPException(502, f"Could not reach Sarvam: {exc.__class__.__name__}")

    audio_b64 = result.get("audio_b64") or result.get("audio")
    if not audio_b64:
        raise HTTPException(502, "Sarvam response did not contain audio data.")
    try:
        audio_bytes = base64.b64decode(audio_b64)
    except Exception:
        raise HTTPException(502, "Could not decode audio returned by Sarvam.")

    out_name = f"{uuid.uuid4().hex}.wav"
    (OUTPUTS / out_name).write_bytes(audio_bytes)
    return {
        "status": "completed",
        "voice_id": voice_id,
        "audio_url": f"{PUBLIC_BASE_URL}/outputs/{out_name}",
        "audio_path": f"/outputs/{out_name}",
        "request_id": result.get("request_id"),
        "message": "Real voice-cloned audio generated by Sarvam AI."
    }


@app.post("/api/generate/avatar")
async def generate_avatar(
    portrait: UploadFile = File(...),
    audio_url: str = Form(""),
    text: str = Form(""),
):
    """Optional HeyGen integration. It uses a configured HeyGen avatar and voice.
    The portrait is accepted for frontend compatibility; existing HeyGen avatar IDs
    are used for generation. For custom photo-avatar workflows, use HeyGen's asset upload flow.
    """
    if not (HEYGEN_API_KEY and HEYGEN_AVATAR_ID and HEYGEN_VOICE_ID):
        raise HTTPException(
            503,
            "Avatar video is not configured. Add HEYGEN_API_KEY, HEYGEN_AVATAR_ID, and HEYGEN_VOICE_ID to .env. "
            "Sarvam voice generation works independently."
        )
    if not text.strip():
        raise HTTPException(400, "Enter the script text for avatar generation.")
    if len(text) > 5000:
        raise HTTPException(400, "Avatar script must be 5,000 characters or fewer.")

    payload = {
        "title": "VoiceTwin AI video",
        "video_inputs": [{
            "character": {"type": "avatar", "avatar_id": HEYGEN_AVATAR_ID, "avatar_style": "normal"},
            "voice": {"type": "text", "input_text": text.strip(), "voice_id": HEYGEN_VOICE_ID}
        }],
        "dimension": {"width": 1280, "height": 720},
    }
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=20.0)) as client:
        try:
            response = await client.post(
                "https://api.heygen.com/v2/video/generate",
                headers={"X-Api-Key": HEYGEN_API_KEY, "Content-Type": "application/json"},
                json=payload,
            )
        except httpx.RequestError as exc:
            raise HTTPException(502, f"Could not reach HeyGen: {exc.__class__.__name__}")
    if response.is_error:
        raise HTTPException(response.status_code, f"HeyGen video generation failed: {response.text[:700]}")
    data = response.json()
    video_id = data.get("data", {}).get("video_id") or data.get("video_id")
    return {
        "status": "queued",
        "job_id": video_id,
        "message": "HeyGen accepted the video job. Check status in HeyGen dashboard; this starter project does not yet poll video status."
    }


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    if not HEYGEN_API_KEY:
        raise HTTPException(503, "HEYGEN_API_KEY is not configured.")
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"https://api.heygen.com/v1/video_status.get",
            headers={"X-Api-Key": HEYGEN_API_KEY},
            params={"video_id": job_id},
        )
    if response.is_error:
        raise HTTPException(response.status_code, f"HeyGen status check failed: {response.text[:500]}")
    payload = response.json().get("data", response.json())
    status = payload.get("status", "processing")
    return {
        "status": "completed" if status == "completed" else ("failed" if status == "failed" else "processing"),
        "video_url": payload.get("video_url"),
        "message": payload.get("error") or status
    }
