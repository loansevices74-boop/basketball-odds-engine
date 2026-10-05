import os
from typing import Any
from PIL import Image
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
            return "Gemini API Key required for screenshot scanning."

        if isinstance(image_path_or_pil, str):
            img = Image.open(image_path_or_pil)
        else:
            img = image_path_or_pil

        prompt = (
            "Analyze this basketball betting screenshot. Extract all matches, home/away teams, "
            "odds, lines (1st Half, Fulltime), and league names. Output as a clean structured Markdown table."
        )

        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[img, prompt]
        )
        return response.text