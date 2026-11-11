from __future__ import annotations

import math
import operator
from typing import Any

from tools._shared import err


_OPERATIONS = {
    "add": operator.add,
    "subtract": operator.sub,
    "multiply": operator.mul,
    "divide": operator.truediv,
}


def calculate(
    a: int | float | None = None,
    b: int | float | None = None,
    operation: str = "",
) -> dict[str, Any]:
    try:
        if isinstance(a, bool) or not isinstance(a, (int, float)):
            raise ValueError("a must be a number")
        if isinstance(b, bool) or not isinstance(b, (int, float)):
            raise ValueError("b must be a number")
        if not math.isfinite(a) or not math.isfinite(b):
            raise ValueError("a and b must be finite numbers")
        if operation not in _OPERATIONS:
            raise ValueError("operation must be add, subtract, multiply, or divide")

        result = _OPERATIONS[operation](a, b)
        if isinstance(result, float) and not math.isfinite(result):
            raise ValueError("result must be a finite number")
        return {
            "tool": "calculator",
            "a": a,
            "b": b,
            "operation": operation,
            "result": result,
        }
    except (ArithmeticError, TypeError, ValueError) as exc:
        return err("calculator", exc)
