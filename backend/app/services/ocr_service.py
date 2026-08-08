"""
OCR pipeline (see architecture doc Section 14).

Steps: pre-process (deskew/denoise/contrast) -> OCR extraction -> text
post-processing (entity extraction: URLs, phone numbers, amounts).

Uses Tesseract as the default self-hosted engine. In production this
should be swapped for/augmented with a cloud OCR API (Vision/Textract)
for noisy real-world screenshots — the interface below is written so
that swap only touches `_extract_text`.
"""
import re
from typing import Any

import cv2
import numpy as np
import pytesseract
from PIL import Image

from app.core.config import settings

pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

URL_RE = re.compile(r"https?://[^\s]+|www\.[^\s]+")
PHONE_RE = re.compile(r"\+?\d[\d\s\-()]{7,}\d")
AMOUNT_RE = re.compile(r"(?:USD|INR|EUR|GBP|\$|₹|€|£)\s?[\d,]+(?:\.\d{1,2})?")


class OCRService:
    def _preprocess(self, image_bytes: bytes) -> np.ndarray:
        img_array = np.frombuffer(image_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Denoise + adaptive threshold improves OCR accuracy on real-world screenshots
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11
        )
        return thresh

    def _extract_text(self, processed_image: np.ndarray) -> str:
        pil_img = Image.fromarray(processed_image)
        return pytesseract.image_to_string(pil_img)

    def extract(self, image_bytes: bytes) -> dict[str, Any]:
        processed = self._preprocess(image_bytes)
        text = self._extract_text(processed)

        return {
            "raw_text": text.strip(),
            "extracted_urls": URL_RE.findall(text),
            "extracted_phones": PHONE_RE.findall(text),
            "extracted_amounts": AMOUNT_RE.findall(text),
            "word_count": len(text.split()),
        }


ocr_service = OCRService()
