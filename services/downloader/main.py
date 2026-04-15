import os
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class DownloadRequest(BaseModel):
    url: str
    job_id: str

class DownloadResponse(BaseModel):
    audio_path: str
    video_path: str

@app.post("/download", response_model=DownloadResponse)
def download(req: DownloadRequest):
    job_dir = f"/data/jobs/{req.job_id}"
    audio_path = f"{job_dir}/audio.wav"
    video_path = f"{job_dir}/video.webm"

    os.makedirs(f"{job_dir}/frames", exist_ok=True)
    os.makedirs(f"{job_dir}/analysis", exist_ok=True)

    # Download audio
    result = subprocess.run([
        "yt-dlp", "-x",
        "--audio-format", "wav",
        "--audio-quality", "0",
        "-o", audio_path,
        req.url
    ], capture_output=True, text=True)

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Audio download failed: {result.stderr}")

    # Download video
    result = subprocess.run([
        "yt-dlp",
        "-o", video_path,
        req.url
    ], capture_output=True, text=True)

    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Video download failed: {result.stderr}")

    return DownloadResponse(audio_path=audio_path, video_path=video_path)

@app.get("/health")
def health():
    return {"status": "ok"}