import os


def isLocal(working_directory, file):

    abs_working_path = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(os.path.join(abs_working_path, file))

    if not abs_full_path.startswith(abs_working_path):
        return None, False

    return abs_full_path, True
