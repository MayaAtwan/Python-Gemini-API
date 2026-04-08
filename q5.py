# AI-Powered Code Reviewer
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
file_path = input("Enter the path to the Python file: ").strip()

try:
    # Read file content
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    max_chars = 20000
    if len(code) > max_chars:
        code = code[:max_chars]
        print(f"Warning: File too large, only first {max_chars} characters were sent.\n")
    prompt = f"""
    You are a senior Python code reviewer.
    
    Review the following Python code and provide feedback in this format:
    
    1. Summary
    - Briefly explain what the code does
    
    2. Strengths
    - Mention 2-4 good things
    
    3. Issues
    - Mention bugs, bad practices, or risks
    
    4. Suggestions for Improvement
    - Give concrete improvements
    
    5. Cleaned-Up Version
    - If possible, provide a better version of the code
    
    Python code:
    ```python
    {code}
        """
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    print("\n--- Code Review ---\n")
    print(response.text)
except FileNotFoundError:
    print("Error: File not found. Please check the path.")
except Exception as e:
    print(f"An error occurred: {e}")