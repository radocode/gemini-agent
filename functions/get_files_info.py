import os

def get_files_info(working_directory, directory=None):
    try:
        if not os.path.isdir(working_directory):
            return f'Error: "{working_directory}" is not a directory'
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'
        if not os.listdir(directory) in working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    else:
            #f'''- README.md: file_size=1032 bytes, is_dir=False
            #    - src: file_size=128 bytes, is_dir=True
            #   - package.json: file_size=1234 bytes, is_dir=False'''
        info = ""
        for item in working_directory:
            info += f'- {item}: file_size={os.path.getsize(item)} bytes, is_dir={os.path.isdir(item)}' + "\n"
        return info