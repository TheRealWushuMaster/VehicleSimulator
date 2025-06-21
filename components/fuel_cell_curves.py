"""This module generates sample power and efficiency curves for Fuel Cells."""

from math import exp
from collections.abc import Callable
import numpy as np
import matplotlib.pyplot as plt
from components.state import ElectricalState
from helpers.functions import assert_type_and_range, assert_range


class FuelCellEfficiencyCurves():
    """
    Generates efficiency curves for Fuel Cells.
    """
    @staticmethod
    def constant(min_power: float,
                 max_power: float,
                 efficiency: float) -> Callable[[ElectricalState], float]:
        """
        Returns a constant efficiency function.
        """
        assert_type_and_range(min_power, efficiency,
                              more_than=0.0)
        assert_type_and_range(max_power,
                              more_than=min_power)
        assert_range(efficiency,
                     less_than=1.0)
        def efficiency_func(state: ElectricalState) -> float:
            if not min_power <= state.power <= max_power:
                return 0.0
            return efficiency
        return efficiency_func

    @staticmethod
    def gaussian(min_power: float,
                 min_power_eff: float,
                 power_peak_eff: float,
                 peak_eff: float,
                 max_power: float,
                 max_power_eff: float) -> Callable[[ElectricalState], float]:
        """
        Returns a piecewise gaussian curve efficiency function.
        """
        assert_type_and_range(min_power, min_power_eff,
                              power_peak_eff, peak_eff,
                              max_power, max_power_eff,
                              more_than=0.0)
        assert_range(power_peak_eff,
                     more_than=min_power,
                     less_than=max_power)
        assert_range(max_power_eff,
                     more_than=min_power_eff,
                     less_than=peak_eff)
        k2 = (min_power_eff - peak_eff) / (exp(-0.5)-1)
        k1 = peak_eff - k2
        alpha1 = 0.5 / (power_peak_eff - min_power)**2
        k4 = (max_power_eff - peak_eff) / (exp(-0.5)-1)
        k3 = peak_eff - k4
        alpha2 = 0.5 / (power_peak_eff - max_power)**2
        def efficiency_func(state: ElectricalState) -> float:
            if not min_power <= state.power <= max_power:
                return 0.0
            if state.power <= power_peak_eff:
                return k1 + k2 * exp(-alpha1*(state.power - power_peak_eff)**2)
            return k3 + k4 * exp(-alpha2*(state.power - power_peak_eff)**2)
        return efficiency_func
