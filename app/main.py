from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid

from .extractor import extract_pdf_text, extract_docx_text, extract_image_text
from .config import UPLOAD_DIR

app = FastAPI(title="Resume Extraction API", version="1.0")

@app.get("/")
def health():
    return {"status": "Local Resume API running"}

@app.post("/extract-resume-text")
async def extract_resume(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()
    file_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{file_id}.{ext}")

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        if ext == "pdf":
            text = extract_pdf_text(path)
        elif ext in ["docx", "doc"]:
            text = extract_docx_text(path)
        elif ext in ["jpg", "jpeg", "png"]:
            text = extract_image_text(path)
        else:
            return {"success": False, "error": "Unsupported file format"}

        return {
            "success": True,
            "filename": file.filename,
            "text_length": len(text),
            "raw_text": text.strip()
        }

    finally:
        if os.path.exists(path):
            os.remove(path)
