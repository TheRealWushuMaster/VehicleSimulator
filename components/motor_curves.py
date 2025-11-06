"""This module generates sample power vs RPM and efficiency vs power & RPM curves."""

from math import exp, sqrt
from typing import Callable
from components.component_snapshot import ElectricMotorSnapshot, \
    LiquidCombustionEngineSnapshot, GaseousCombustionEngineSnapshot
from helpers.functions import assert_type, assert_range, assert_type_and_range, \
    assert_numeric, assert_callable, power_to_torque
from helpers.functions import clamp
from helpers.types import MotorOperationPoint, MotorEfficiencyPoint

ICESnapshot = LiquidCombustionEngineSnapshot | GaseousCombustionEngineSnapshot
MotorSnapshot = ElectricMotorSnapshot | ICESnapshot

class MechanicalMaxPowerVsRPMCurves():
    """
    Generates maximum power vs RPM curves.
    Only applies to mechanical components.
    """
    @staticmethod
    def constant(max_power: float,
                 max_rpm: float,
                 min_rpm: float) -> Callable[[MotorSnapshot], float]:
        """
        Generates a constant maximum power from min_rpm to max_rpm.
        """
        assert_type(max_power, max_rpm, min_rpm,
                    expected_type=float)
        assert_range(max_power, max_rpm, min_rpm,
                     more_than=0.0)
        assert_range(max_rpm,
                     more_than=min_rpm)
        def power_func(snap: MotorSnapshot) -> float:
            return max_power if min_rpm<=snap.state.output_port.rpm<=max_rpm else 0.0
        return power_func

    @staticmethod
    def linear(min_rpm: MotorOperationPoint,
               max_rpm: MotorOperationPoint) -> Callable[[MotorSnapshot], float]:
        """Generates a linear maximum power curve from min_rpm to max_rpm."""
        assert_numeric(min_rpm.rpm, max_rpm.rpm, min_rpm.power, max_rpm.power)
        assert_range(min_rpm.rpm, min_rpm.power, max_rpm.power,
                     more_than=0.0)
        assert_range(max_rpm.rpm,
                     more_than=min_rpm.rpm)
        def power_func(snap: MotorSnapshot) -> float:
            if not min_rpm.rpm <= snap.state.output_port.rpm <= max_rpm.rpm:
                return 0.0
            return (max_rpm.power - min_rpm.power) * (snap.state.output_port.rpm - min_rpm.rpm) / (max_rpm.rpm - min_rpm.rpm) + min_rpm.power
        return power_func

    @staticmethod
    def ice(min_rpm: MotorOperationPoint,
            max_rpm: MotorOperationPoint,
            peak_rpm: MotorOperationPoint
            ) -> Callable[[ICESnapshot], float]:
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
        def power_func(snap: ICESnapshot) -> float:
            if not min_rpm.rpm <= snap.state.output_port.rpm <= max_rpm.rpm:
                return 0.0
            alpha, a, b = (alpha_1, k1, k2) if snap.state.output_port.rpm <= peak_rpm.rpm else (alpha_2, k3, k4)
            return a + b * exp(-alpha * (snap.state.output_port.rpm - peak_rpm.rpm)**2)
        return power_func

    @staticmethod
    def em(base_rpm: float,
           max_rpm: float,
           max_power: float) -> Callable[[ElectricMotorSnapshot], float]:
        """
        Generates a sample power vs RPM curve for an electric motor.
        Maximum power increases linearly up to base_rpm, then remains constant.
        """
        assert_type_and_range(base_rpm, max_power,
                              more_than=0.0)
        assert_type_and_range (max_rpm,
                               more_than=base_rpm)
        def power_func(snap: ElectricMotorSnapshot) -> float:
            if not 0.0 <= snap.state.output_port.rpm <= max_rpm:
                return 0.0
            if snap.state.output_port.rpm <= base_rpm:
                return max_power * snap.state.output_port.rpm / base_rpm
            return max_power
        return power_func


class MechanicalMaxTorqueVsRPMCurves():
    """
    Generates maximum torque vs RPM curves.
    Only applies to mechanical components.
    """
    @staticmethod
    def ice(min_rpm: MotorOperationPoint,
            max_rpm: MotorOperationPoint,
            peak_rpm: MotorOperationPoint
            ) -> Callable[[ICESnapshot], float]:
        """
        Generates a sample maximum torque vs RPM curve for an internal
        combustion engine.
        It is simulated with two Gaussian curves for the maximum power
        and afterwards converting from power to torque.
        """
        power_func = MechanicalMaxPowerVsRPMCurves.ice(min_rpm=min_rpm,
                                                       max_rpm=max_rpm,
                                                       peak_rpm=peak_rpm)
        def torque_func(snap: ICESnapshot) -> float:
            return power_to_torque(power=power_func(snap),
                                   rpm=snap.state.output_port.rpm)
        return torque_func

    @staticmethod
    def em(base_rpm: float,
           max_rpm: float,
           max_torque: float
           ) -> Callable[[ElectricMotorSnapshot], float]:
        """
        Generates a sample torque vs RPM curve for an electric motor.
        Maximum power increases linearly up to base_rpm, then remains constant.
        """
        assert_type_and_range(base_rpm, max_torque,
                              more_than=0.0)
        assert_type_and_range(max_rpm,
                              more_than=base_rpm)
        def torque_func(snap: ElectricMotorSnapshot) -> float:
            if not 0.0 <= snap.state.output_port.rpm <= max_rpm:
                return 0.0
            if snap.state.output_port.rpm <= base_rpm:
                return max_torque
            return max_torque * base_rpm / snap.state.output_port.rpm
        return torque_func


