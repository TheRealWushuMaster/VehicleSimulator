"""This module contains property curves for battery objects."""

from typing import Callable
from helpers.functions import assert_type_and_range


class BatteryEfficiencyCurves():
    """
    Returns curves relating energy efficiency.
    """
    pass


class BatteryVoltageVSCurrent():
    """
    Returns curves relating voltage and current.
    """
    @staticmethod
    def constant_voltage(voltage: float,
                         max_power: float) -> Callable[[float], float]:
        """
        Returns a constant voltage for all values of current.
        """
        assert_type_and_range(voltage, max_power,
                              more_than=0.0)
        max_current = max_power / voltage
        def voltage_vs_current(current: float) -> float:
            assert_type_and_range(current,
                                  more_than=0.0)
            if current <= max_current:
                return voltage
            return 0.0
        return voltage_vs_current
        