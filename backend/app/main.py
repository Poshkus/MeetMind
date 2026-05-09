from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
from pathlib import Path

app = FastAPI(title="MeetMind API")

UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save file temporarily
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Mock transcription result
    # In real app, would send to preprocessing + STT
    transcription = f"Mock transcription of {file.filename}: This is a sample transcript from the meeting."

    # Clean up
    try:
        os.remove(file_path)
    except Exception:
        pass

    return JSONResponse(content={"filename": file.filename, "transcription": transcription})

@app.get("/health")
async def health():
    return {"status": "ok"}