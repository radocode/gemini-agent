import os
import sys
from dotenv import load_dotenv

load_dotenv()

# system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

if len(sys.argv) < 2:
    print("Error: No prompt was provided.")
    sys.exit(1)

user_prompt = sys.argv[1]
is_verbose = "--verbose" in sys.argv[2:]

api_key = os.environ.get("GEMINI_API_KEY")
from google import genai
from google.genai import types
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
model_name = 'gemini-2.0-flash-001'
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists file contents in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path itself",
            ),
        },
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs file contents in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path itself",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write file contents in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path itself",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content of the file to be written",
            ),
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)
config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
# response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)
# response = client.models.generate_content(
#     model=model_name,
#     contents=messages,
#     config=types.GenerateContentConfig(system_instruction=system_prompt),
# )

response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config = config
)

prompt_tokens=response.usage_metadata.prompt_token_count
response_tokens=response.usage_metadata.candidates_token_count

if is_verbose:
    print(f"User prompt: {response.text}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
else:
    #print(response.text)
    for item in response.function_calls:
        print(f"Calling function: {item.name}({item.args})")