import os
import argparse
from dotenv import load_dotenv
from google import genai


def main():
    parser = argparse.ArgumentParser(description="aiagent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("api key not found")
    client = genai.Client(api_key=api_key)
    print(f"User prompt: {user_prompt}")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
    )
    usage_metadata = response.usage_metadata
    if usage_metadata is None:
        raise RuntimeError("usage metadata is missing, failed API request")
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
