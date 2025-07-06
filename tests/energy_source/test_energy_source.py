"""This module contains test routines for the EnergySource class."""

from typing import TypedDict
from components.battery import AlAirBattery, LiCoBattery, LiPoBattery, LiMnBattery, \
    LiPhBattery, NiCdBattery, NiMHBattery, PbAcidBattery, SolidStateBattery
from components.energy_source import Battery, BatteryNonRechargeable, \
    LiquidFuelTank, GaseousFuelTank
from components.fuel_type import LiquidFuel, GaseousFuel, Biodiesel, Gasoline, Diesel, \
    Ethanol, HydrogenLiquid, Methanol, HydrogenGas, Methane


class TestBatteryParams(TypedDict):
    name: str
    nominal_energy: float
    energy: float
    battery_mass: float
    soh: float
    efficiency: float

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


battery_dict: TestBatteryParams = {"name": "Test battery",
                                   "nominal_energy": 1_000.0,
                                   "energy": 500.0,
                                   "battery_mass": 50.0,
                                   "soh": 1.0,
                                   "efficiency": 0.96}

liquid_tank_dict: TestLiquidFuelTankParams = {"name": "Test liquid fuel tank",
                                              "capacity_litres": 500.0,
                                              "litres": 250.0,
                                              "tank_mass": 50.0}

gaseous_tank_dict: TestGaseousFuelTankParams = {"name": "Test liquid fuel tank",
                                                "capacity_kg": 500.0,
                                                "kg": 250.0,
                                                "tank_mass": 50.0}

def create_battery(battery_type: type[Battery|BatteryNonRechargeable]=Battery
                   ) -> Battery|BatteryNonRechargeable:
    if battery_type in (Battery, BatteryNonRechargeable):
        battery = battery_type(name=battery_dict["name"],
                               nominal_energy=battery_dict["nominal_energy"],
                               energy=battery_dict["energy"],
                               battery_mass=battery_dict["battery_mass"],
                               soh=battery_dict["soh"],
                               efficiency=battery_dict["efficiency"])
        assert isinstance(battery, (Battery, BatteryNonRechargeable))
    elif issubclass(battery_type, Battery):
        battery = battery_type(battery_dict["name"],
                               battery_dict["nominal_energy"],
                               battery_dict["energy"],
                               battery_dict["soh"],
                               battery_dict["efficiency"])
    else:
        raise TypeError("The argument `battery_type` must be of type `Battery` or `BatteryNonRechargeable`.")
    return battery

#===============================

def test_create_generic_battery() -> Battery:
    battery = create_battery(battery_type=Battery)
    assert isinstance(battery, Battery)
    return battery

def test_create_generic_non_rechargeable_battery() -> BatteryNonRechargeable:
    battery = create_battery(battery_type=BatteryNonRechargeable)
    assert isinstance(battery, BatteryNonRechargeable)
    return battery

def test_create_AlAirBattery() -> AlAirBattery:
    battery = create_battery(battery_type=AlAirBattery)
    assert isinstance(battery, AlAirBattery)
    return battery

def test_create_LiCoBattery() -> LiCoBattery:
    battery = create_battery(battery_type=LiCoBattery)
    assert isinstance(battery, LiCoBattery)
    return battery

def test_create_LiPoBattery() -> LiPoBattery:
    battery = create_battery(battery_type=LiPoBattery)
    assert isinstance(battery, LiPoBattery)
    return battery

def test_create_LiMnBattery() -> LiMnBattery:
    battery = create_battery(battery_type=LiMnBattery)
    assert isinstance(battery, LiMnBattery)
    return battery

def test_create_LiPhBattery() -> LiPhBattery:
    battery = create_battery(battery_type=LiPhBattery)
    assert isinstance(battery, LiPhBattery)
    return battery

def test_create_NiCdBattery() -> NiCdBattery:
    battery = create_battery(battery_type=NiCdBattery)
    assert isinstance(battery, NiCdBattery)
    return battery

def test_create_NiMHBattery() -> NiMHBattery:
    battery = create_battery(battery_type=NiMHBattery)
    assert isinstance(battery, NiMHBattery)
    return battery

def test_create_PbAcidBattery() -> PbAcidBattery:
    battery = create_battery(battery_type=PbAcidBattery)
    assert isinstance(battery, PbAcidBattery)
    return battery

def test_create_SolidStateBattery() -> SolidStateBattery:
    battery = create_battery(battery_type=SolidStateBattery)
    assert isinstance(battery, SolidStateBattery)
    return battery

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
