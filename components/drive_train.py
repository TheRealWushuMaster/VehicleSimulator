"""
This module contains definitions for the drive train, including
all modules that transmit power to and from the ground.
"""

from dataclasses import dataclass

@dataclass
class DriveTrain():
    ...


@dataclass
class Wheel():
    """
    This class defines the physical properties of the wheels.
    """
    radius: float
    width: float
    mass: float
    air_pressure: float


@dataclass
class Differential():
    ...


@dataclass
class GearBox():
    ...


@dataclass
class PlanetaryGearBox():
    ...
