import os
from pathlib import Path


def isLocal(full_path, working_directory):
    try:
        full_path.relative_to(working_directory)
    except ValueError:
        return False
    return True


def get_files_info(working_directory, directory=None):

    if directory is None:
        return f'Error: "{directory}" is not a directory'

    if type(directory) is not str:
        return f'Error: "{directory}" is not a string.'

    working_path = Path(os.path.abspath(working_directory)).resolve()
    full_path = Path(working_path).joinpath(directory).resolve()

    if not full_path.is_dir():
        return f'Error: "{directory}" is not a directory'

    if not isLocal(full_path, working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

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
        except Exception as e:
            is_dir = False

        result += f' - {file}: file_size:{size} bytes, is_dir={is_dir}\n'

    return result
