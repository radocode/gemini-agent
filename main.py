import os
import sys
from dotenv import load_dotenv

load_dotenv()

if len(sys.argv) < 2:
    print("Error: No prompt was provided.")
    sys.exit(1)

user_prompt = sys.argv[1]
is_verbose = "--verbose" in sys.argv[2:]

api_key = os.environ.get("GEMINI_API_KEY")
from google import genai
from google.genai import types
client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)

prompt_tokens=response.usage_metadata.prompt_token_count
response_tokens=response.usage_metadata.candidates_token_count

if is_verbose:
    print(f"User prompt: {response.text}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
else:
    print(response.text)