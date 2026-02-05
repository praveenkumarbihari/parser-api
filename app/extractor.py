import fitz
import pytesseract
import cv2
from PIL import Image
import numpy as np
from docx import Document
from .config import TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# -------------------------
# PDF
# -------------------------

def extract_pdf_text(path):
    text = ""
    doc = fitz.open(path)

    for page in doc:
        text += page.get_text()

    if len(text.strip()) > 50:
        return text

    # OCR fallback
    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text += pytesseract.image_to_string(img)

    return text

# -------------------------
# DOCX
# -------------------------

def extract_docx_text(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

# -------------------------
# IMAGE
# -------------------------

def extract_image_text(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    return pytesseract.image_to_string(gray)
