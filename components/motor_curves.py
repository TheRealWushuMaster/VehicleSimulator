"""This module generates sample power vs RPM and efficiency vs power & RPM curves."""

from math import exp, sqrt
from typing import Callable
from components.state import MechanicalState
from helpers.functions import assert_type, assert_range, assert_numeric, assert_type_and_range
from helpers.types import MotorOperationPoint, MotorEfficiencyPoint


class MechanicalMaxPowerVsRPMCurves():
    """
    Generates maximum power vs RPM curves.
    Only applies to mechanical components.
    """
    @staticmethod
    def constant(max_power: float,
                 max_rpm: float,
                 min_rpm: float) -> Callable[[MechanicalState], float]:
        """
        Generates a constant maximum power from min_rpm to max_rpm.
        """
        assert_type(max_power, max_rpm, min_rpm,
                    expected_type=float)
        assert_range(max_power, max_rpm, min_rpm,
                     more_than=0.0)
        assert_range(max_rpm,
                     more_than=min_rpm)
        def power_func(state: MechanicalState) -> float:
            return max_power if min_rpm<=state.rpm<=max_rpm else 0.0
        return power_func

    @staticmethod
    def linear(min_rpm: MotorOperationPoint,
               max_rpm: MotorOperationPoint) -> Callable[[MechanicalState], float]:
        """Generates a linear maximum power curve from min_rpm to max_rpm."""
        assert_numeric(min_rpm.rpm, max_rpm.rpm, min_rpm.power, max_rpm.power)
        assert_range(min_rpm.rpm, min_rpm.power, max_rpm.power,
                     more_than=0.0)
        assert_range(max_rpm.rpm,
                     more_than=min_rpm.rpm)
        def power_func(state: MechanicalState) -> float:
            if not min_rpm.rpm <= state.rpm <= max_rpm.rpm:
                return 0.0
            return (max_rpm.power - min_rpm.power) * (state.rpm - min_rpm.rpm) / (max_rpm.rpm - min_rpm.rpm) + min_rpm.power
        return power_func

    @staticmethod
    def ice(min_rpm: MotorOperationPoint,
            max_rpm: MotorOperationPoint,
            peak_rpm: MotorOperationPoint) -> Callable[[MechanicalState], float]:
        """
        Generates a sample maximum power vs RPM curve for an internal
        combustion engine.
        It is simulated with two Gaussian curves.
        """
        assert_range(peak_rpm.rpm,
                     more_than=min_rpm.rpm,
                     less_than=max_rpm.rpm)
        assert_range(min_rpm.power, max_rpm.power,
                     less_than=peak_rpm.power)
        alpha_1 = 1 / 2 / (peak_rpm.rpm - min_rpm.rpm)**2
        k2 = (min_rpm.power - peak_rpm.power) / (exp(-0.5) - 1)
        k1 = peak_rpm.power - k2
        alpha_2 = 1 / 2 / (peak_rpm.rpm - max_rpm.rpm)**2
        k4 = (max_rpm.power - peak_rpm.power) / (exp(-0.5) - 1)
        k3 = peak_rpm.power - k4
        def power_func(state: MechanicalState) -> float:
            if not min_rpm.rpm <= state.rpm <= max_rpm.rpm:
                return 0.0
            alpha, a, b = (alpha_1, k1, k2) if state.rpm <= peak_rpm.rpm else (alpha_2, k3, k4)
            return a + b * exp(-alpha * (state.rpm - peak_rpm.rpm)**2)
        return power_func

    @staticmethod
    def em(base_rpm: float,
           max_rpm: float,
           max_power: float) -> Callable[[MechanicalState], float]:
        """
        Generates a sample power vs RPM curve for an electric motor.
        Maximum power increases linearly up to base_rpm, then remains constant.
        """
        assert_type_and_range(base_rpm, max_power,
                              more_than=0.0)
        assert_type_and_range (max_rpm,
                               more_than=base_rpm)
        def power_func(state: MechanicalState) -> float:
            if not 0.0 <= state.rpm <= max_rpm:
                return 0.0
            if state.rpm <= base_rpm:
                return max_power * state.rpm / base_rpm
            return max_power
        return power_func


