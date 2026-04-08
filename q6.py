# Multi-Modal Caption Generator (Text + Image)
from dotenv import load_dotenv
from google import genai
from PIL import Image
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

image_path = input("Enter the image path: ").strip()
try:
    image = Image.open(image_path)
    prompt = """
Look at this image and generate:
1. A short descriptive caption
2. Exactly 3 relevant hashtags

Return the response in this format:

Caption:
...

Hashtags:
1. ...
2. ...
3. ...
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[prompt, image]
    )
    print("\n--- Image Marketing Content ---\n")
    print(response.text)
except FileNotFoundError:
    print("Error: Image file not found. Please check the path.")
except Exception as e:
    print(f"An error occurred: {e}")