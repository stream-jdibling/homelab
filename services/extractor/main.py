import os
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ExtractRequest(BaseModel):
    video_path: str
    job_id: str
    timestamps: list[float]

class ExtractResponse(BaseModel):
    frames: list[str]

@app.post("/extract", response_model=ExtractResponse)
def extract(req: ExtractRequest):
    if not os.path.exists(req.video_path):
        raise HTTPException(status_code=404, detail=f"Video file not found: {req.video_path}")

    frames_dir = f"/data/jobs/{req.job_id}/frames"
    os.makedirs(frames_dir, exist_ok=True)

    frames = []
    for ts in req.timestamps:
        frame_path = f"{frames_dir}/frame_{ts:.2f}.jpg"
        result = subprocess.run([
            "ffmpeg", "-y",
            "-ss", str(ts),
            "-i", req.video_path,
            "-frames:v", "1",
            "-q:v", "2",
            frame_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Frame extraction failed at {ts}s: {result.stderr}")

        frames.append(frame_path)

    return ExtractResponse(frames=frames)

@app.get("/health")
def health():
    return {"status": "ok"}