from google import genai
from shared import settings

genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)