import os
from functions.get_files_info import isLocal

MAX_CHARS = 10000


def get_file_contents(working_directory, file_path):

    full_path, is_valid_path = isLocal(working_directory, file_path)
    if not is_valid_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'

    if full_path is None:
        return 'Error: this should never be reached.\n'

    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"\n'

    try:
        fd = open(full_path, "r")
    except Exception as e:
        return f'Error: {e}\n'

    try:
        contents = fd.read(MAX_CHARS + 1)
    except Exception as e:
        return f'Error: {e}\n'

    if len(contents) > MAX_CHARS:
        contents = contents[:MAX_CHARS + 1]
        if contents[-1] != '\n':
            contents += '\n'
        contents += f'[...File "{file_path}" truncated at 10000 characters]\n'

    return contents
