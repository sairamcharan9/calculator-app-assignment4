"""
Tests for the Calculation Module
===================================

Parameterized tests covering Calculation, CalculationFactory,
and CalculationHistory classes with positive and negative cases.
"""

import pytest
from decimal import Decimal

from app.operation import add, subtract, multiply, divide
from app.calculation import Calculation, CalculationFactory, CalculationHistory


# ===========================================================================
# Calculation class tests
# ===========================================================================


class TestCalculation:
    """Tests for the Calculation data class."""

    @pytest.mark.parametrize(
        "a, b, operation, op_name, expected",
        [
            (Decimal("5"), Decimal("3"), add, "add", Decimal("8")),
            (Decimal("10"), Decimal("4"), subtract, "subtract", Decimal("6")),
            (Decimal("6"), Decimal("7"), multiply, "multiply", Decimal("42")),
            (Decimal("20"), Decimal("4"), divide, "divide", Decimal("5")),
        ],
        ids=["add", "subtract", "multiply", "divide"],
    )
    def test_calculation_computes_result(
        self, a: Decimal, b: Decimal, operation, op_name: str, expected: Decimal
    ) -> None:
        """Test that Calculation computes the correct result on creation."""
        calc = Calculation(a, b, operation, op_name)
        assert calc.result == expected
        assert calc.operand_a == a
        assert calc.operand_b == b
        assert calc.operation_name == op_name

    def test_calculation_repr(self) -> None:
        """Test the repr output of a Calculation."""
        calc = Calculation(Decimal("2"), Decimal("3"), add, "add")
        assert "Calculation" in repr(calc)
        assert "add" in repr(calc)
        assert "5" in repr(calc)

    @pytest.mark.parametrize(
        "a, b, operation, op_name, expected_symbol",
        [
            (Decimal("5"), Decimal("3"), add, "add", "+"),
            (Decimal("10"), Decimal("4"), subtract, "subtract", "-"),
            (Decimal("6"), Decimal("7"), multiply, "multiply", "*"),
            (Decimal("20"), Decimal("4"), divide, "divide", "/"),
        ],
        ids=["add_symbol", "subtract_symbol", "multiply_symbol", "divide_symbol"],
    )
    def test_calculation_str(
        self, a: Decimal, b: Decimal, operation, op_name: str, expected_symbol: str
    ) -> None:
        """Test the user-friendly string representation."""
        calc = Calculation(a, b, operation, op_name)
        result_str = str(calc)
        assert expected_symbol in result_str
        assert "=" in result_str

    def test_calculation_str_unknown_operation(self) -> None:
        """Test str when operation_name is not in the symbol map."""
        calc = Calculation(Decimal("2"), Decimal("3"), add, "custom_op")
        result_str = str(calc)
        assert "custom_op" in result_str

    def test_calculation_division_by_zero(self) -> None:
        """Test that creating a division-by-zero Calculation raises."""
        with pytest.raises(ZeroDivisionError):
            Calculation(Decimal("10"), Decimal("0"), divide, "divide")


# ===========================================================================
# CalculationFactory tests
# ===========================================================================


class TestCalculationFactory:
    """Tests for the CalculationFactory."""

    @pytest.mark.parametrize(
        "op_name, a, b, expected",
        [
            ("add", Decimal("2"), Decimal("3"), Decimal("5")),
            ("subtract", Decimal("10"), Decimal("3"), Decimal("7")),
            ("multiply", Decimal("4"), Decimal("5"), Decimal("20")),
            ("divide", Decimal("10"), Decimal("2"), Decimal("5")),
        ],
        ids=["factory_add", "factory_subtract", "factory_multiply", "factory_divide"],
    )
    def test_create_valid_operations(
        self, op_name: str, a: Decimal, b: Decimal, expected: Decimal
    ) -> None:
        """Test that the factory creates Calculation instances correctly."""
        calc = CalculationFactory.create(a, b, op_name)
        assert calc.result == expected
        assert calc.operation_name == op_name

    def test_create_unknown_operation(self) -> None:
        """Test that an unknown operation raises ValueError."""
        with pytest.raises(ValueError, match="Unknown operation"):
            CalculationFactory.create(Decimal("1"), Decimal("2"), "modulo")

    def test_create_division_by_zero(self) -> None:
        """Test that factory propagates ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            CalculationFactory.create(Decimal("10"), Decimal("0"), "divide")

    def test_get_supported_operations(self) -> None:
        """Test that all four operations are returned."""
        operations = CalculationFactory.get_supported_operations()
        assert "add" in operations
        assert "subtract" in operations
        assert "multiply" in operations
        assert "divide" in operations
        assert len(operations) == 4


# ===========================================================================
# CalculationHistory tests
# ===========================================================================


class TestCalculationHistory:
    """Tests for the CalculationHistory."""

    def test_empty_history(self) -> None:
        """Test that a new history is empty."""
        history = CalculationHistory()
        assert len(history) == 0
        assert history.get_all() == []
        assert history.get_latest() is None

    def test_add_and_retrieve(self) -> None:
        """Test adding a calculation and retrieving it."""
        history = CalculationHistory()
        calc = Calculation(Decimal("2"), Decimal("3"), add, "add")
        history.add(calc)
        assert len(history) == 1
        assert history.get_latest() == calc
        assert history.get_all() == [calc]

    def test_multiple_calculations(self) -> None:
        """Test that multiple calculations are stored in order."""
        history = CalculationHistory()
        calc1 = Calculation(Decimal("1"), Decimal("2"), add, "add")
        calc2 = Calculation(Decimal("5"), Decimal("3"), subtract, "subtract")
        history.add(calc1)
        history.add(calc2)
        assert len(history) == 2
        assert history.get_latest() == calc2
        assert history.get_all() == [calc1, calc2]

    def test_clear_history(self) -> None:
        """Test clearing the history."""
        history = CalculationHistory()
        history.add(Calculation(Decimal("1"), Decimal("2"), add, "add"))
        history.clear()
        assert len(history) == 0
        assert history.get_latest() is None

    def test_repr(self) -> None:
        """Test the repr of CalculationHistory."""
        history = CalculationHistory()
        assert "0 calculations" in repr(history)
        history.add(Calculation(Decimal("1"), Decimal("2"), add, "add"))
        assert "1 calculations" in repr(history)
