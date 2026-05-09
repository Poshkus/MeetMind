from uuid import uuid4
from pathlib import Path
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="MeetMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_UPLOAD_BYTES = 1 * 1024 * 1024 * 1024

# Разрешённые типы содержимого (content_type)
ALLOWED_CONTENT_TYPES = {
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "video/mp4",
    "audio/mp4",
    "text/plain",
}

# Разрешённые расширения файлов по расширению (для дополнительной проверки)
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".mp4", ".txt"}


def cleanup_file(path: Path) -> None:
    """Удаляет файл при ошибке, чтобы не оставлять частичные загрузки."""
    try:
        if path.exists():
            path.unlink()
    except Exception:
        pass


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Проверка типа содержимого
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        return JSONResponse(
            status_code=415,
            content={"detail": f"Unsupported content type: {file.content_type}"},
        )

    # Проверка расширения файла по имени
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return JSONResponse(
            status_code=415,
            content={"detail": f"Unsupported file extension: {ext}"},
        )

    safe_name = f"{uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / safe_name

    written = 0
    try:
        with file_path.open("wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                written += len(chunk)
                if written > MAX_UPLOAD_BYTES:
                    raise ValueError("FILE_TOO_LARGE")
                buffer.write(chunk)
    except ValueError as e:
        if str(e) == "FILE_TOO_LARGE":
            cleanup_file(file_path)
            return JSONResponse(
                status_code=413,
                content={"detail": f"File too large. Limit is {MAX_UPLOAD_BYTES} bytes"},
            )
        cleanup_file(file_path)
        raise
    except Exception:
        cleanup_file(file_path)
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