# a Python script that sends a prompt to Gemini and prints the generated response.

from dotenv import load_dotenv
import os
from google import genai

load_dotenv(dotenv_path=".env")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found!")
client = genai.Client(api_key=api_key)
prompt = "Explain black holes like I'm 10 years old."
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt
)
print(response.text)