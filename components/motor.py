"""
This module contains definitions for motors and engines.
"""

from dataclasses import dataclass
from components.fuel_type import Fuel
from components.converter import Converter
from helpers.types import PowerType

@dataclass
class ElectricMotor(Converter):
    """Models a simple, reversible electric motor."""
    def __init__(self,
                 name: str,
                 mass: float,
                 max_power: float,
                 efficiency: float,
                 reverse_efficiency: float):
        super().__init__(name=name,
                         mass=mass,
                         input=PowerType.ELECTRIC,
                         output=PowerType.MECHANICAL,
                         max_power=max_power,
                         efficiency=efficiency,
                         reverse_efficiency=reverse_efficiency)


@dataclass
class InternalCombustionEngine(Converter):
    """Models a simple internal combustion engine."""
    def __init__(self,
                 name: str,
                 mass: float,
                 max_power: float,
                 efficiency: float,
                 fuel: Fuel):
        super().__init__(name=name,
                         mass=mass,
                         input=fuel,
                         output=PowerType.MECHANICAL,
                         max_power=max_power,
                         efficiency=efficiency,
                         reverse_efficiency=None)


@dataclass
class ElectricGenerator(Converter):
    """Models a simple, non reversible electric generator."""
    def __init__(self,
                 name: str,
                 mass: float,
                 max_power: float,
                 efficiency: float):
        super().__init__(name=name,
                         mass=mass,
                         input=PowerType.MECHANICAL,
                         output=PowerType.ELECTRIC,
                         max_power=max_power,
                         efficiency=efficiency,
                         reverse_efficiency=None)