class MechanicalPowerEfficiencyCurves():
    """
    Generates efficiency vs power & RPM curves.
    Only applies to mechanical components.
    """
    @staticmethod
    def constant(efficiency: float,
                 max_rpm: float,
                 min_rpm: float,
                 max_power_vs_rpm: Callable[[float], float]
                 ) -> Callable[[MechanicalState], float]:
        """
        Generates a constant maximum efficiency from min_rpm to max_rpm.
        """
        assert_numeric(efficiency, max_rpm, min_rpm)
        assert_type(max_power_vs_rpm,
                    expected_type=Callable) # type: ignore[arg-type]
        assert_range(min_rpm,
                     more_than=0.0)
        assert_range(max_rpm,
                     more_than=min_rpm)
        assert_range(efficiency,
                     more_than=0.0,
                     less_than=1.0)
        def efficiency_func(state: MechanicalState) -> float:
            if not min_rpm <= state.rpm <= max_rpm:
                return 0.0
            if not 0.0 <= state.power <= max_power_vs_rpm(state.rpm):
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
               rpm_falloff_rate: float) -> Callable[[MechanicalState], float]:
        """Generates a linear maximum efficiency from min_rpm to max_rpm."""
        assert_type(max_efficiency, min_efficiency, max_rpm, min_rpm,
                    power_max_eff, rpm_max_eff,
                    power_falloff_rate, rpm_falloff_rate,
                    expected_type=float)
        assert_type(max_power_vs_rpm,
                    expected_type=Callable) # type: ignore[arg-type]
        assert_range(min_rpm,
                     more_than=0.0)
        assert_range(max_rpm,
                     more_than=min_rpm)
        assert_range(rpm_max_eff,
                     more_than=min_rpm,
                     less_than=max_rpm)
        assert_range(max_efficiency,
                     more_than=0.0,
                     less_than=1.0)
        assert_range(min_efficiency,
                     more_than=0.0,
                     less_than=max_efficiency)
        def efficiency_func(state: MechanicalState) -> float:
            if not min_rpm <= state.rpm <= max_rpm:
                return 0.0
            if not 0.0 <= state.power <= max_power_vs_rpm(state.rpm):
                return 0.0
            power_range = max_power_vs_rpm(rpm_max_eff)
            rpm_range = max_rpm - min_rpm
            power_distance = abs(state.power - power_max_eff) / power_range
            rpm_distance = abs(state.rpm - rpm_max_eff) / rpm_range
            elliptical_distance = sqrt((power_distance*power_falloff_rate)**2 + (rpm_distance*rpm_falloff_rate)**2)
            return max(max_efficiency * max(0.0, 1.0 - elliptical_distance), min_efficiency)
        return efficiency_func

    @staticmethod
    def gaussian(max_eff: MotorEfficiencyPoint,
                 min_eff: float,
                 falloff_rpm: float,
                 falloff_power: float,
                 max_power_vs_rpm: Callable[[MechanicalState], float],
                 min_rpm: float,
                 max_rpm: float) -> Callable[[MechanicalState], float]:
        """
        Generates a sample efficiency vs power & rpm for internal
        combustion engines and electric motors.
        It is simulated using a bivariate Gaussian curve.
        The values of `falloff_rpm` and `falloff_power` should be much
        smaller for electric motors than for ICEs.
        """
        assert_type(falloff_rpm, falloff_power, min_rpm, max_rpm,
                    expected_type=float)
        assert_type(max_power_vs_rpm,
                    expected_type=Callable) # type: ignore[arg-type]
        assert_range(falloff_rpm, falloff_power,
                     more_than=0.0)
        assert_range(min_eff,
                     more_than=0.0,
                     less_than=max_eff.efficiency)
        def efficiency_func(state: MechanicalState) -> float:
            if not min_rpm <= state.rpm <= max_rpm or \
               not 0.0 <= state.power <= max_power_vs_rpm(state):
                return 0.0
            return max(max_eff.efficiency * exp(-falloff_rpm*(state.rpm-max_eff.rpm)**2 - falloff_power*(state.power-max_eff.power)**2), min_eff)
        return efficiency_func
