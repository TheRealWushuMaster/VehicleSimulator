"""This module contains property curves for battery objects."""

from typing import Callable
from helpers.functions import assert_type_and_range


class BatteryEfficiencyCurves():
    """
    Returns curves relating energy efficiency.
    """
    @staticmethod
    def constant(efficiency: float,
                 max_current: float) -> Callable[[float], float]:
        """
        Returns a constant efficiency for all current values.
        """
        assert_type_and_range(efficiency,
                              more_than=0.0,
                              less_than=1.0,
                              include_more=False)
        assert_type_and_range(max_current,
                              more_than=0.0,
                              include_more=False)
        def constant_efficiency(current: float) -> float:
            if 0.0 <= current <= max_current:
                return efficiency
            return 0.0
        return constant_efficiency


class BatteryVoltageVSCurrent():
    """
    Returns curves relating voltage and current.
    """
    @staticmethod
    def constant_voltage(voltage: float,
                         max_current: float) -> Callable[[float], float]:
        """
        Returns a constant voltage for all values of current.
        """
        assert_type_and_range(voltage, max_current,
                              more_than=0.0,
                              include_more=False)
        def voltage_vs_current(current: float) -> float:
            if 0.0 <= current <= max_current:
                return voltage
            return 0.0
        return voltage_vs_current
