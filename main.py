import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


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
    print(f"Response: {response.text}")


def generate_content(client: genai.Client, messages: list[types.Content], verbose: bool=False) -> None:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )
    usage_metadata = response.usage_metadata
    if usage_metadata is None:
        raise RuntimeError("usage metadata is missing, failed API request")
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}") if verbose else None
    print(f"Response tokens: {usage_metadata.candidates_token_count}") if verbose else None
    return response


if __name__ == "__main__":
    main()
