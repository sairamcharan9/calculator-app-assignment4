"""
Tests for the Operation Module
================================

Parameterized tests covering all four arithmetic operations:
add, subtract, multiply, divide — including edge cases
(zero, negative numbers, decimals, large numbers, division by zero).
"""

import pytest
from decimal import Decimal

from app.operation import add, subtract, multiply, divide


# ---------------------------------------------------------------------------
# Parameterized tests for add
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("2"), Decimal("3"), Decimal("5")),
        (Decimal("0"), Decimal("0"), Decimal("0")),
        (Decimal("-1"), Decimal("1"), Decimal("0")),
        (Decimal("-5"), Decimal("-3"), Decimal("-8")),
        (Decimal("1.5"), Decimal("2.5"), Decimal("4.0")),
        (Decimal("100"), Decimal("200"), Decimal("300")),
        (Decimal("999999999"), Decimal("1"), Decimal("1000000000")),
        (Decimal("0.1"), Decimal("0.2"), Decimal("0.3")),
    ],
    ids=[
        "positive+positive",
        "zero+zero",
        "negative+positive",
        "negative+negative",
        "decimal+decimal",
        "large+large",
        "large_boundary",
        "small_decimals",
    ],
)
def test_add(a: Decimal, b: Decimal, expected: Decimal) -> None:
    """Test addition with various input scenarios."""
    assert add(a, b) == expected


# ---------------------------------------------------------------------------
# Parameterized tests for subtract
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("5"), Decimal("3"), Decimal("2")),
        (Decimal("0"), Decimal("0"), Decimal("0")),
        (Decimal("-1"), Decimal("-1"), Decimal("0")),
        (Decimal("3"), Decimal("5"), Decimal("-2")),
        (Decimal("10.5"), Decimal("0.5"), Decimal("10.0")),
        (Decimal("1000"), Decimal("1"), Decimal("999")),
    ],
    ids=[
        "positive-positive",
        "zero-zero",
        "negative-negative",
        "result_negative",
        "decimal_subtraction",
        "large_subtraction",
    ],
)
def test_subtract(a: Decimal, b: Decimal, expected: Decimal) -> None:
    """Test subtraction with various input scenarios."""
    assert subtract(a, b) == expected


# ---------------------------------------------------------------------------
# Parameterized tests for multiply
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("4"), Decimal("3"), Decimal("12")),
        (Decimal("0"), Decimal("100"), Decimal("0")),
        (Decimal("-2"), Decimal("3"), Decimal("-6")),
        (Decimal("-3"), Decimal("-4"), Decimal("12")),
        (Decimal("1.5"), Decimal("2"), Decimal("3.0")),
        (Decimal("1000"), Decimal("1000"), Decimal("1000000")),
    ],
    ids=[
        "positive*positive",
        "zero_factor",
        "negative*positive",
        "negative*negative",
        "decimal*integer",
        "large_multiplication",
    ],
)
def test_multiply(a: Decimal, b: Decimal, expected: Decimal) -> None:
    """Test multiplication with various input scenarios."""
    assert multiply(a, b) == expected


# ---------------------------------------------------------------------------
# Parameterized tests for divide
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (Decimal("10"), Decimal("2"), Decimal("5")),
        (Decimal("7"), Decimal("2"), Decimal("3.5")),
        (Decimal("0"), Decimal("5"), Decimal("0")),
        (Decimal("-10"), Decimal("2"), Decimal("-5")),
        (Decimal("-10"), Decimal("-2"), Decimal("5")),
        (Decimal("1"), Decimal("3"), Decimal("1") / Decimal("3")),
    ],
    ids=[
        "even_division",
        "decimal_result",
        "zero_dividend",
        "negative_dividend",
        "both_negative",
        "repeating_decimal",
    ],
)
def test_divide(a: Decimal, b: Decimal, expected: Decimal) -> None:
    """Test division with various input scenarios."""
    assert divide(a, b) == expected


def test_divide_by_zero() -> None:
    """Test that dividing by zero raises ZeroDivisionError (EAFP)."""
    with pytest.raises(ZeroDivisionError):
        divide(Decimal("10"), Decimal("0"))
