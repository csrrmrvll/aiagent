import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def _parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="aiagent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def _initialize_agent(user_prompt: str) -> tuple[genai.Client, list[types.Content]]:
    """Initializes the Gemini client and prepares initial messages."""
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Error: GEMINI_API_KEY environment variable not found.")
    client = genai.Client(api_key=api_key)
    initial_messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    return client, initial_messages


def _log_verbose(message: str, verbose: bool):
    """Prints a message if verbose mode is enabled."""
    if verbose:
        print(message)


def _append_candidates_to_messages(
    messages: list[types.Content], candidates: list[types.Candidate]
):
    """Appends candidates from the model's response to the message history."""
    if candidates:
        for candidate in candidates:
            messages.append(candidate)


def _log_usage_metadata(usage_metadata: types.UsageMetadata, verbose: bool):
    """Logs token usage metadata if verbose mode is enabled."""
    if usage_metadata is None:
        raise RuntimeError("Error: Usage metadata is missing from the API response.")
    _log_verbose(f"Prompt tokens: {usage_metadata.prompt_token_count}", verbose)
    _log_verbose(f"Response tokens: {usage_metadata.candidates_token_count}", verbose)


def _handle_function_calls(
    function_calls: list[types.FunctionCall],
    messages: list[types.Content],
    verbose: bool,
) -> list[types.Part]:
    """Executes function calls and returns their results as a list of Content parts."""
    function_results: list[types.Part] = []
    for function_call in function_calls:
        function_call_result = call_function(function_call, verbose=verbose)
        parts = function_call_result.parts
        if not parts:
            raise RuntimeError("Error: Function call result has no parts.")
        first_part = parts[0]
        function_response = first_part.function_response
        if function_response is None:
            raise RuntimeError("Error: Function call result has no function response.")
        response_content = function_response.response
        if response_content is None:
            raise RuntimeError("Error: Function response content is missing.")

        function_results.append(first_part)
        _log_verbose(f"-> {response_content}", verbose)
    return function_results


def _process_agent_step(
    client: genai.Client, messages: list[types.Content], verbose: bool
) -> bool:
    """Performs one step of the agent's interaction, generating content and handling function calls."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    _append_candidates_to_messages(messages, response.candidates)
    _log_usage_metadata(response.usage_metadata, verbose)

    if not response.function_calls:
        print(f"Final response: {response.text}")
        return False  # No more steps needed, final response received

    function_results = _handle_function_calls(
        response.function_calls, messages, verbose
    )
    messages.append(types.Content(role="user", parts=function_results))
    return True  # More steps might be needed


def main():
    args = _parse_arguments()
    user_prompt = args.user_prompt
    verbose = args.verbose

    _log_verbose(f"User prompt: {user_prompt}", verbose)

    try:
        client, messages = _initialize_agent(user_prompt)
    except RuntimeError as e:
        print(f"Error: Agent initialization failed: {e}")
        exit(1)

    max_iterations = 20
    for i in range(max_iterations):
        try:
            if not _process_agent_step(client, messages, verbose):
                return
        except RuntimeError as e:
            print(f"Error: An error occurred during agent step: {e}")
            exit(1)
        except Exception as e:
            print(f"Error: An unexpected error occurred: {e}")
            exit(1)

    print(
        f"Error: Max iterations ({max_iterations}) reached without a final response, stopping."
    )
    exit(1)


if __name__ == "__main__":
    main()
