"""A clean calculator module demonstrating good Python practices."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence


class CalculatorError(Exception):
    """Base exception for calculator operations."""


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""


class InvalidOperationError(CalculatorError):
    """Raised when an unsupported operation is requested."""


class Operation(Enum):
    """Supported arithmetic operations."""

    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


@dataclass(frozen=True)
class CalculationResult:
    """Immutable result of a calculation."""

    operation: Operation
    operands: tuple[float, ...]
    result: float

    def __str__(self) -> str:
        op_symbol = {
            Operation.ADD: "+",
            Operation.SUBTRACT: "-",
            Operation.MULTIPLY: "*",
            Operation.DIVIDE: "/",
        }
        symbol = op_symbol[self.operation]
        expr = f" {symbol} ".join(str(op) for op in self.operands)
        return f"{expr} = {self.result}"


class Calculator:
    """A stateful calculator that keeps a history of operations.

    Example usage::

        calc = Calculator()
        result = calc.add(2, 3)
        assert result.result == 5
        assert len(calc.history) == 1
    """

    def __init__(self) -> None:
        self._history: list[CalculationResult] = []

    @property
    def history(self) -> tuple[CalculationResult, ...]:
        """Return an immutable view of calculation history."""
        return tuple(self._history)

    def clear_history(self) -> None:
        """Clear all calculation history."""
        self._history.clear()

    def add(self, a: float, b: float) -> CalculationResult:
        """Add two numbers."""
        return self._record(Operation.ADD, (a, b), a + b)

    def subtract(self, a: float, b: float) -> CalculationResult:
        """Subtract b from a."""
        return self._record(Operation.SUBTRACT, (a, b), a - b)

    def multiply(self, a: float, b: float) -> CalculationResult:
        """Multiply two numbers."""
        return self._record(Operation.MULTIPLY, (a, b), a * b)

    def divide(self, a: float, b: float) -> CalculationResult:
        """Divide a by b.

        Raises:
            DivisionByZeroError: If b is zero.
        """
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return self._record(Operation.DIVIDE, (a, b), a / b)

    def sum_all(self, numbers: Sequence[float]) -> CalculationResult:
        """Sum a sequence of numbers.

        Raises:
            ValueError: If the sequence is empty.
        """
        if not numbers:
            raise ValueError("Cannot sum an empty sequence")
        total = sum(numbers)
        return self._record(Operation.ADD, tuple(numbers), total)

    def _record(
        self,
        operation: Operation,
        operands: tuple[float, ...],
        result: float,
    ) -> CalculationResult:
        """Record a calculation and return the result."""
        calc_result = CalculationResult(
            operation=operation,
            operands=operands,
            result=result,
        )
        self._history.append(calc_result)
        return calc_result
