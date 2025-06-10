import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
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
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description=("Creates or Overwrites file argument with data contained "
                     "in contents argument"),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description=("The file to write the data to.  "
                                 "If not provided, an error is returned."
                                 ),
                ),
                "contents": types.Schema(
                    type=types.Type.STRING,
                    description=("The data that should be written to the "
                                 "file.\nWARNING: If contents is an empty"
                                 "string. File may be destroyed."
                                 )
                ),
            }
        ),
    )

    schema_get_file_contents = types.FunctionDeclaration(
        name="get_file_contents",
        description=("Return the data contents of the specified file, "
                     "constrained to the working directory."),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description=("The file from which to read the data. "
                                 "If not provided, an error is returned."
                                 ),
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description=("Runs the specificied python script constrainted to the "
                     "current working directory."),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "script": types.Schema(
                    type=types.Type.STRING,
                    description=("The python script to execute."
                                 ),
                ),
            },
        ),
    )

    schema_get_files_info = types.FunctionDeclaration(
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
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_get_file_contents,
            schema_run_python_file,
        ]
    )

    if len(sys.argv) < 2:
        print("Error, must provide a prompt!")
        exit(1)

    parser = argparse.ArgumentParser(prog="pooglai",
                                     description="Simple LLM code assistant",
                                     epilog="https://github.com/posixenjoyer/pooglai")

    parser.add_argument(
        "user_prompt", type=str)
    parser.add_argument(
        "-v", "--verbose", action='store_true')
    args = parser.parse_args(sys.argv[1:])

    verbose = args.verbose

    user_prompt = args.user_prompt
    messages = [types.Content(
        role="user", parts=[types.Part(text=user_prompt)]
    ),
    ]

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
    )

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
            print(
                f"Calling function: {function_call.name}({function_call.args})"
            )


if __name__ == "__main__":
    main()
