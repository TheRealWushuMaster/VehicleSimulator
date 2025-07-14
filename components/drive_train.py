"""
This module contains definitions for the drive train, including
all modules that transmit power to and from the ground.
"""

from dataclasses import dataclass
from typing import Optional
from components.converter import Converter
from helpers.functions import assert_type
from helpers.types import PowerType


@dataclass
class Wheel():
    """
    Defines the physical properties of the wheels.
    """
    radius: float
    width: float
    mass: float
    air_pressure: float

    def __post_init__(self):
        assert_type(self.radius, self.width, self.mass, self.air_pressure,
                    expected_type=float)


@dataclass
class Differential(Converter):
    """Models an axle differential."""
    def __init__(self,
                 name: str,
                 mass: float,
                 reverse_efficiency: float,
                 max_power: float=float("inf")):
        super().__init__(name=name,
                         mass=mass,
                         input=PowerType.MECHANICAL,
                         output=PowerType.MECHANICAL,
                         max_power=max_power,
                         reverse_efficiency=reverse_efficiency)


@dataclass
class GearBox(Converter):
    """Models a gear box."""
    def __init__(self,
                 name: str,
                 mass: float,
                 efficiency: float,
                 reverse_efficiency: float,
                 max_power: float=float("inf")):
        super().__init__(name=name,
                         mass=mass,
                         input=PowerType.MECHANICAL,
                         output=PowerType.MECHANICAL,
                         max_power=max_power,
                         efficiency=efficiency,
                         reverse_efficiency=reverse_efficiency)


@dataclass
class PlanetaryGear(Converter):
    """Models a planetary gear train."""
    def __init__(self,
                 name: str,
                 mass: float,
                 efficiency: float,
                 reverse_efficiency: float,
                 max_power: float=float("inf")):
        super().__init__(name=name,
                         mass=mass,
                         input=PowerType.MECHANICAL,
                         output=PowerType.MECHANICAL,
                         max_power=max_power,
                         efficiency=efficiency,
                         reverse_efficiency=reverse_efficiency)


@dataclass
class DriveTrain():
    """
    Models the full drive train for the vehicle.
    """
    wheel: Wheel
    driving_wheels: int
    passive_wheels: int
    differential: Differential
    gearbox: GearBox
    planetarygear: Optional[PlanetaryGear]
