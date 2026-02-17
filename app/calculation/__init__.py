"""
Calculation Module
==================

Provides the core data model for calculations:

- **Calculation**: Represents a single arithmetic calculation with two operands
  and an operation, computing and storing the result.
- **CalculationFactory**: Factory class that creates ``Calculation`` instances
  from string-based operation names (Factory Pattern).
- **CalculationHistory**: Manages a session-level list of past calculations.
"""

from decimal import Decimal
from typing import Callable, List, Optional

from app.operation import add, subtract, multiply, divide


class Calculation:
    """Represents a single arithmetic calculation.

    Attributes:
        operand_a: The first operand.
        operand_b: The second operand.
        operation: The callable that performs the arithmetic.
        operation_name: A human-readable name for the operation.
        result: The computed result.
    """

    def __init__(
        self,
        operand_a: Decimal,
        operand_b: Decimal,
        operation: Callable[[Decimal, Decimal], Decimal],
        operation_name: str,
    ) -> None:
        """Initialize and immediately compute the calculation.

        Args:
            operand_a: The first operand.
            operand_b: The second operand.
            operation: A callable that takes two Decimals and returns a Decimal.
            operation_name: Human-readable name (e.g., "add").

        Raises:
            ZeroDivisionError: If the operation is division and operand_b is 0.
        """
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.operation = operation
        self.operation_name = operation_name
        self.result = operation(operand_a, operand_b)

    def __repr__(self) -> str:
        """Return a detailed string representation of the calculation."""
        return (
            f"Calculation({self.operand_a}, {self.operand_b}, "
            f"{self.operation_name}) = {self.result}"
        )

    def __str__(self) -> str:
        """Return a user-friendly string of the calculation."""
        symbols = {"add": "+", "subtract": "-", "multiply": "*", "divide": "/"}
        symbol = symbols.get(self.operation_name, self.operation_name)
        return f"{self.operand_a} {symbol} {self.operand_b} = {self.result}"


class CalculationFactory:
    """Factory that creates Calculation instances from string operation names.

    Maps operation name strings to their corresponding callables,
    implementing the Factory and Strategy patterns.
    """

    # Class-level mapping of operation names to functions (Strategy Pattern)
    _operations: dict[str, Callable[[Decimal, Decimal], Decimal]] = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }

    @classmethod
    def create(
        cls, operand_a: Decimal, operand_b: Decimal, operation_name: str
    ) -> "Calculation":
        """Create a Calculation from an operation name string.

        Args:
            operand_a: The first operand.
            operand_b: The second operand.
            operation_name: Name of the operation (add, subtract, multiply, divide).

        Returns:
            A Calculation instance with the result already computed.

        Raises:
            ValueError: If the operation_name is not recognized.
            ZeroDivisionError: If dividing by zero.
        """
        operation = cls._operations.get(operation_name)
        if operation is None:
            supported = ", ".join(cls._operations.keys())
            raise ValueError(
                f"Unknown operation '{operation_name}'. "
                f"Supported operations: {supported}"
            )
        return Calculation(operand_a, operand_b, operation, operation_name)

    @classmethod
    def get_supported_operations(cls) -> list[str]:
        """Return a list of supported operation names.

        Returns:
            List of operation name strings.
        """
        return list(cls._operations.keys())


class CalculationHistory:
    """Maintains a history of Calculation objects for the current session.

    Provides methods to add, retrieve, and clear calculation history.
    """

    def __init__(self) -> None:
        """Initialize an empty history."""
        self._history: List[Calculation] = []

    def add(self, calculation: Calculation) -> None:
        """Add a calculation to the history.

        Args:
            calculation: The Calculation instance to store.
        """
        self._history.append(calculation)

    def get_all(self) -> List[Calculation]:
        """Return all calculations in the history.

        Returns:
            A list of all Calculation objects, in order.
        """
        return list(self._history)

    def get_latest(self) -> Optional[Calculation]:
        """Return the most recent calculation, or None if history is empty.

        Returns:
            The last Calculation, or None.
        """
        return self._history[-1] if self._history else None

    def clear(self) -> None:
        """Clear all calculations from the history."""
        self._history.clear()

    def __len__(self) -> int:
        """Return the number of calculations in the history."""
        return len(self._history)

    def __repr__(self) -> str:
        """Return a string representation of the history."""
        return f"CalculationHistory({len(self._history)} calculations)"
