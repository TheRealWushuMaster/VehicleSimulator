"""This module contains definitions and
properties of the body of the vehicle."""

from dataclasses import dataclass

@dataclass
class Body():
    """
    The physical properties of the vehicle.
    It assumes dual axles.
    
    Attributes:
        - mass (float): mass, in kg
        - height (float): height, in meters
        - length (float): length, in meters
        - front_area (float): front area of the vehicle, in meters^2
        - rear_area (float): rear area of the vehicle, in meters^2
        - axle_distance (float): distance between axles, in meters
    """
    mass: float
    height: float
    length: float
    front_area: float
    rear_area: float
    axle_distance: float


@dataclass
class Wheel():
    """
    This class defines the physical properties of the wheels.
    """
    radius: float
    width: float
    mass: float
    air_pressure: float
