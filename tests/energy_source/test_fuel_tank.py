"""This module contains test routines for the EnergySource class."""

from typing import TypedDict
from components.fuel_tank import LIQUID_FUEL_TANKS, GASEOUS_FUEL_TANKS


class TestLiquidFuelTankParams(TypedDict):
    name: str
    capacity_liters: float
    liters: float
    tank_mass: float


class TestGaseousFuelTankParams(TypedDict):
    name: str
    capacity_mass: float
    fuel_mass: float
    tank_mass: float

capacity: float = 500.0
amount: float = 250.0
tank_mass: float = 50.0

liquid_tank_dict: TestLiquidFuelTankParams = {"name": "Test liquid fuel tank",
                                              "capacity_liters": capacity,
                                              "liters": amount,
                                              "tank_mass": tank_mass}

gaseous_tank_dict: TestGaseousFuelTankParams = {"name": "Test liquid fuel tank",
                                                "capacity_mass": capacity,
                                                "fuel_mass": amount,
                                                "tank_mass": tank_mass}


# ===============================
# ===============================

def test_create_liquid_fuel_tanks() -> None:
    for tank in LIQUID_FUEL_TANKS:
        lft = tank(name="Test liquid fuel tank",
                   capacity_liters=liquid_tank_dict["capacity_liters"],
                   liters=liquid_tank_dict["liters"],
                   tank_mass=liquid_tank_dict["tank_mass"])
        assert isinstance(lft, tank)

def test_create_gaseous_fuel_tanks() -> None:
    for tank in GASEOUS_FUEL_TANKS:
        lft = tank(name="Test liquid fuel tank",
                   capacity_mass=gaseous_tank_dict["capacity_mass"],
                   fuel_mass=gaseous_tank_dict["fuel_mass"],
                   tank_mass=gaseous_tank_dict["tank_mass"])
        assert isinstance(lft, tank)
