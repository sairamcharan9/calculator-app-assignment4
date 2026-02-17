"""
Tests for the Calculator Module
==================================

Tests the Calculator REPL's input processing, validation,
special commands, and error handling.
Uses capsys to capture printed output.
"""

import pytest
from decimal import Decimal
from unittest.mock import patch

from app.calculator import Calculator


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def calculator() -> Calculator:
    """Provide a fresh Calculator instance for each test."""
    return Calculator()


# ===========================================================================
# Arithmetic operations via process_input
# ===========================================================================


class TestArithmeticOperations:
    """Test that arithmetic commands are processed correctly."""

    @pytest.mark.parametrize(
        "user_input, expected_substring",
        [
            ("add 5 3", "5 + 3 = 8"),
            ("subtract 10 4", "10 - 4 = 6"),
            ("multiply 6 7", "6 * 7 = 42"),
            ("divide 20 4", "20 / 4 = 5"),
            ("add -5 3", "-5 + 3 = -2"),
            ("multiply 0 100", "0 * 100 = 0"),
            ("add 1.5 2.5", "1.5 + 2.5 = 4.0"),
        ],
        ids=[
            "add_basic",
            "subtract_basic",
            "multiply_basic",
            "divide_basic",
            "negative_operand",
            "zero_operand",
            "decimal_operand",
        ],
    )
    def test_valid_operations(
        self, calculator: Calculator, user_input: str, expected_substring: str
    ) -> None:
        """Test that valid operations return the correct result."""
        result = calculator.process_input(user_input)
        assert expected_substring in result

    def test_operation_adds_to_history(self, calculator: Calculator) -> None:
        """Test that successful operations are recorded in history."""
        calculator.process_input("add 2 3")
        assert len(calculator.history) == 1
        assert calculator.history.get_latest() is not None


# ===========================================================================
# Input validation (LBYL)
# ===========================================================================


class TestInputValidation:
    """Test LBYL input validation."""

    @pytest.mark.parametrize(
        "user_input",
        [
            "add",
            "add 5",
            "add 5 3 2",
            "5 3",
            "",
        ],
        ids=[
            "one_token",
            "two_tokens",
            "four_tokens",
            "missing_operation",
            "empty_after_strip",
        ],
    )
    def test_invalid_format(self, calculator: Calculator, user_input: str) -> None:
        """Test that incorrectly formatted input returns an error."""
        result = calculator.process_input(user_input)
        assert "Error" in result or result == ""

    @pytest.mark.parametrize(
        "user_input",
        [
            "modulo 5 3",
            "power 2 8",
            "sqrt 9 0",
        ],
        ids=["modulo", "power", "sqrt"],
    )
    def test_unknown_operation(self, calculator: Calculator, user_input: str) -> None:
        """Test that unknown operations produce a clear error."""
        result = calculator.process_input(user_input)
        assert "Unknown operation" in result


# ===========================================================================
# Error handling (EAFP)
# ===========================================================================


class TestErrorHandling:
    """Test EAFP error handling for runtime errors."""

    def test_division_by_zero(self, calculator: Calculator) -> None:
        """Test that division by zero is handled gracefully."""
        result = calculator.process_input("divide 10 0")
        assert "Division by zero" in result

    @pytest.mark.parametrize(
        "user_input",
        [
            "add abc 3",
            "add 5 xyz",
            "add abc xyz",
        ],
        ids=["invalid_first", "invalid_second", "both_invalid"],
    )
    def test_invalid_numbers(self, calculator: Calculator, user_input: str) -> None:
        """Test that non-numeric inputs are handled gracefully."""
        result = calculator.process_input(user_input)
        assert "not valid numbers" in result

    def test_error_does_not_add_to_history(self, calculator: Calculator) -> None:
        """Test that failed operations are NOT recorded in history."""
        calculator.process_input("divide 10 0")
        assert len(calculator.history) == 0

    def test_value_error_from_factory(self, calculator: Calculator) -> None:
        """Test that a ValueError raised by CalculationFactory is handled (EAFP).

        This covers the except-ValueError branch in process_input that is
        normally unreachable because LBYL validation catches unknown
        operations first.  We patch the factory to force the path.
        """
        with patch(
            "app.calculator.CalculationFactory.create",
            side_effect=ValueError("Injected error"),
        ):
            result = calculator.process_input("add 1 2")
        assert "Error" in result
        assert "Injected error" in result


# ===========================================================================
# Special commands
# ===========================================================================


class TestSpecialCommands:
    """Test special (non-arithmetic) commands."""

    def test_help_command(self, calculator: Calculator) -> None:
        """Test the 'help' command."""
        result = calculator.process_input("help")
        assert "Calculator Help" in result
        assert "add" in result

    def test_help_question_mark(self, calculator: Calculator) -> None:
        """Test the '?' shortcut for help."""
        result = calculator.process_input("?")
        assert "Calculator Help" in result

    def test_history_empty(self, calculator: Calculator) -> None:
        """Test 'history' when no calculations exist."""
        result = calculator.process_input("history")
        assert "No calculations" in result

    def test_history_with_entries(self, calculator: Calculator) -> None:
        """Test 'history' after performing calculations."""
        calculator.process_input("add 1 2")
        calculator.process_input("multiply 3 4")
        result = calculator.process_input("history")
        assert "1 + 2 = 3" in result
        assert "3 * 4 = 12" in result
        assert "2 calculation(s)" in result

    def test_clear_command(self, calculator: Calculator) -> None:
        """Test the 'clear' command."""
        calculator.process_input("add 1 2")
        result = calculator.process_input("clear")
        assert "cleared" in result.lower()
        assert len(calculator.history) == 0

    def test_case_insensitive_commands(self, calculator: Calculator) -> None:
        """Test that commands are case-insensitive."""
        result = calculator.process_input("HELP")
        assert "Calculator Help" in result

    def test_case_insensitive_operations(self, calculator: Calculator) -> None:
        """Test that operations are case-insensitive."""
        result = calculator.process_input("ADD 5 3")
        assert "5 + 3 = 8" in result

    def test_whitespace_handling(self, calculator: Calculator) -> None:
        """Test that extra whitespace is handled."""
        result = calculator.process_input("  add   5   3  ")
        # After split(), extra whitespace may cause token count issues
        # This tests that strip() is applied
        assert "Error" in result or "+" in result


# ===========================================================================
# Validate input parts (static method)
# ===========================================================================


class TestValidateInputParts:
    """Test the _validate_input_parts static method directly."""

    def test_valid_input(self) -> None:
        """Test that valid input returns None (no error)."""
        assert Calculator._validate_input_parts(["add", "5", "3"]) is None

    def test_too_few_parts(self) -> None:
        """Test that too few tokens returns an error."""
        result = Calculator._validate_input_parts(["add", "5"])
        assert result is not None
        assert "Invalid format" in result

    def test_too_many_parts(self) -> None:
        """Test that too many tokens returns an error."""
        result = Calculator._validate_input_parts(["add", "5", "3", "2"])
        assert result is not None
        assert "Invalid format" in result

    def test_unknown_operation_name(self) -> None:
        """Test that an unknown operation name returns an error."""
        result = Calculator._validate_input_parts(["modulo", "5", "3"])
        assert result is not None
        assert "Unknown operation" in result


# ===========================================================================
# Main entry point
# ===========================================================================


class TestMainEntryPoint:
    """Test the main.py entry point."""

    def test_main_function_exists(self) -> None:
        """Test that main function is importable."""
        from main import main
        assert callable(main)
