import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="aiagent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    verbose = args.verbose
    print(f"User prompt: {user_prompt}") if verbose else None
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("api key not found")
    client = genai.Client(api_key=api_key)
    response = generate_content(client=client, messages=messages, verbose=verbose)
    if response.function_calls is None or len(response.function_calls) == 0:
        print(f"Response: {response.text}")
        return
    function_results = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=verbose)
        parts = function_call_result.parts
        if not parts:
            raise RuntimeError("function call result has no parts")
        first_part = parts[0]
        function_response = first_part.function_response
        if function_response is None:
            raise RuntimeError("function call result has no function response")
        response = function_response.response
        if response is None:
            raise RuntimeError("function call result has no response")
        function_results.append(first_part)
        if verbose:
            print(f"-> {first_part.function_response.response}")


def generate_content(
    client: genai.Client, messages: list[types.Content], verbose: bool = False
) -> None:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt, temperature=0
        ),
    )
    usage_metadata = response.usage_metadata
    if usage_metadata is None:
        raise RuntimeError("usage metadata is missing, failed API request")
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}") if verbose else None
    (
        print(f"Response tokens: {usage_metadata.candidates_token_count}")
        if verbose
        else None
    )
    return response


if __name__ == "__main__":
    main()
