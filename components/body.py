"""This module contains definitions and
properties of the body of the vehicle."""

from dataclasses import dataclass
from helpers.functions import assert_type

@dataclass
class Body():
    """
    The physical properties of the vehicle.
    It assumes dual axles.
    
    Attributes:
        - mass (float): mass, in kg
        - occupants_mass (float): mass of the occupants, in kg
        - height (float): height, in meters
        - length (float): length, in meters
        - front_area (float): front area of the vehicle, in meters²
        - rear_area (float): rear area of the vehicle, in meters²
        - axle_distance (float): distance between axles, in meters
    """
    mass: float
    occupants_mass: float
    height: float
    length: float
    front_area: float
    rear_area: float
    axle_distance: float

    def __post_init__(self):
        assert_type(self.mass, self.occupants_mass, self.height, self.length,
                    self.front_area, self.rear_area, self.axle_distance,
                    expected_type=float)

    @property
    def total_body_mass(self):
        """
        Returns the total mass of the body of the vehicle.
        """
        return self.mass + self.occupants_mass
