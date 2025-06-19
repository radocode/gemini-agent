import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)


prompt = client.models.generate_content(model='gemini-2.0-flash-001', contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")

print(prompt.text)

print(f"Prompt tokens: {prompt.usage_metadata.prompt_token_count}")
print(f"Response tokens: {prompt.usage_metadata.candidates_token_count}")