"""Tests for the calculator module."""

import pytest

from app.calculator import (
    Calculator,
    CalculationResult,
    DivisionByZeroError,
    Operation,
)


@pytest.fixture
def calc() -> Calculator:
    """Provide a fresh calculator instance."""
    return Calculator()


class TestAdd:
    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (2, 3, 5),
            (0, 0, 0),
            (-1, 1, 0),
            (0.1, 0.2, pytest.approx(0.3)),
            (-5, -3, -8),
        ],
    )
    def test_add(self, calc: Calculator, a: float, b: float, expected: float) -> None:
        result = calc.add(a, b)
        assert result.result == expected
        assert result.operation == Operation.ADD

    def test_add_records_history(self, calc: Calculator) -> None:
        calc.add(1, 2)
        calc.add(3, 4)
        assert len(calc.history) == 2


class TestSubtract:
    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (5, 3, 2),
            (0, 0, 0),
            (-1, -1, 0),
            (10, 20, -10),
        ],
    )
    def test_subtract(self, calc: Calculator, a: float, b: float, expected: float) -> None:
        result = calc.subtract(a, b)
        assert result.result == expected


class TestMultiply:
    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (2, 3, 6),
            (0, 100, 0),
            (-2, 3, -6),
            (-2, -3, 6),
        ],
    )
    def test_multiply(self, calc: Calculator, a: float, b: float, expected: float) -> None:
        result = calc.multiply(a, b)
        assert result.result == expected


class TestDivide:
    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (6, 3, 2),
            (7, 2, 3.5),
            (-6, 3, -2),
            (0, 5, 0),
        ],
    )
    def test_divide(self, calc: Calculator, a: float, b: float, expected: float) -> None:
        result = calc.divide(a, b)
        assert result.result == expected

    def test_divide_by_zero_raises(self, calc: Calculator) -> None:
        with pytest.raises(DivisionByZeroError, match="Cannot divide by zero"):
            calc.divide(1, 0)


class TestSumAll:
    def test_sum_multiple(self, calc: Calculator) -> None:
        result = calc.sum_all([1, 2, 3, 4])
        assert result.result == 10

    def test_sum_single(self, calc: Calculator) -> None:
        result = calc.sum_all([42])
        assert result.result == 42

    def test_sum_empty_raises(self, calc: Calculator) -> None:
        with pytest.raises(ValueError, match="empty sequence"):
            calc.sum_all([])


class TestHistory:
    def test_history_is_immutable(self, calc: Calculator) -> None:
        calc.add(1, 2)
        history = calc.history
        assert isinstance(history, tuple)

    def test_clear_history(self, calc: Calculator) -> None:
        calc.add(1, 2)
        calc.clear_history()
        assert len(calc.history) == 0


class TestCalculationResult:
    def test_str_representation(self) -> None:
        result = CalculationResult(
            operation=Operation.ADD,
            operands=(2, 3),
            result=5,
        )
        assert str(result) == "2 + 3 = 5"

    def test_frozen(self) -> None:
        result = CalculationResult(
            operation=Operation.ADD,
            operands=(1, 2),
            result=3,
        )
        with pytest.raises(AttributeError):
            result.result = 99  # type: ignore[misc]
