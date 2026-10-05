import os
import io
import base64
from typing import Any
from PIL import Image
from openai import OpenAI

class ScreenshotScanner:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.environ.get("QWEN_API_KEY")
        # Default Base URL (DashScope). Change if using OpenRouter or another provider.
        self.base_url = base_url or os.environ.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = None

    def scan_image(self, image_path_or_pil: Any) -> str:
        """Uses Qwen Vision to parse odds screenshots into structured text."""
        if not self.client:
            return "❌ Qwen API Key required for screenshot scanning."

        try:
            # 1. Load and prepare image
            if isinstance(image_path_or_pil, str):
                img = Image.open(image_path_or_pil)
            else:
                img = image_path_or_pil

            if img.mode != 'RGB':
                img = img.convert('RGB')

            # 2. Convert image to Base64
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # 3. Define Prompt
            prompt = (
                "Analyze this basketball betting screenshot. Extract all matches, home/away teams, "
                "odds, lines (1st Half, Fulltime), and league names. Output as a clean structured Markdown table."
            )

            # 4. Call Qwen API (OpenAI compatible format)
            # Note: Change the model name below if your provider uses a different exact ID
            response = self.client.chat.completions.create(
                model="qwen-vl-max",  # <-- Change this if your provider uses "qwen-omni-flash" or similar
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}
                            },
                            {"type": "text", "text": prompt}
                        ]
                    }
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"❌ Error scanning image: {str(e)}\n\nCheck: 1) API Key 2) Base URL 3) Model Name"