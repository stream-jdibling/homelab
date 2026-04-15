import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from faster_whisper import WhisperModel

app = FastAPI()

MODEL_NAME = os.getenv("WHISPER_MODEL", "large-v3-turbo")
model = WhisperModel(MODEL_NAME, device="cuda", compute_type="float16")

class TranscribeRequest(BaseModel):
    audio_path: str
    job_id: str

class TranscribeResponse(BaseModel):
    transcript_path: str

@app.post("/transcribe", response_model=TranscribeResponse)
def transcribe(req: TranscribeRequest):
    if not os.path.exists(req.audio_path):
        raise HTTPException(status_code=404, detail=f"Audio file not found: {req.audio_path}")

    segments, info = model.transcribe(req.audio_path, beam_size=5)

    transcript = {
        "job_id": req.job_id,
        "language": info.language,
        "language_probability": info.language_probability,
        "segments": [
            {
                "start": s.start,
                "end": s.end,
                "text": s.text.strip()
            }
            for s in segments
        ]
    }

    transcript_path = f"/data/jobs/{req.job_id}/transcript.json"
    with open(transcript_path, "w") as f:
        json.dump(transcript, f, indent=2)

    return TranscribeResponse(transcript_path=transcript_path)

@app.get("/health")
def health():
    return {"status": "ok"}