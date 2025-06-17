"""
This module contains definitions for different types of fuel.
"""

from dataclasses import dataclass
from typing import Optional
from helpers.functions import assert_type
from helpers.types import PowerType, StateOfMatter
from simulation.constants import ENERGY_DENSITY_BIODIESEL, ENERGY_DENSITY_DIESEL, \
    ENERGY_DENSITY_ETHANOL, ENERGY_DENSITY_GASOLINE, ENERGY_DENSITY_HYDROGEN, \
    ENERGY_DENSITY_METHANOL, ENERGY_DENSITY_METHANE, DENSITY_GASOLINE, \
    DENSITY_DIESEL, DENSITY_ETHANOL, DENSITY_METHANOL, DENSITY_BIODIESEL, \
    DENSITY_HYDROGEN_LIQUID, EPSILON


@dataclass
class Fuel():
    """
    Represents a type of fuel the vehicle can carry
    for a combustion engine.

    Attributes.
        - name (str): a readable name for the fuel
        - energy_density (float): the energy density in J/kg
        - density (float): the density of the fuel in kg/m³
        - state (StateOfMatter): whether the fuel is liquid, gaseous, or solid
    """
    name: str
    energy_density: float
    density: Optional[float]
    state: StateOfMatter

    def __post_init__(self):
        assert_type(self.name,
                    expected_type=str)
        assert_type(self.energy_density,
                    expected_type=float)
        assert_type(self.density,
                    expected_type=float,
                    allow_none=True)
        assert_type(self.state,
                    expected_type=StateOfMatter)
        self.energy_density = max(self.energy_density, EPSILON)
        if self.density:
            self.density = max(self.density, EPSILON)
        self.power_type = PowerType.CHEMICAL

    @property
    def is_solid(self) -> bool:
        """Returns whether the fuel is solid."""
        return self.state==StateOfMatter.SOLID

    @property
    def is_liquid(self) -> bool:
        """Returns whether the fuel is liquid."""
        return self.state==StateOfMatter.LIQUID

    @property
    def is_gaseous(self) -> bool:
        """Returns whether the fuel is gaseous."""
        return self.state==StateOfMatter.GASEOUS


@dataclass
class GaseousFuel(Fuel):
    """Assists creating a gaseous fuel."""
    def __init__(self,
                 name: str,
                 energy_density: float):
        super().__init__(name=name,
                         energy_density=energy_density,
                         density=None,
                         state=StateOfMatter.GASEOUS)


@dataclass
class LiquidFuel(Fuel):
    """Assists creating a liquid fuel."""
    def __init__(self,
                 name: str,
                 energy_density: float,
                 density: float):
        assert isinstance(density, float)
        super().__init__(name=name,
                         energy_density=energy_density,
                         density=density,
                         state=StateOfMatter.LIQUID)


@dataclass
class HydrogenGas(GaseousFuel):
    """Creates gaseous Hydrogen fuel."""
    def __init__(self):
        super().__init__(name="Gaseous Hydrogen",
                         energy_density=ENERGY_DENSITY_HYDROGEN)


@dataclass
class HydrogenLiquid(LiquidFuel):
    """Creates liquid Hydrogen fuel."""
    def __init__(self):
        super().__init__(name="Liquid Hydrogen",
                         energy_density=ENERGY_DENSITY_HYDROGEN,
                         density=DENSITY_HYDROGEN_LIQUID)


@dataclass
class Methane(GaseousFuel):
    """Creates gaseous Methane fuel."""
    def __init__(self):
        super().__init__(name="Methane",
                         energy_density=ENERGY_DENSITY_METHANE)


@dataclass
class Gasoline(LiquidFuel):
    """Creates liquid Gasoline fuel."""
    def __init__(self):
        super().__init__(name="Gasoline",
                         energy_density=ENERGY_DENSITY_GASOLINE,
                         density=DENSITY_GASOLINE)


@dataclass
class Diesel(LiquidFuel):
    """Creates liquid Diesel fuel."""
    def __init__(self):
        super().__init__(name="Diesel",
                         energy_density=ENERGY_DENSITY_DIESEL,
                         density=DENSITY_DIESEL)


@dataclass
class Ethanol(LiquidFuel):
    """Creates liquid Ethanol fuel."""
    def __init__(self):
        super().__init__(name="Ethanol",
                         energy_density=ENERGY_DENSITY_ETHANOL,
                         density=DENSITY_ETHANOL)


@dataclass
class Methanol(LiquidFuel):
    """Creates liquid Methanol fuel."""
    def __init__(self):
        super().__init__(name="Methanol",
                         energy_density=ENERGY_DENSITY_METHANOL,
                         density=DENSITY_METHANOL)


@dataclass
class Biodiesel(LiquidFuel):
    """Creates liquid Biodiesel fuel."""
    def __init__(self):
        super().__init__(name="Biodiesel",
                         energy_density=ENERGY_DENSITY_BIODIESEL,
                         density=DENSITY_BIODIESEL)
