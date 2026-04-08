# a chat loop that keeps conversation history in a list and sends it as context to Gemini.
from dotenv import load_dotenv
import os
from google import genai

load_dotenv(dotenv_path=".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")
client = genai.Client(api_key=api_key)
history = []

print("Gemini Chat started. Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chat ended.")
        break
    history.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=history
        )
        model_text = response.text
        print("Gemini:", model_text)
        history.append({
            "role": "model",
            "parts": [{"text": model_text}]
        })

    except Exception as e:
        print("Error:", e)