class MechanicalPowerEfficiencyCurves():
    """
    Generates efficiency vs power & RPM curves.
    Only applies to mechanical components.
    """
    @staticmethod
    def constant(efficiency: float,
                 max_rpm: float,
                 min_rpm: float,
                 max_torque_vs_rpm: Callable[[MotorSnapshot], float]
                 ) -> Callable[[MotorSnapshot], float]:
        """
        Generates a constant maximum efficiency from min_rpm to max_rpm.
        """
        assert_numeric(efficiency, max_rpm, min_rpm)
        assert_callable(max_torque_vs_rpm)
        assert_range(min_rpm,
                     more_than=0.0)
        assert_range(max_rpm,
                     more_than=min_rpm)
        assert_range(efficiency,
                     more_than=0.0,
                     less_than=1.0)
        def efficiency_func(snap: MotorSnapshot,
                            limit: bool=True) -> float:
            if limit:
                snap.io.output_port.applied_torque = clamp(val=snap.io.output_port.applied_torque,
                                                           min_val=0.0,
                                                           max_val=max_torque_vs_rpm(snap))
                snap.state.output_port.rpm = clamp(val=snap.state.output_port.rpm,
                                                   min_val=min_rpm,
                                                   max_val=max_rpm)
            if not min_rpm <= snap.state.output_port.rpm <= max_rpm:
                return 0.0
            if 0.0 <= snap.io.output_port.applied_torque <= max_torque_vs_rpm(snap):
                return efficiency
            return 0.0
        return efficiency_func

    @staticmethod
    def linear(max_efficiency: float,
               min_efficiency: float,
               max_rpm: float,
               min_rpm: float,
               max_power_vs_rpm: Callable[[MotorSnapshot], float],
               power_max_eff: float,
               rpm_max_eff: float,
               power_falloff_rate: float,
               rpm_falloff_rate: float) -> Callable[[MotorSnapshot], float]:
        """Generates a linear maximum efficiency from min_rpm to max_rpm."""
        assert_type(max_efficiency, min_efficiency, max_rpm, min_rpm,
                    power_max_eff, rpm_max_eff,
                    power_falloff_rate, rpm_falloff_rate,
                    expected_type=float)
        assert_callable(max_power_vs_rpm)
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
        def efficiency_func(snap: MotorSnapshot) -> float:
            if not min_rpm <= snap.state.output_port.rpm <= max_rpm:
                return 0.0
            if not 0.0 <= snap.power_out <= max_power_vs_rpm(snap):
                return 0.0
            power_range = max_power_vs_rpm(snap)
            rpm_range = max_rpm - min_rpm
            power_distance = abs(snap.power_out - power_max_eff) / power_range
            rpm_distance = abs(snap.state.output_port.rpm - rpm_max_eff) / rpm_range
            elliptical_distance = sqrt((power_distance*power_falloff_rate)**2 + (rpm_distance*rpm_falloff_rate)**2)
            return max(max_efficiency * max(0.0, 1.0 - elliptical_distance), min_efficiency)
        return efficiency_func

    @staticmethod
    def gaussian(max_eff: MotorEfficiencyPoint,
                 min_eff: float,
                 falloff_rpm: float,
                 falloff_power: float,
                 max_power_vs_rpm: Callable[[MotorSnapshot], float],
                 min_rpm: float,
                 max_rpm: float) -> Callable[[MotorSnapshot], float]:
        """
        Generates a sample efficiency vs power & rpm for internal
        combustion engines and electric motors.
        It is simulated using a bivariate Gaussian curve.
        The values of `falloff_rpm` and `falloff_power` should be much
        smaller for electric motors than for ICEs.
        """
        assert_type(falloff_rpm, falloff_power, min_rpm, max_rpm,
                    expected_type=float)
        assert_callable(max_power_vs_rpm)
        assert_range(falloff_rpm, falloff_power,
                     more_than=0.0)
        assert_range(min_eff,
                     more_than=0.0,
                     less_than=max_eff.efficiency)
        def efficiency_func(snap: MotorSnapshot) -> float:
            if not min_rpm <= snap.state.output_port.rpm <= max_rpm or \
               not 0.0 <= snap.power_out <= max_power_vs_rpm(snap):
                return 0.0
            return max(max_eff.efficiency * exp(-falloff_rpm*(snap.state.output_port.rpm-max_eff.rpm)**2 - falloff_power*(snap.power_out-max_eff.power)**2), min_eff)
        return efficiency_func
