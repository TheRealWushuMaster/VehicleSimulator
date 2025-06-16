"""
This module contains definitions for different types of fuel.
"""

from dataclasses import dataclass
from typing import Optional
from simulation.constants import ENERGY_DENSITY_BIODIESEL, ENERGY_DENSITY_DIESEL, \
    ENERGY_DENSITY_ETHANOL, ENERGY_DENSITY_GASOLINE, ENERGY_DENSITY_HYDROGEN, \
    ENERGY_DENSITY_METHANOL, DENSITY_GASOLINE, DENSITY_DIESEL, DENSITY_ETHANOL, \
    DENSITY_METHANOL, DENSITY_BIODIESEL


@dataclass
class FuelType():
    """
    Represents a type of fuel the vehicle can carry
    for a combustion engine.

    Attributes.
        - energy_density (float): the energy density in J/kg
    """
    energy_density: float    # J/kg
    density: Optional[float] # kg/m^3

    def __post_init__(self):
        self.energy_density = max(self.energy_density, 0.0)
        if self.density:
            self.density = max(self.density, 0.0)


@dataclass
class Hydrogen(FuelType):
    def __init__(self):
        super().__init__(energy_density=ENERGY_DENSITY_HYDROGEN,
                         density=None)


@dataclass
class Gasoline(FuelType):
    def __init__(self):
        super().__init__(energy_density=ENERGY_DENSITY_GASOLINE,
                         density=DENSITY_GASOLINE)


@dataclass
class Diesel(FuelType):
    def __init__(self):
        super().__init__(energy_density=ENERGY_DENSITY_DIESEL,
                         density=DENSITY_DIESEL)


@dataclass
class Ethanol(FuelType):
    def __init__(self):
        super().__init__(energy_density=ENERGY_DENSITY_ETHANOL,
                         density=DENSITY_ETHANOL)


@dataclass
class Methanol(FuelType):
    def __init__(self):
        super().__init__(energy_density=ENERGY_DENSITY_METHANOL,
                         density=DENSITY_METHANOL)


@dataclass
class Biodiesel(FuelType):
    def __init__(self):
        super().__init__(energy_density=ENERGY_DENSITY_BIODIESEL,
                         density=DENSITY_BIODIESEL)
