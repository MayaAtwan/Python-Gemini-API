from dotenv import load_dotenv
from google import genai
import os
import requests # requests is a Python library used to send HTTP requests to websites
from bs4 import BeautifulSoup # BeautifulSoup creates a tree data structure. why a tree? because html is naturally nested.. not flat. it must be a tree


load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
url=input("Enter the url here: ").strip()

try:
    response=requests.get(url,timeout=15)
# print(response.text) # this prints the html of the webpage
    response.raise_for_status() # this checks if the request succeeded
# Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")
    # Remove unwanted elements
    for tag in soup(["script", "style", "noscript", "header", "footer"]):
        tag.decompose()

    # Extract clean text
    text = soup.get_text(separator=" ", strip=True)
    # Optional: limit text length so prompt isn't too large
    cleaned_text = text[:8000]

    # Build prompt
    prompt = f"""
    Summarize the following webpage content in 5-7 clear bullet points.
    Focus on the main ideas and important details.

    Webpage content:
    {cleaned_text}
    """
    result = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    print("\n--- Summary ---\n")
    print(result.text)
except requests.exceptions.RequestException as e:
    print(f"Error fetching webpage: {e}")
except Exception as e:
    print(f"An error occurred: {e}")