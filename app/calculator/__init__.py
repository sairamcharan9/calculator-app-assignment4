"""
Calculator Module
=================

Provides the ``Calculator`` class, which implements a Read-Eval-Print Loop
(REPL) for continuous user interaction with the calculator.

Features:
    - Arithmetic operations via user-friendly commands
    - Input validation using **LBYL** (Look Before You Leap)
    - Error handling using **EAFP** (Easier to Ask Forgiveness than Permission)
    - Special commands: help, history, clear, exit
    - Calculation history tracking
"""

from decimal import Decimal, InvalidOperation

from app.calculation import CalculationFactory, CalculationHistory


class Calculator:
    """Interactive calculator with a REPL interface.

    Supports add, subtract, multiply, and divide operations,
    maintains a history of calculations, and provides special
    commands for user convenience.

    Attributes:
        history: The CalculationHistory instance for this session.
    """

    # Special (non-arithmetic) commands
    SPECIAL_COMMANDS = ("help", "history", "clear", "exit")

    def __init__(self) -> None:
        """Initialize the calculator with an empty history."""
        self.history = CalculationHistory()

    # ------------------------------------------------------------------
    # REPL
    # ------------------------------------------------------------------

    def run(self) -> None:  # pragma: no cover
        """Start the Read-Eval-Print Loop.

        Continuously prompts the user for input until they type 'exit'.
        """
        self._print_welcome()
        while True:
            try:
                user_input = input("\n>>> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            self.process_input(user_input)

    # ------------------------------------------------------------------
    # Input processing (public so tests can call it directly)
    # ------------------------------------------------------------------

    def process_input(self, user_input: str) -> str:
        """Parse and execute a single line of user input.

        Uses **LBYL** to validate the input format before attempting
        to create a calculation, and **EAFP** to handle runtime
        errors (invalid numbers, division by zero).

        Args:
            user_input: The raw string entered by the user.

        Returns:
            A feedback message string describing the result or error.
        """
        command = user_input.strip().lower()

        # --- Handle special commands ---
        if command in ("help", "?"):
            return self._handle_help()
        if command == "history":
            return self._handle_history()
        if command == "clear":
            return self._handle_clear()

        # --- LBYL: validate input format before processing ---
        parts = command.split()
        validation_error = self._validate_input_parts(parts)
        if validation_error:
            print(validation_error)
            return validation_error

        operation_name, raw_a, raw_b = parts[0], parts[1], parts[2]

        # --- EAFP: attempt numeric conversion and calculation ---
        try:
            operand_a = Decimal(raw_a)
            operand_b = Decimal(raw_b)
        except InvalidOperation:
            msg = (
                f"Error: '{raw_a}' and/or '{raw_b}' are not valid numbers. "
                "Please enter numeric values."
            )
            print(msg)
            return msg

        try:
            calc = CalculationFactory.create(operand_a, operand_b, operation_name)
        except ZeroDivisionError:
            msg = "Error: Division by zero is not allowed."
            print(msg)
            return msg
        except ValueError as exc:
            msg = f"Error: {exc}"
            print(msg)
            return msg

        self.history.add(calc)
        result_msg = f"Result: {calc}"
        print(result_msg)
        return result_msg

    # ------------------------------------------------------------------
    # LBYL validation helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_input_parts(parts: list[str]) -> str | None:
        """Validate that the input has the correct format (LBYL).

        Checks:
            1. Exactly three tokens are present.
            2. The first token is a recognized operation name.

        Args:
            parts: The tokenized user input.

        Returns:
            An error message string if invalid, or None if valid.
        """
        if len(parts) != 3:
            return (
                "Error: Invalid format. Please use: <operation> <number1> <number2>\n"
                "Example: add 5 3\n"
                "Type 'help' for available commands."
            )

        valid_operations = CalculationFactory.get_supported_operations()
        if parts[0] not in valid_operations:
            return (
                f"Error: Unknown operation '{parts[0]}'.\n"
                f"Available operations: {', '.join(valid_operations)}\n"
                "Type 'help' for more information."
            )

        return None

    # ------------------------------------------------------------------
    # Special command handlers
    # ------------------------------------------------------------------

    def _handle_help(self) -> str:
        """Display help information.

        Returns:
            The help text.
        """
        operations = CalculationFactory.get_supported_operations()
        help_text = (
            "=== Calculator Help ===\n"
            "\n"
            "Usage: <operation> <number1> <number2>\n"
            "\n"
            f"Operations: {', '.join(operations)}\n"
            "\n"
            "Examples:\n"
            "  add 5 3        => 5 + 3 = 8\n"
            "  subtract 10 4  => 10 - 4 = 6\n"
            "  multiply 6 7   => 6 * 7 = 42\n"
            "  divide 20 4    => 20 / 4 = 5\n"
            "\n"
            "Special commands:\n"
            "  help / ?   - Show this help message\n"
            "  history    - Show calculation history\n"
            "  clear      - Clear calculation history\n"
            "  exit       - Exit the calculator"
        )
        print(help_text)
        return help_text

    def _handle_history(self) -> str:
        """Display the calculation history.

        Returns:
            The formatted history or a 'no history' message.
        """
        calculations = self.history.get_all()
        if not calculations:
            msg = "No calculations in history."
            print(msg)
            return msg

        lines = ["=== Calculation History ==="]
        for i, calc in enumerate(calculations, start=1):
            lines.append(f"  {i}. {calc}")
        lines.append(f"\nTotal: {len(calculations)} calculation(s)")
        history_text = "\n".join(lines)
        print(history_text)
        return history_text

    def _handle_clear(self) -> str:
        """Clear the calculation history.

        Returns:
            A confirmation message.
        """
        self.history.clear()
        msg = "History cleared."
        print(msg)
        return msg

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _print_welcome() -> None:  # pragma: no cover
        """Print the welcome banner when the REPL starts."""
        print(
            "================================\n"
            "   Welcome to the Calculator!\n"
            "================================\n"
            "Type 'help' for available commands.\n"
            "Type 'exit' to quit."
        )
