
import sys
from pkg.calculator import Calculator
from pkg.render import format_json_output

def display_usage() -> None:
    """
    Displays the application's usage instructions to the console.
    This function is called when no expression or an invalid expression
    is provided via command-line arguments.
    """
    print("Calculator App")
    print('Usage: python main.py "<expression>"')
    print('Example: python main.py "3 + 5 * 2"')


def parse_expression_from_arguments() -> str | None:
    """
    Parses command-line arguments to extract the mathematical expression.
    The expression is expected to be provided as a single argument (potentially quoted)
    or multiple arguments that are joined to form the expression.

    Returns:
        A string containing the mathematical expression if found,
        otherwise None, indicating that no expression was provided.
    """
    # sys.argv[0] is the script name, so we look for arguments starting from index 1.
    if len(sys.argv) < 2:
        return None
    # Joins all command-line arguments after the script name into a single string.
    # This allows expressions with spaces (e.g., "1 + 2") to be passed correctly.
    return " ".join(sys.argv[1:])


def execute_calculation_and_display_result(calculator: Calculator, expression: str) -> None:
    """
    Executes the given mathematical expression using the provided calculator instance.
    It handles potential errors during the evaluation process and prints the result
    or an appropriate error message to the console.

    Args:
        calculator: An instance of the Calculator class responsible for evaluating expressions.
        expression: The mathematical expression string to be evaluated.
    """
    try:
        result = calculator.evaluate(expression)
        # If the calculator returns a result (even 0 is a valid result),
        # format and print it as JSON.
        if result is not None:
            output = format_json_output(expression, result)
            print(output)
        else:
            # This case should ideally not be reached if the calculator handles
            # all valid expressions by returning a number, but it's a safeguard.
            print(f"Error: No result obtained for expression '{expression}'.")
    except ValueError as e:
        # Catches errors specific to invalid mathematical expressions (e.g., syntax errors).
        print(f"Error: Invalid expression '{expression}': {e}")
    except Exception as e:
        # Catches any other unexpected errors during the calculation process.
        print(f"Error: An unexpected error occurred during calculation: {e}")


def run_calculator_app() -> None:
    """
    Main function to run the calculator application.
    It orchestrates parsing arguments, displaying usage, and performing calculations.
    """
    calculator = Calculator()
    expression = parse_expression_from_arguments()

    if expression is None:
        display_usage()
        sys.exit(1)  # Exit with a non-zero status code to indicate an error (e.g., incorrect usage).

    execute_calculation_and_display_result(calculator, expression)


if __name__ == "__main__":
    run_calculator_app()
