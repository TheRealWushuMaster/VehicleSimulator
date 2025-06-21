"""This module generates sample power and efficiency curves for Fuel Cells."""

from collections.abc import Callable
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
