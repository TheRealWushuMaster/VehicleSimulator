"""
Helper functions for use in the project.
"""

from typing import Any, Callable
from simulation.constants import RPM_TO_ANG_VEL, ANG_VEL_TO_RPM, \
    CUBIC_METERS_TO_LTS, LTS_TO_CUBIC_METERS

def clamp(val: float, min_val: float, max_val: float) -> float:
    """
    Limits the input value `val` between `min_val` and `max_val`.
    """
    return max(min(val, max_val), min_val)

# CALCULATIONS

def electric_power(voltage: float,
                   current: float) -> float:
    """
    Returns the power in an electric exchange.
    When the signal is AC, the values of `voltage`
    and `current` must be effective values.
    """
    assert_type_and_range(voltage, current,
                          more_than=0.0)
    return voltage * current

# VERIFICATIONS

def assert_callable(*args: Any,
                    allow_none: bool=False) -> None:
    """
    Asserts that all the arguments in *args are of type Callable.
    """
    assert isinstance(allow_none, bool)
    assert_type(args,
                expected_type=Callable,  # type: ignore[arg-type]
                allow_none=allow_none)

def assert_type(*args: Any,
                expected_type: type|tuple[type, ...],
                allow_none: bool=False) -> None:
    """
    Asserts that all the arguments in *args are of the expected types.
    """
    assert isinstance(expected_type, (type, tuple))
    assert isinstance(allow_none, bool)
    for arg in args:
        is_expected_type = isinstance(arg, expected_type)  # type: ignore[arg-type]
        if isinstance(expected_type, tuple):
            is_expected_class = arg in expected_type
        else:
            is_expected_class = arg is expected_type
        is_none_allowed = allow_none and (arg is None)
        assert is_expected_type or is_expected_class or is_none_allowed, (
            f"Variable {arg}: Expected {expected_type}" +
            (" or None" if allow_none else "") + 
            f", got {type(arg).__name__}")

def assert_range(*args: Any,
                 more_than: float=float("-inf"),
                 less_than: float=float("inf"),
                 include_more: bool=True,
                 include_less: bool=True,
                 allow_none: bool=False) -> None:
    """
    Asserts if the arguments in *args are of type float and fall
    between the range of [`more_than`, `less_than`].
    The `include_more` and `include_less` control if the limits are
    included in the comparison.
    If one of the values is missing, it assumes a simple less than or
    more than comparison.
    """
    assert_type(more_than, less_than,
                expected_type=float)
    assert_type(include_more, include_less,
                expected_type=bool)
    for arg in args:
        assert_numeric(arg,
                       allow_none=allow_none)
        assert more_than <= arg if include_more else more_than < arg
        assert arg <= less_than if include_less else arg < less_than

def assert_type_and_range(*args: Any,
                          more_than: float=float("-inf"),
                          less_than: float=float("inf"),
                          include_more: bool=True,
                          include_less: bool=True,
                          allow_none: bool=False) -> None:
    """
    Verifies the input arguments are numeric (float or int) and
    checks that they span the selected range of values.
    Combines both assertions of type and range into a single check.
    """
    for arg in args:
        assert_numeric(arg,
                       allow_none=allow_none)
        if arg is not None:
            assert_range(arg,
                         more_than=more_than,
                         less_than=less_than,
                         include_more=include_more,
                         include_less=include_less)

def assert_numeric(*args: Any,
                   allow_none: bool=False) -> None:
    """
    Asserts if the arguments are numeric (of type `float` or `int`).
    """
    for arg in args:
        assert_type(arg,
                    expected_type=(float, int),
                    allow_none=allow_none)

# CONVERSIONS

def rpm_to_ang_vel(rpm: float) -> float:
    """
    Returns the angular velocity for a given rpm value.
    """
    assert_numeric(rpm)
    return rpm * RPM_TO_ANG_VEL

def ang_vel_to_rpm(ang_vel: float) -> float:
    """
    Returns the rpm value for a given angular velocity.
    """
    assert_numeric(ang_vel)
    return ang_vel * ANG_VEL_TO_RPM

def power_to_torque(power: float, rpm: float) -> float:
    """
    Converts power to torque.
    """
    assert_type_and_range(power, rpm,
                          more_than=0.0,
                          include_more=True)
    return power / rpm_to_ang_vel(rpm=rpm) if rpm > 0.0 else 0.0

def torque_to_power(torque: float, rpm: float) -> float:
    """
    Converts torque to power.
    """
    assert_type_and_range(torque, rpm,
                          more_than=0.0,
                          include_more=True)
    return torque * rpm_to_ang_vel(rpm=rpm) if rpm > 0.0 else 0.0

def kelvin_to_celsius(t_kelvin: float) -> float:
    """
    Converts temperature in Kelvin to Celsius.
    """
    assert_type_and_range(t_kelvin,
                          more_than=0.0)
    return t_kelvin - 273.15

def kelvin_to_fahrenheit(t_kelvin: float) -> float:
    """
    Converts temperature in Kelvin to Fahrenheit.
    """
    assert_type_and_range(t_kelvin,
                          more_than=0.0)
    return kelvin_to_celsius(t_kelvin=t_kelvin) * 1.8 + 32.0

def liters_to_cubic_meters(liters: float) -> float:
    """
    Converts liters to cubic meters.
    """
    assert_type_and_range(liters,
                          more_than=0.0)
    return liters * LTS_TO_CUBIC_METERS

def cubic_meters_to_liters(cubic_meters: float) -> float:
    """
    Converts cubic meters to liters.
    """
    assert_type_and_range(cubic_meters,
                          more_than=0.0)
    return cubic_meters * CUBIC_METERS_TO_LTS
