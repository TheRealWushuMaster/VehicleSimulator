"""This module generates sample power vs RPM and efficiency vs power & RPM curves."""

from math import exp
from typing import Callable
from helpers.functions import assert_type, assert_range


class MaxPowerVsRPMCurves():
    """Generator for maximum power vs RPM curves."""

    @staticmethod
    def constant(max_power: float,
                 max_rpm: float,
                 min_rpm: float=0.0) -> Callable[[float], float]:
        """Generates a constant maximum power from min_rpm to max_rpm."""
        assert_type(max_power, max_rpm, min_rpm,
                    expected_type=float)
        assert_range(max_power, max_rpm, min_rpm,
                     more_than=0.0)
        def power_func(rpm: float) -> float:
            return max_power if min_rpm<=rpm<=max_rpm else 0.0
        return power_func

    @staticmethod
    def linear(min_rpm: float,
               max_rpm: float,
               power_min_rpm: float,
               power_max_rpm: float) -> Callable[[float], float]:
        """Generates a linear maximum power curve from min_rpm to max_rpm."""
        assert_type(min_rpm, max_rpm, power_min_rpm, power_max_rpm,
                    expected_type=float)
        assert_range(min_rpm, max_rpm, power_min_rpm, power_max_rpm,
                     more_than=0.0)
        def power_func(rpm: float) -> float:
            if not min_rpm <= rpm <= max_rpm:
                return 0.0
            return (power_max_rpm - power_min_rpm) * (rpm - min_rpm) / (max_rpm - min_rpm) + power_min_rpm
        return power_func

    @staticmethod
    def ice(min_rpm: float,
            max_rpm: float,
            peak_rpm: float,
            peak_power: float,
            alpha: float) -> Callable[[float], float]:
        """
        Generates a sample power vs RPM curve for an internal combustion engine.
        It is simulated with a normal distribution.
        """
        assert_type(min_rpm, max_rpm, peak_rpm, peak_power, alpha,
                    expected_type=float)
        assert_range(min_rpm, max_rpm, peak_power, alpha,
                     more_than=0.0)
        assert_range(peak_rpm,
                     more_than=min_rpm,
                     less_than=max_rpm)
        def power_func(rpm: float) -> float:
            return peak_power*exp(-alpha*(rpm - peak_rpm)**2)
        return power_func

    @staticmethod
    def electric_motor() -> Callable[[float], float]:
        """
        Generates a sample power vs RPM curve for an electric motor.
        """
        raise NotImplementedError


class PowerEfficiencyCurves():
    """Generator for maximum power vs RPM curves."""
    raise NotImplementedError
