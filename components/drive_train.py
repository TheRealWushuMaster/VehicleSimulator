"""
This module contains definitions for the drive train, including
all modules that transmit power to and from the ground.
"""

from dataclasses import dataclass
from typing import Optional
from components.converter import MechanicalConverter
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

    @property
    def inertia(self) -> float:
        """
        Returns the moment of inertia.
        It assumes a "thick ring" type of wheel, with most of its
        mass concentrated near the rim.
        """
        return 0.75 * self.mass * self.radius**2


@dataclass
class Differential(MechanicalConverter):
    """Models an axle differential."""
    def __init__(self,
                 name: str,
                 mass: float,
                 reverse_efficiency: float,
                 inertia: float,
                 max_power: float=float("inf")):
        super().__init__(name=name,
                         mass=mass,
                         input=PowerType.MECHANICAL,
                         output=PowerType.MECHANICAL,
                         control=0.0,
                         max_power=max_power,
                         power_func=None,
                         efficiency_func=None,
                         dynamic_response=None,
                         reverse_efficiency=reverse_efficiency,
                         inertia=inertia)


@dataclass
class GearBox(MechanicalConverter):
    """Models a gear box."""
    def __init__(self,
                 name: str,
                 mass: float,
                 efficiency: float,
                 reverse_efficiency: float,
                 inertia: float,
                 max_power: float=float("inf")):
        super().__init__(name=name,
                         mass=mass,
                         input=PowerType.MECHANICAL,
                         output=PowerType.MECHANICAL,
                         max_power=max_power,
                         efficiency=efficiency,
                         reverse_efficiency=reverse_efficiency,
                         inertia=inertia)


@dataclass
class PlanetaryGear(MechanicalConverter):
    """Models a planetary gear train."""
    def __init__(self,
                 name: str,
                 mass: float,
                 efficiency: float,
                 reverse_efficiency: float,
                 inertia: float,
                 max_power: float=float("inf")):
        super().__init__(name=name,
                         mass=mass,
                         input=PowerType.MECHANICAL,
                         output=PowerType.MECHANICAL,
                         max_power=max_power,
                         efficiency=efficiency,
                         reverse_efficiency=reverse_efficiency,
                         inertia=inertia)


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
