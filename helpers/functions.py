"""
Helper functions for use in the project.
"""

def clamp(val: float, min_val: float, max_val: float) -> float:
    """
    Limits the input value `val` between `min_val` and `max_val`.
    """
    return max(min(val, max_val), min_val)
