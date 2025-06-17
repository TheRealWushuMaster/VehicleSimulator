"""
This module contains definitions for motors and engines.
"""

from dataclasses import dataclass
from components.fuel_type import Fuel
from components.power_converter import PowerConverter
from helpers.types import PowerType

@dataclass
class ElectricMotor(PowerConverter):
    """Models a simple electric motor."""
    def __init__(self,
                 name: str,
                 power_rating: float,
                 efficiency: float,
                 reverse_efficiency: float):
        super().__init__(name=name,
                         input_power=PowerType.ELECTRIC,
                         output_power=PowerType.MECHANICAL,
                         power_rating=power_rating,
                         efficiency=efficiency,
                         fuel=None,
                         reverse_efficiency=reverse_efficiency)


@dataclass
class InternalCombustionEngine(PowerConverter):
    """Models a simple internal combustion engine."""
    def __init__(self,
                 name: str,
                 power_rating: float,
                 efficiency: float,
                 fuel: Fuel):
        super().__init__(name=name,
                         input_power=PowerType.CHEMICAL,
                         output_power=PowerType.MECHANICAL,
                         power_rating=power_rating,
                         efficiency=efficiency,
                         fuel=fuel,
                         reverse_efficiency=None)


@dataclass
class ElectricGenerator(PowerConverter):
    """Models a simple, non reversible electric generator."""
    def __init__(self,
                 name: str,
                 power_rating: float,
                 efficiency: float):
        super().__init__(name=name,
                         input_power=PowerType.MECHANICAL,
                         output_power=PowerType.ELECTRIC,
                         power_rating=power_rating,
                         efficiency=efficiency,
                         fuel=None,
                         reverse_efficiency=None)
