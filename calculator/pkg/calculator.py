
from collections.abc import Callable


class Calculator:
    def __init__(self) -> None:
        """
        Initializes the Calculator with supported operators, their
        corresponding functions, and precedence levels.
        """
        self.operators: dict[str, Callable[[float, float], float]] = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        # Precedence for operators: higher number means higher precedence.
        self.precedence: dict[str, int] = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression: str) -> float | None:
        """
        Evaluates a mathematical expression given as a string.

        Args:
            expression: The mathematical expression to evaluate.

        Returns:
            The result of the evaluation as a float, or None if the expression
            is empty or contains only whitespace.

        Raises:
            ValueError: If the expression is invalid (e.g., contains invalid tokens,
                        is malformed, or has division by zero).
        """
        if not expression or expression.isspace():
            return None
        # Tokenize the expression by splitting on spaces.
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens: list[str]) -> float:
        """
        Evaluates an infix expression using the Shunting-Yard algorithm principle.
        It converts the infix expression to a postfix-like evaluation order.

        Args:
            tokens: A list of strings representing the tokens of the expression.

        Returns:
            The numerical result of the expression.

        Raises:
            ValueError: If the expression is malformed, contains invalid tokens,
                        or has an insufficient number of operands for an operator.
        """
        values: list[float] = []  # Stack for numbers
        operators: list[str] = []  # Stack for operators

        for token in tokens:
            if token in self.operators:
                # While there are operators on the operator stack with greater
                # or equal precedence, apply them to the value stack.
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    # Attempt to convert the token to a float and push to the value stack.
                    values.append(float(token))
                except ValueError:
                    # Handle cases where a token is neither an operator nor a valid number.
                    raise ValueError(f"Error: Invalid token '{token}' in expression.")

        # After processing all tokens, apply any remaining operators in the stack.
        while operators:
            self._apply_operator(operators, values)

        # A valid expression should result in exactly one value on the value stack.
        if len(values) != 1:
            raise ValueError("Error: Invalid expression format.")

        return values[0]

    def _apply_operator(self, operators: list[str], values: list[float]) -> None:
        """
        Pops an operator from the operator stack and two operands from the value stack,
        performs the operation, and pushes the result back onto the value stack.

        Args:
            operators: The stack of operators.
            values: The stack of numerical values.

        Raises:
            ValueError: If there are insufficient operands on the value stack
                        for the operator to be applied.
            ZeroDivisionError: If a division by zero occurs.
        """
        if not operators:
            # Should not happen in a well-formed evaluation, but added for robustness.
            return

        operator = operators.pop()
        # Ensure there are enough operands for the binary operator.
        if len(values) < 2:
            raise ValueError(f"Error: Not enough operands for operator '{operator}'.")

        # Pop operands in the correct order (b then a for a op b).
        b = values.pop()
        a = values.pop()
        try:
            result = self.operators[operator](a, b)
            values.append(result)
        except ZeroDivisionError:
            # Catch division by zero specifically and re-raise with a custom message.
            raise ValueError("Error: Division by zero is not allowed.")
