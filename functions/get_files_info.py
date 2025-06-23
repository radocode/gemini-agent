import os

def get_files_info(working_directory, directory=None):
    try:
        # Default directory is the working directory itself
        if directory is None:
            directory = working_directory

        # Resolve full paths relative to working_directory
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(os.path.join(working_directory, directory))

        # Validate that the target dir is a real directory
        if not os.path.isdir(abs_target_dir):
            return f'Error: "{directory}" is not a directory'

        # Security check: is target dir within working dir?
        if not abs_target_dir.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Build output string
        lines = []
        for item in os.listdir(abs_target_dir):
            full_path = os.path.join(abs_target_dir, item)
            size = os.path.getsize(full_path) if os.path.isfile(full_path) else 0
            is_dir = os.path.isdir(full_path)
            lines.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"

def get_file_content(working_directory, file_path):
    try:
        MAX_CHARS = 10000
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_target_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_target_path):
            return f'Error: "{file_path}" is not a file'

        with open(abs_target_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS + 1)
            if len(content) > MAX_CHARS:
                content = content[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f"Error: {e}"
        

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_target_path.startswith(abs_working_dir):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        target_dir = os.path.dirname(abs_target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Write content to the file
        with open(abs_target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"