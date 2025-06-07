import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    if len(sys.argv) < 2:
        print("Error, must provide a prompt!")
        exit(1)

    parser = argparse.ArgumentParser(prog="pooglai",
                                     description="Simple LLM code assistant",
                                     epilog="https://github.com/posixenjoyer/pooglai")

    parser.add_argument("user_prompt", type=str)
    parser.add_argument("-v", "--verbose", action='store_true')
    args = parser.parse_args(sys.argv[1:])

    verbose = args.verbose

    user_prompt = args.user_prompt
    messages = [types.Content(
        role="user", parts=[types.Part(text=user_prompt)]),]
    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents=messages)

    if verbose:
        if response.usage_metadata is not None:
            print(f"User prompt: {user_prompt}")
            response_parse = ("Response tokens: "
                              f'{response.usage_metadata.candidates_token_count}')
            print(f'Prompt tokens: {
                  response.usage_metadata.prompt_token_count}')
            print(response_parse)

    print(response.text)


if __name__ == "__main__":
    main()
