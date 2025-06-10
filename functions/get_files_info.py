import os
from pathlib import Path
from functions.islocal import isLocal


def get_files_info(working_directory, directory=None):

    if directory is None:
        return f'Error: "{directory}" is not a directory'

    if type(directory) is not str:
        return f'Error: "{directory}" is not a string.'

    full_path, path_is_valid = isLocal(working_directory, directory)
    if not path_is_valid:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if full_path is None:
        return 'Error: This error should literally never happen'

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    files = os.listdir(full_path)

    if len(files) == 0:
        return f'{directory} empty!'

    result = ""
    for file in files:
        full_file = str(full_path) + "/" + file
        try:
            size = os.path.getsize(full_file)
        except Exception as e:
            result += f'Error: File={file} {e}\n'
            return result
        try:
            is_dir = os.path.isdir(full_file)
        except Exception:
            is_dir = False

        result += f' - {file}: file_size:{size} bytes, is_dir={is_dir}\n'

    return result
