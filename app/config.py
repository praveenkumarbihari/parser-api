import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Windows only
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
