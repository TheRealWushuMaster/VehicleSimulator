"""
This module contains definitions for different types of fuel.
"""

from dataclasses import dataclass
from helpers.functions import assert_type, assert_range, assert_type_and_range, \
    liters_to_cubic_meters
from helpers.types import PowerType, StateOfMatter
from simulation.constants import ENERGY_DENSITY_BIODIESEL, ENERGY_DENSITY_DIESEL, \
    ENERGY_DENSITY_ETHANOL, ENERGY_DENSITY_GASOLINE, ENERGY_DENSITY_HYDROGEN, \
    ENERGY_DENSITY_METHANOL, ENERGY_DENSITY_METHANE, DENSITY_GASOLINE, \
    DENSITY_DIESEL, DENSITY_ETHANOL, DENSITY_METHANOL, DENSITY_BIODIESEL, \
    DENSITY_HYDROGEN_LIQUID


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
    state: StateOfMatter

    def __post_init__(self):
        assert_type(self.name,
                    expected_type=str)
        assert_type_and_range(self.energy_density,
                              more_than=0.0,
                              include_more=False)
        assert_type(self.state,
                    expected_type=StateOfMatter)
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

    def energy_per_kg(self, mass: float) -> float:
        """
        Returns the amount of energy contained
        in a certain mass of fuel.
        """
        assert_type_and_range(mass,
                              more_than=0.0)
        return mass * self.energy_density


@dataclass
class GaseousFuel(Fuel):
    """Creates a gaseous fuel."""
    def __init__(self,
                 name: str,
                 energy_density: float):
        super().__init__(name=name,
                         energy_density=energy_density,
                         state=StateOfMatter.GASEOUS)


@dataclass
class LiquidFuel(Fuel):
    """Creates a liquid fuel."""
    mass_density: float

    def __init__(self,
                 name: str,
                 energy_density: float,
                 mass_density: float):
        assert_range(mass_density,
                     more_than=0.0)
        super().__init__(name=name,
                         energy_density=energy_density,
                         state=StateOfMatter.LIQUID)
        self.mass_density = mass_density

    def energy_per_liter(self, liters: float) -> float:
        """
        Returns the amount of energy contained
        in a certain volume (liters) of fuel.
        """
        assert_type_and_range(liters,
                              more_than=0.0)
        return liters_to_cubic_meters(liters) * self.mass_density * self.energy_density

    def energy_per_cubic_meter(self, cubic_meters: float) -> float:
        """
        Returns the amount of energy contained
        in a certain volume (liters) of fuel.
        """
        assert_type_and_range(cubic_meters,
                              more_than=0.0)
        return cubic_meters * self.mass_density * self.energy_density


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
                         mass_density=DENSITY_HYDROGEN_LIQUID)


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
                         mass_density=DENSITY_GASOLINE)


@dataclass
class Diesel(LiquidFuel):
    """Creates liquid Diesel fuel."""
    def __init__(self):
        super().__init__(name="Diesel",
                         energy_density=ENERGY_DENSITY_DIESEL,
                         mass_density=DENSITY_DIESEL)


@dataclass
class Ethanol(LiquidFuel):
    """Creates liquid Ethanol fuel."""
    def __init__(self):
        super().__init__(name="Ethanol",
                         energy_density=ENERGY_DENSITY_ETHANOL,
                         mass_density=DENSITY_ETHANOL)


@dataclass
class Methanol(LiquidFuel):
    """Creates liquid Methanol fuel."""
    def __init__(self):
        super().__init__(name="Methanol",
                         energy_density=ENERGY_DENSITY_METHANOL,
                         mass_density=DENSITY_METHANOL)


@dataclass
class Biodiesel(LiquidFuel):
    """Creates liquid Biodiesel fuel."""
    def __init__(self):
        super().__init__(name="Biodiesel",
                         energy_density=ENERGY_DENSITY_BIODIESEL,
                         mass_density=DENSITY_BIODIESEL)

LIQUID_FUELS: list[LiquidFuel] = [Biodiesel(), Diesel(), Ethanol(),
                                  Gasoline(), HydrogenLiquid(), Methanol()]
GASEOUS_FUELS: list[GaseousFuel] = [HydrogenGas(), Methane()]
