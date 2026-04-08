# Generate Marketing Content (UPDATED)

from dotenv import load_dotenv
import os
from google import genai
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
product_name = input("Enter product name: ")
audience = input("Enter target audience: ")

# Prompt template
prompt = f"""
You are a marketing expert.

Create marketing content for the following product:

Product Name: {product_name}
Target Audience: {audience}

Generate:
1. A short product description (2-3 sentences)
2. 3 catchy ad slogans
3. 1 persuasive call-to-action

Return the response in this format:

Description:
...

Slogans:
1. ...
2. ...
3. ...

Call to Action:
...
"""
# Call Gemini
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt
)
print("\n--- Marketing Content ---\n")
print(response.text)