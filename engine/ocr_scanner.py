import os
from typing import Any
from PIL import Image
import io
from google import genai

class ScreenshotScanner:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def scan_image(self, image_path_or_pil: Any) -> str:
        """Uses Gemini Vision to parse odds screenshots into structured text."""
        if not self.client:
            return "❌ Gemini API Key required for screenshot scanning."

        try:
            # Convert PIL Image to bytes for API
            if isinstance(image_path_or_pil, str):
                img = Image.open(image_path_or_pil)
            else:
                img = image_path_or_pil

            # Convert to RGB if needed (removes alpha channel)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()

            prompt = (
                "Analyze this basketball betting screenshot. Extract all matches, home/away teams, "
                "odds, lines (1st Half, Fulltime), and league names. Output as a clean structured Markdown table."
            )

            # Use gemini-1.5-flash (confirmed working model)
            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[
                    {"mime_type": "image/jpeg", "data": img_bytes},
                    prompt
                ]
            )

            if response and response.text:
                return response.text
            else:
                return "️ No response from Gemini API. Check your API key and quota."

        except Exception as e:
            return f"❌ Error scanning image: {str(e)}\n\nCheck: 1) API key is valid 2) Billing enabled in Google AI Studio 3) Model name is correct"