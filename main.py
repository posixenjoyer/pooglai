import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function


def make_write_file_schema():
    return types.FunctionDeclaration(
        name="write_file",
        description=("Creates or Overwrites file argument with data contained "
                     "in contents argument"),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "filename": types.Schema(
                    type=types.Type.STRING,
                    description=("The file to write the data to.  "
                                 "If not provided, an error is returned."
                                 ),
                ),
                "data": types.Schema(
                    type=types.Type.STRING,
                    description=("The data that should be written to the "
                                 "file.\nWARNING: If contents is an empty"
                                 "string. File may be destroyed."
                                 )
                ),
            }
        ),
    )


def make_get_file_contents_schema():
    return types.FunctionDeclaration(
        name="get_file_contents",
        description=("Return the data contents of the specified file, "
                     "constrained to the working directory."),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description=("The file from which to read the data. "
                                 "If not provided, an error is returned."
                                 ),
                ),
            },
        ),
    )


def make_run_python_file_schema():
    return types.FunctionDeclaration(
        name="run_python_file",
        description=("Runs the specificied python script constrainted to the "
                     "current working directory. You can use ./<script>"),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "path": types.Schema(
                    type=types.Type.STRING,
                    description=("The python script to execute."
                                 ),
                ),
            },
        ),
    )


def make_get_files_info_schema():
    return types.FunctionDeclaration(
        name="get_files_info",
        description=("Lists files in the specified directory along with their "
                     "sizes, constrained to the working directory."),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description=("The directory to list files from, relative "
                                 "to the working directory. If not provided, "
                                 "lists files in the working directory itself."
                                 ),
                ),
            },
        ),
    )


def make_function_schema():

    schemas = []

    schemas.append(make_write_file_schema())
    schemas.append(make_get_file_contents_schema())
    schemas.append(make_run_python_file_schema())
    schemas.append(make_get_files_info_schema())

    return schemas


def main():
    pkg_url = "https://github.com/posixenjoyer/pooglai"
    max_prompt_iterations = 15
    messages = []

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    system_prompt = ("You are a helpful AI coding agent.\nWhen a user asks a "
                     "question or makes a request, make a function call plan. "
                     "You can perform the following operations:\n"
                     "\n- List files and directories\n"
                     "\n- Read the contents of file\n"
                     "\n- Create and write the contents of files\n"
                     "\n- Run python scripts\n"
                     "All paths you provide should be relative to the working "
                     "directory. You do not need to specify the working "
                     "directory in your function calls as it is automatically "
                     "injected for security reasons."
                     )

    model_name = "gemini-2.0-flash-001"
    client = genai.Client(api_key=api_key)

    function_list = make_function_schema()
    available_functions = types.Tool(
        function_declarations=function_list
    )

    if len(sys.argv) < 2:
        print("Error, must provide a prompt!")
        exit(1)

    parser = argparse.ArgumentParser(prog="pooglai",
                                     description="Simple LLM code assistant",
                                     epilog=pkg_url)
    parser.add_argument(
        "user_prompt", type=str)
    parser.add_argument(
        "-v", "--verbose", action='store_true')
    args = parser.parse_args(sys.argv[1:])

    response = types.GenerateContentResponse()

    for _ in range(max_prompt_iterations):
        verbose = args.verbose

        user_prompt = args.user_prompt
        messages.append(types.Content(
            role="user", parts=[types.Part(text=user_prompt)]
        ))

        if response.candidates is not None:
            for candidate in response.candidates:
                messages.append(candidate.content)

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt)
            )
        except Exception as e:
            print(f"Got exception processing prompt: {e}")

        if verbose:
            if response.usage_metadata is not None:
                print(f"User prompt: {user_prompt}")
                response_parse = ("Response tokens: "
                                  f'{response.usage_metadata.candidates_token_count}'
                                  )
                print(f'Prompt tokens: {
                    response.usage_metadata.prompt_token_count}')
                print(response_parse)

                if response.text is not None:
                    print(response.text)
            if response.function_calls is not None:
                for function_call in response.function_calls:
                    function_call_result = call_function(function_call)
                    if function_call_result is None:
                        raise Exception("FUNCTION CALL FAILED!!")

                    if function_call_result.parts is not None:
                        results = function_call_result.parts[0]
                        messages.append(results)

                        if verbose:
                            print(
                                f"-> {results.function_response.response}"
                            )
                    else:
                        results = ""
            else:
                print(response.text)
                break


if __name__ == "__main__":
    main()
