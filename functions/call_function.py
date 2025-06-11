from functions.write_file import write_file
from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_contents
from functions.run_python_file import run_python_file
from google import genai
from google.genai import types


def call_function(function_call_parts, verbose=False):
    working_directory = "./calculator"
    functions = {
        "run_python_file": run_python_file,
        "write_file":   write_file,
        "get_file_contents": get_file_contents,
        "get_files_info": get_files_info,
    }

    if verbose:
        print(f"Calling function {
              function_call_parts.name}({function_call_parts.args})")
    else:
        print(f" - Calling function: {function_call_parts.name}")

    function_call_parts.args["working_directory"] = working_directory

    function_name = function_call_parts.name
    function_args = function_call_parts.args

    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_parts.name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    else:
        function_result = (
            functions[function_name](**function_args)
        )
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
