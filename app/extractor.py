# app/extractor.py

# =====================================================
# IMPORTS (ALL SAFE FOR CLOUD)
# =====================================================

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import pytesseract
except ImportError:
    pytesseract = None

try:
    import cv2
except ImportError:
    cv2 = None

from PIL import Image
from docx import Document
from typing import Optional
from .config import TESSERACT_PATH


# =====================================================
# TESSERACT CONFIGURATION (OPTIONAL)
# =====================================================

if pytesseract and TESSERACT_PATH:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# =====================================================
# PDF TEXT EXTRACTION
# =====================================================

def extract_pdf_text(path: str) -> str:
    """
    Extract text from a PDF file.
    1. First tries native text extraction (fast)
    2. Falls back to OCR only if text is insufficient
    """

    if not fitz:
        return ""

    text = ""

    try:
        doc = fitz.open(path)
    except Exception:
        return ""

    # -------- Native text extraction --------
    for page in doc:
        try:
            text += page.get_text()
        except Exception:
            continue

    if len(text.strip()) > 50:
        return text.strip()

    # -------- OCR fallback --------
    if not pytesseract:
        return text.strip()

    for page in doc:
        try:
            pix = page.get_pixmap()
            img = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )
            text += pytesseract.image_to_string(img)
        except Exception:
            continue

    return text.strip()


# =====================================================
# DOCX TEXT EXTRACTION
# =====================================================

def extract_docx_text(path: str) -> str:
    """
    Extract text from a DOCX file.
    """

    try:
        doc = Document(path)
    except Exception:
        return ""

    paragraphs = []
    for p in doc.paragraphs:
        if p.text and p.text.strip():
            paragraphs.append(p.text.strip())

    return "\n".join(paragraphs)


# =====================================================
# IMAGE TEXT EXTRACTION (OCR)
# =====================================================

def extract_image_text(path: str) -> str:
    """
    Extract text from an image using OpenCV + Tesseract.
    Completely optional and cloud-safe.
    """

    if not cv2 or not pytesseract:
        return ""

    try:
        img = cv2.imread(path)
        if img is None:
            return ""

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(
            gray, 150, 255, cv2.THRESH_BINARY
        )[1]

        return pytesseract.image_to_string(gray).strip()

    except Exception:
        return ""
