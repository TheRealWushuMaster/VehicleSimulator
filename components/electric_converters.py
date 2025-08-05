"""This module contains class definitions for electric converters."""

from dataclasses import dataclass
from typing import Callable
from components.converter import PureElectricConverter
from components.state import State
from helpers.types import ElectricSignalType


@dataclass
class Inverter(PureElectricConverter):
    """
    Models an electric inverter, which converts DC to AC.
    """
    def __init__(self, name: str,
                 mass: float,
                 max_power: float,
                 eff_func: Callable[[State], float],
                 reverse_efficiency: float,
                 power_func: Callable[[State], float],
                 nominal_voltage_in: float,
                 nominal_voltage_out: float):
        super().__init__(name=name,
                         mass=mass,
                         max_power=max_power,
                         eff_func=eff_func,
                         reverse_efficiency=reverse_efficiency,
                         power_func=power_func,
                         reversible=False,
                         in_type=ElectricSignalType.DC,
                         out_type=ElectricSignalType.AC,
                         nominal_voltage_in=nominal_voltage_in,
                         nominal_voltage_out=nominal_voltage_out)


@dataclass
class Rectifier(PureElectricConverter):
    """
    Models an electric rectifier, which converts AC to DC.
    """
    def __init__(self, name: str,
                 mass: float,
                 max_power: float,
                 eff_func: Callable[[State], float],
                 reverse_efficiency: float,
                 power_func: Callable[[State], float],
                 nominal_voltage_in: float,
                 nominal_voltage_out: float):
        super().__init__(name=name,
                         mass=mass,
                         max_power=max_power,
                         eff_func=eff_func,
                         reverse_efficiency=reverse_efficiency,
                         power_func=power_func,
                         reversible=False,
                         in_type=ElectricSignalType.AC,
                         out_type=ElectricSignalType.DC,
                         nominal_voltage_in=nominal_voltage_in,
                         nominal_voltage_out=nominal_voltage_out)
