"""This module contains test routines for the EnergySource class."""

from typing import TypedDict
from components.energy_source import LiquidFuelTank, GaseousFuelTank
from components.fuel_type import LiquidFuel, GaseousFuel, Biodiesel, Gasoline, Diesel, \
    Ethanol, HydrogenLiquid, Methanol, HydrogenGas, Methane


class TestLiquidFuelTankParams(TypedDict):
    name: str
    capacity_litres: float
    litres: float
    tank_mass: float


class TestGaseousFuelTankParams(TypedDict):
    name: str
    capacity_kg: float
    kg: float
    tank_mass: float


liquid_tank_dict: TestLiquidFuelTankParams = {"name": "Test liquid fuel tank",
                                              "capacity_litres": 500.0,
                                              "litres": 250.0,
                                              "tank_mass": 50.0}

gaseous_tank_dict: TestGaseousFuelTankParams = {"name": "Test liquid fuel tank",
                                                "capacity_kg": 500.0,
                                                "kg": 250.0,
                                                "tank_mass": 50.0}


# ===============================
# ===============================

def create_liquid_fuel_tank(fuel: LiquidFuel) -> LiquidFuelTank:
    assert isinstance(fuel, LiquidFuel)
    fuel_tank = LiquidFuelTank(name=liquid_tank_dict["name"],
                               fuel=fuel,
                               capacity_litres=liquid_tank_dict["capacity_litres"],
                               litres=liquid_tank_dict["litres"],
                               tank_mass=liquid_tank_dict["tank_mass"])
    assert isinstance(fuel_tank, LiquidFuelTank)
    return fuel_tank

def create_gaseous_fuel_tank(fuel: GaseousFuel) -> GaseousFuelTank:
    assert isinstance(fuel, GaseousFuel)
    fuel_tank = GaseousFuelTank(name=gaseous_tank_dict["name"],
                                fuel=fuel,
                                capacity_kg=gaseous_tank_dict["capacity_kg"],
                                kg=gaseous_tank_dict["kg"],
                                tank_mass=gaseous_tank_dict["tank_mass"])
    assert isinstance(fuel_tank, GaseousFuelTank)
    return fuel_tank

# ===============================

def test_create_gasoline_tank() -> LiquidFuelTank:
    fuel_tank = create_liquid_fuel_tank(fuel=Gasoline())
    return fuel_tank

def test_create_diesel_tank() -> LiquidFuelTank:
    fuel_tank = create_liquid_fuel_tank(fuel=Diesel())
    return fuel_tank

def test_create_biodiesel_tank() -> LiquidFuelTank:
    fuel_tank = create_liquid_fuel_tank(fuel=Biodiesel())
    return fuel_tank

def test_create_ethanol_tank() -> LiquidFuelTank:
    fuel_tank = create_liquid_fuel_tank(fuel=Ethanol())
    return fuel_tank

def test_create_methanol_tank() -> LiquidFuelTank:
    fuel_tank = create_liquid_fuel_tank(fuel=Methanol())
    return fuel_tank

def test_create_liquid_hydrogen_tank() -> LiquidFuelTank:
    fuel_tank = create_liquid_fuel_tank(fuel=HydrogenLiquid())
    return fuel_tank

def test_create_gaseous_hydrogen_tank() -> GaseousFuelTank:
    fuel_tank = create_gaseous_fuel_tank(fuel=HydrogenGas())
    return fuel_tank

def test_create_methane_tank() -> GaseousFuelTank:
    fuel_tank = create_gaseous_fuel_tank(fuel=Methane())
    return fuel_tank
