# Cái file này là file unit test của tool calculator

from __future__ import annotations

import pytest

from tools.calculator.tool import calculate


@pytest.mark.parametrize(
    ("a", "b", "operation", "expected"),
    [
        (2, 3, "add", 5),
        (7, 4, "subtract", 3),
        (6, 5, "multiply", 30),
        (8, 2, "divide", 4),
    ],
)
def test_calculate_supported_operations(a: int, b: int, operation: str, expected: int | float) -> None:
    result = calculate(a=a, b=b, operation=operation)

    assert result["result"] == expected


def test_calculate_division_by_zero_returns_error() -> None:
    result = calculate(a=1, b=0, operation="divide")

    assert result["error"] == "ZeroDivisionError"


def test_calculate_unsupported_operation_returns_error() -> None:
    result = calculate(a=1, b=2, operation="power")

    assert result["error"] == "ValueError"
