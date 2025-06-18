"""This module generates sample power vs RPM and efficiency vs power & RPM curves."""

from math import exp, log, sqrt
from typing import Callable
from helpers.functions import assert_type, assert_range
from helpers.types import MotorOperationPoint


class MaxPowerVsRPMCurves():
    """Generates maximum power vs RPM curves."""

    @staticmethod
    def constant(max_power: float,
                 max_rpm: float,
                 min_rpm: float) -> Callable[[float], float]:
        """Generates a constant maximum power from min_rpm to max_rpm."""
        assert_type(max_power, max_rpm, min_rpm,
                    expected_type=float)
        assert_range(max_power, max_rpm, min_rpm,
                     more_than=0.0)
        assert_range(max_rpm,
                     more_than=min_rpm)
        def power_func(rpm: float) -> float:
            return max_power if min_rpm<=rpm<=max_rpm else 0.0
        return power_func

    @staticmethod
    def linear(min_rpm: MotorOperationPoint,
               max_rpm: MotorOperationPoint) -> Callable[[float], float]:
        """Generates a linear maximum power curve from min_rpm to max_rpm."""
        assert_type(min_rpm.rpm, max_rpm.rpm, min_rpm.power, max_rpm.power,
                    expected_type=float)
        assert_range(min_rpm.rpm, min_rpm.power, max_rpm.power,
                     more_than=0.0)
        assert_range(max_rpm.rpm,
                     more_than=min_rpm.rpm)
        def power_func(rpm: float) -> float:
            if not min_rpm.rpm <= rpm <= max_rpm.rpm:
                return 0.0
            return (max_rpm.power - min_rpm.power) * (rpm - min_rpm.rpm) / (max_rpm.rpm - min_rpm.rpm) + min_rpm.power
        return power_func

    @staticmethod
    def ice(min_rpm: MotorOperationPoint,
            max_rpm: MotorOperationPoint,
            peak_rpm: MotorOperationPoint) -> Callable[[float], float]:
        """
        Generates a sample power vs RPM curve for an internal combustion engine.
        It is simulated with a piecewise normal distribution.
        """
        assert_type(min_rpm.rpm, min_rpm.power,
                    max_rpm.rpm, max_rpm.power,
                    peak_rpm.rpm, peak_rpm.power,
                    expected_type=float)
        assert_range(min_rpm.rpm, min_rpm.power,
                     max_rpm.rpm, max_rpm.power,
                     more_than=0.0)
        assert_range(peak_rpm.rpm,
                     more_than=min_rpm.rpm,
                     less_than=max_rpm.rpm)
        assert_range(min_rpm.power, max_rpm.power,
                     less_than=peak_rpm.power)
        alpha1 = (log(peak_rpm.power) - log(min_rpm.power)) / (min_rpm.rpm - peak_rpm.rpm)**2
        alpha2 = (log(peak_rpm.power) - log(max_rpm.power)) / (max_rpm.rpm - peak_rpm.rpm)**2
        def power_func(rpm: float) -> float:
            if rpm < min_rpm.rpm or rpm > max_rpm.rpm:
                return 0.0
            alpha = alpha1 if rpm <= peak_rpm.rpm else alpha2
            return peak_rpm.power * exp(-alpha * (rpm - peak_rpm.rpm)**2)
        return power_func

    @staticmethod
    def electric_motor() -> Callable[[float], float]:
        """
        Generates a sample power vs RPM curve for an electric motor.
        """
        raise NotImplementedError


class PowerEfficiencyCurves():
    """Generates efficiency vs power & RPM curves."""

    @staticmethod
    def constant(efficiency: float,
                 max_rpm: float,
                 min_rpm: float,
                 max_power_vs_rpm: Callable[[float], float]
                 ) -> Callable[[float, float], float]:
        """Generates a constant maximum efficiency from min_rpm to max_rpm."""
        assert_type(efficiency, max_rpm, min_rpm,
                    expected_type=float)
        assert_range(max_rpm, min_rpm,
                     more_than=0.0)
        assert_range(efficiency,
                     more_than=0.0,
                     less_than=1.0)
        def efficiency_func(power: float,
                            rpm: float) -> float:
            if not min_rpm <= rpm <= max_rpm:
                return 0.0
            if not 0.0 <= power <= max_power_vs_rpm(rpm):
                return 0.0
            return efficiency
        return efficiency_func

    @staticmethod
    def linear(max_efficiency: float,
               min_efficiency: float,
               max_rpm: float,
               min_rpm: float,
               max_power_vs_rpm: Callable[[float], float],
               power_max_eff: float,
               rpm_max_eff: float,
               power_falloff_rate: float,
               rpm_falloff_rate: float) -> Callable[[float, float], float]:
        """Generates a linear maximum efficiency from min_rpm to max_rpm."""
        assert_type(max_efficiency, min_efficiency, max_rpm, min_rpm,
                    power_max_eff, rpm_max_eff,
                    power_falloff_rate, rpm_falloff_rate,
                    expected_type=float)
        assert_range(max_rpm, min_rpm,
                     more_than=0.0)
        assert_range(rpm_max_eff,
                     more_than=min_rpm,
                     less_than=max_rpm)
        assert_range(max_efficiency,
                     more_than=0.0,
                     less_than=1.0)
        assert_range(min_efficiency,
                     more_than=0.0,
                     less_than=max_efficiency)
        def efficiency_func(power: float,
                            rpm: float) -> float:
            if not min_rpm <= rpm <= max_rpm:
                return 0.0
            if not 0.0 <= power <= max_power_vs_rpm(rpm):
                return 0.0
            power_range = max_power_vs_rpm(rpm_max_eff)
            rpm_range = max_rpm - min_rpm
            power_distance = abs(power - power_max_eff) / power_range
            rpm_distance = abs(rpm - rpm_max_eff) / rpm_range
            elliptical_distance = sqrt((power_distance*power_falloff_rate)**2 + (rpm_distance*rpm_falloff_rate)**2)
            return max(max_efficiency * max(0.0, 1.0 - elliptical_distance), min_efficiency)
        return efficiency_func
