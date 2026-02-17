"""
Operation Module
================

Provides basic arithmetic operations as static methods.
Each operation takes two numeric values and returns the result.

This module demonstrates the EAFP (Easier to Ask Forgiveness than Permission)
paradigm for error handling — division does not pre-check for zero; instead,
callers handle the ZeroDivisionError exception.
"""

from decimal import Decimal, InvalidOperation


def add(a: Decimal, b: Decimal) -> Decimal:
    """Return the sum of two numbers.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The sum a + b.

    Examples:
        >>> add(Decimal('2'), Decimal('3'))
        Decimal('5')
    """
    return a + b


def subtract(a: Decimal, b: Decimal) -> Decimal:
    """Return the difference of two numbers.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The difference a - b.

    Examples:
        >>> subtract(Decimal('5'), Decimal('3'))
        Decimal('2')
    """
    return a - b


def multiply(a: Decimal, b: Decimal) -> Decimal:
    """Return the product of two numbers.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The product a * b.

    Examples:
        >>> multiply(Decimal('4'), Decimal('3'))
        Decimal('12')
    """
    return a * b


def divide(a: Decimal, b: Decimal) -> Decimal:
    """Return the quotient of two numbers.

    Uses EAFP: does not pre-check for zero divisor.
    Raises ZeroDivisionError if b is zero, which the caller
    should handle.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The quotient a / b.

    Raises:
        ZeroDivisionError: If b is zero.

    Examples:
        >>> divide(Decimal('10'), Decimal('2'))
        Decimal('5')
    """
    return a / b
