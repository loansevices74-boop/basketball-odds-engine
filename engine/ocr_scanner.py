import os
from typing import Any
from PIL import Image
import io

class ScreenshotScanner:
    def __init__(self, api_key: str = None):
        # Ignore api_key for EasyOCR (no key needed)
        self.client = "easyocr"

    def scan_image(self, image_path_or_pil: Any) -> str:
        """Uses EasyOCR to extract text from betting screenshots."""
        try:
            if isinstance(image_path_or_pil, str):
                img = Image.open(image_path_or_pil)
            else:
                img = image_path_or_pil

            # Convert to RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Try EasyOCR
            try:
                import easyocr
                reader = easyocr.Reader(['en'], gpu=False)
                results = reader.readtext(img)
                
                # Extract all text
                extracted_text = "\n".join([r[1] for r in results])
                
                return f"### Extracted Text (EasyOCR)\n\n```\n{extracted_text}\n```\n\n⚠️ For structured JSON output, enable Gemini API billing."
                
            except ImportError:
                return "❌ EasyOCR not installed. Add `easyocr>=1.7.0` to requirements.txt"
                
        except Exception as e:
            return f" Error scanning image: {str(e)}"