from uuid import uuid4
from pathlib import Path
import os
import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="MeetMind API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_UPLOAD_BYTES = 1 * 1024 * 1024 * 1024  # 1 GB

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed_types = {
        "audio/mpeg",
        "audio/wav",
        "audio/x-wav",
        "video/mp4",
        "audio/mp4",
        "application/octet-stream",
        "text/plain",
    }
    if file.content_type not in allowed_types:
        return JSONResponse(
            status_code=415,
            content={"detail": f"Unsupported content type: {file.content_type}"},
        )

    # Generate safe server-side name (ignore user-provided filename)
    suffix = Path(file.filename).suffix[:10]  # tiny guard for weird filenames
    safe_name = f"{uuid4().hex}{suffix}"
    file_path = UPLOAD_DIR / safe_name

    written = 0
    try:
        with file_path.open("wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)  # 1 MB
                if not chunk:
                    break
                written += len(chunk)
                if written > MAX_UPLOAD_BYTES:
                    raise ValueError("FILE_TOO_LARGE")
                buffer.write(chunk)
    except ValueError as e:
        if str(e) == "FILE_TOO_LARGE":
            try:
                os.remove(file_path)
            except Exception:
                pass
            return JSONResponse(
                status_code=413,
                content={"detail": f"File too large. Limit is {MAX_UPLOAD_BYTES} bytes"},
            )
        raise
    finally:
        await file.close()

    # Mock transcription result
    transcription = (
        f"Mock transcription of {file.filename}: "
        "This is a sample transcript from the meeting."
    )

    # Clean up
    try:
        os.remove(file_path)
    except Exception:
        pass

    return JSONResponse(
        content={
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": written,
            "transcription": transcription,
        }
    )

@app.get("/health")
async def health():
    return {"status": "ok"}