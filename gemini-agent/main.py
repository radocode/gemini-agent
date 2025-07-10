import os
import sys
from dotenv import load_dotenv
import functions
import functions.get_files_info

load_dotenv()

if len(sys.argv) < 2:
    print("Error: No prompt was provided.")
    sys.exit(1)

user_prompt = sys.argv[1]
is_verbose = "--verbose" in sys.argv[2:]

# Initialize Gemini client
api_key = os.environ.get("GEMINI_API_KEY")
from google import genai
from google.genai import types
client = genai.Client(api_key=api_key)

# System prompt
system_prompt = """
You are a helpful AI coding agent.

When interacting, think step-by-step. Use the provided functions via function calls:
- get_files_info(directory)
- get_file_content(file_path)
- run_python_file(file_path)
- write_file(file_path, content)

Paths are relative; working_directory is injected automatically.
"""

# Register function schemas
func_declarations = []

def make_schema(fn_name, desc, params):
    return types.FunctionDeclaration(
        name=fn_name,
        description=desc,
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties=params,
        ),
    )

func_declarations.append(make_schema(
    "get_files_info",
    "List files in a directory",
    {"directory": types.Schema(type=types.Type.STRING)}
))
func_declarations.append(make_schema(
    "get_file_content",
    "Get the contents of a file",
    {"file_path": types.Schema(type=types.Type.STRING)}
))
func_declarations.append(make_schema(
    "run_python_file",
    "Execute a Python file",
    {"file_path": types.Schema(type=types.Type.STRING)}
))
func_declarations.append(make_schema(
    "write_file",
    "Write content to a file",
    {
        "file_path": types.Schema(type=types.Type.STRING),
        "content": types.Schema(type=types.Type.STRING)
    }
))

tool = types.Tool(function_declarations=func_declarations)
config = types.GenerateContentConfig(tools=[tool], system_instruction=system_prompt)

# Initialize message history
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

# Local function dispatcher
def call_function(call: types.FunctionCall) -> types.Content:
    name = call.name
    args = dict(call.args)
    args['working_directory'] = os.getcwd()

    # Map name to actual function
    func = {
        "get_files_info": functions.get_files_info.get_file_content,
        "get_file_content": functions.get_files_info.get_file_content,
        "run_python_file": functions.get_files_info.run_python_file,
        "write_file": functions.get_files_info.write_file,
    }.get(name)

    if is_verbose:
        print(f"Calling function: {name} with {args}")

    if not func:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=name,
                response={"error": f"Unknown function: {name}"}
            )]
        )

    try:
        result = func(**args)
        response_content = {"result": result}
    except Exception as e:
        response_content = {"error": str(e)}

    tool_msg = types.Content(
        role="tool",
        parts=[types.Part.from_function_response(name=name, response=response_content)]
    )

    if is_verbose:
        print(f"-> {response_content}")

    return tool_msg

# Conversation loop
for i in range(20):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=config
        )
    except Exception as e:
        print(f"Generation error: {e}")
        break

    # Add assistant messages
    for cand in response.candidates:
        # Only append if candidate has text content
        if isinstance(cand.content, str) and cand.content.strip():
            messages.append(types.Content(role="assistant", parts=[types.Part(text=cand.content)]))

    # If final text, print and exit
    if response.text:
        print(response.text)
        break

    # Otherwise, perform function calls
    for call in response.function_calls:
        tool_message = call_function(call)
        messages.append(tool_message)

        if is_verbose:
            print(f"-> {tool_message.parts[0].function_response.response}")
else:
    print("Max iterations reached without final response.")
