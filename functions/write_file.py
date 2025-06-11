import os
from functions.get_files_info import isLocal


def write_file(working_directory, filename, data):
    full_path, is_valid_path = isLocal(working_directory, filename)

    if not is_valid_path:
        return f'Error: Cannot write to "{filename}" as it is outside the permitted working directory'

    if full_path is None:
        return 'Error: Never Never Never. (is_path = True, and full_path is None)'

    direct_parent = full_path.rsplit('/', 1)[0]
    if not os.path.exists(direct_parent):
        try:
            os.makedirs(direct_parent, 755)
        except Exception as e:
            return f'Error: {e}'

    try:
        file = os.open(full_path, os.O_CREAT | os.O_WRONLY |
                       os.O_TRUNC | os.O_TRUNC)
    except Exception as e:
        return f'Error: {e}'

    try:
        os.write(file, data.encode())
    except Exception as e:
        return f'Error: {e}'

    return f'Successfully wrote to "{full_path}" ({len(data)} characters written)'
