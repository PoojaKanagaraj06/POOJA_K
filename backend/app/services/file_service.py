import json
import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.database import UPLOADS_DIR

ALLOWED_EXTENSIONS = {".txt", ".md", ".json"}


def validate_file(file: UploadFile) -> None:
    if file is None:
        raise HTTPException(status_code=400, detail="No file was provided.")

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file was provided.")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}. Allowed types: {sorted(ALLOWED_EXTENSIONS)}")

    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    if file_size == 0:
        raise HTTPException(status_code=400, detail="File is empty.")


def extract_text_from_file(file_name: str, file_bytes: bytes) -> str:
    ext = Path(file_name).suffix.lower()

    if ext in {".txt", ".md"}:
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise HTTPException(status_code=400, detail="File could not be decoded as UTF-8 text.") from exc

    if ext == ".json":
        try:
            parsed = json.loads(file_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise HTTPException(status_code=400, detail="Invalid JSON file content.") from exc
        return json.dumps(parsed, ensure_ascii=False, indent=2)

    raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_name}")


def save_uploaded_file(file_name: str, file_bytes: bytes) -> tuple[str, str]:
    extension = Path(file_name).suffix.lower()
    unique_name = f"{uuid.uuid4()}_{file_name}"
    file_path = UPLOADS_DIR / unique_name
    file_path.write_bytes(file_bytes)
    return unique_name, str(file_path)
