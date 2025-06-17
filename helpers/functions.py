"""
Helper functions for use in the project.
"""

from typing import Any

def clamp(val: float, min_val: float, max_val: float) -> float:
    """
    Limits the input value `val` between `min_val` and `max_val`.
    """
    return max(min(val, max_val), min_val)

def assert_type(*args: Any,
                expected_type: type|tuple[type, ...],
                allow_none: bool=False) -> None:
    """
    Asserts that all the arguments in *args are of the expected types.
    """
    for arg in args:
        is_expected_type = isinstance(arg, expected_type)
        is_none_allowed = allow_none and (arg is None)
        assert is_expected_type or is_none_allowed, (
            f"Variable {arg}: Expected {expected_type}" +
            (" or None" if allow_none else "") + 
            f", got {type(arg).__name__}")

def assert_range(*args: Any,
                 more_than: float=float("-inf"),
                 less_than: float=float("inf")) -> None:
    """
    Asserts if the arguments in *args fall between the range of
    [more_than, less_than].
    If one of the values is missing, it assumes a simple less than or
    more than comparison.
    """
    for arg in args:
        assert isinstance(arg, float)
        assert more_than <= arg <= less_than
