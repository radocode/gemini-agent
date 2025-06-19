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
