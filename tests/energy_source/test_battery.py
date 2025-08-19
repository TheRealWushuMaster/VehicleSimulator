"""This module contains test routines for the Battery class."""

from typing import TypedDict
from components.battery import AlAirBattery, LiCoBattery, LiPoBattery, LiMnBattery, \
    LiPhBattery, NiCdBattery, NiMHBattery, PbAcidBattery, SolidStateBattery
from components.consumption import RechargeableBatteryConsumption, \
    NonRechargeableBatteryConsumption, \
    return_rechargeable_battery_consumption, return_non_rechargeable_battery_consumption
from components.energy_source import BatteryRechargeable, BatteryNonRechargeable


class TestBatteryParams(TypedDict):
    """
    Default test parameters for batteries.
    """
    name: str
    nominal_energy: float
    max_power: float
    energy: float
    battery_mass: float
    soh: float
    rech_eff: RechargeableBatteryConsumption
    non_rech_eff: NonRechargeableBatteryConsumption
    nominal_voltage: float

voltage: float = 400.0
power: float = 200.0
efficiency_rech: float = 0.96
efficiency_disch: float = 0.94
battery_dict: TestBatteryParams = {"name": "Test battery",
                                   "nominal_energy": 1_000.0,
                                   "max_power": power,
                                   "energy": 500.0,
                                   "battery_mass": 50.0,
                                   "soh": 1.0,
                                   "rech_eff": return_rechargeable_battery_consumption(discharge_efficiency_func=lambda s: efficiency_disch,
                                                                                       recharge_efficiency_func=lambda s: efficiency_rech),
                                   "non_rech_eff": return_non_rechargeable_battery_consumption(discharge_efficiency_func=lambda s: efficiency_disch),
                                   "nominal_voltage": voltage}

def create_rechargeable_battery() -> BatteryRechargeable:
    battery = BatteryRechargeable(name=battery_dict["name"],
                                  nominal_energy=battery_dict["nominal_energy"],
                                  max_power=battery_dict["max_power"],
                                  energy=battery_dict["energy"],
                                  battery_mass=battery_dict["battery_mass"],
                                  soh=battery_dict["soh"],
                                  efficiency=battery_dict["rech_eff"],
                                  nominal_voltage=battery_dict["nominal_voltage"])
    return battery

def create_non_rechargeable_battery() -> BatteryNonRechargeable:
    battery = BatteryNonRechargeable(name=battery_dict["name"],
                                     nominal_energy=battery_dict["nominal_energy"],
                                     max_power=battery_dict["max_power"],
                                     energy=battery_dict["energy"],
                                     battery_mass=battery_dict["battery_mass"],
                                     soh=battery_dict["soh"],
                                     efficiency=battery_dict["non_rech_eff"],
                                     nominal_voltage=battery_dict["nominal_voltage"])
    return battery

def create_battery_type(battery_type) -> BatteryRechargeable|BatteryNonRechargeable:
    assert issubclass(battery_type, BatteryRechargeable|BatteryNonRechargeable)
    assert battery_type in (AlAirBattery, LiCoBattery, LiPoBattery, LiMnBattery, LiPhBattery,
                            NiCdBattery, NiMHBattery, PbAcidBattery, SolidStateBattery)
    battery = battery_type(name=battery_dict["name"],
                           nominal_energy=battery_dict["nominal_energy"],
                           max_power=battery_dict["max_power"],
                           energy=battery_dict["energy"],
                           soh=battery_dict["soh"],
                           efficiency=battery_dict["rech_eff"],
                           nominal_voltage=battery_dict["nominal_voltage"])
    return battery

# ===============================

def test_create_generic_rechargeable_battery() -> BatteryRechargeable:
    battery = create_rechargeable_battery()
    assert isinstance(battery, BatteryRechargeable)
    return battery

def test_create_generic_non_rechargeable_battery() -> BatteryNonRechargeable:
    battery = create_non_rechargeable_battery()
    assert isinstance(battery, BatteryNonRechargeable)
    return battery

def test_create_AlAirBattery() -> AlAirBattery:
    battery = create_battery_type(battery_type=AlAirBattery)
    assert isinstance(battery, AlAirBattery)
    return battery

def test_create_LiCoBattery() -> LiCoBattery:
    battery = create_battery_type(battery_type=LiCoBattery)
    assert isinstance(battery, LiCoBattery)
    return battery

def test_create_LiPoBattery() -> LiPoBattery:
    battery = create_battery_type(battery_type=LiPoBattery)
    assert isinstance(battery, LiPoBattery)
    return battery

def test_create_LiMnBattery() -> LiMnBattery:
    battery = create_battery_type(battery_type=LiMnBattery)
    assert isinstance(battery, LiMnBattery)
    return battery

def test_create_LiPhBattery() -> LiPhBattery:
    battery = create_battery_type(battery_type=LiPhBattery)
    assert isinstance(battery, LiPhBattery)
    return battery

def test_create_NiCdBattery() -> NiCdBattery:
    battery = create_battery_type(battery_type=NiCdBattery)
    assert isinstance(battery, NiCdBattery)
    return battery

def test_create_NiMHBattery() -> NiMHBattery:
    battery = create_battery_type(battery_type=NiMHBattery)
    assert isinstance(battery, NiMHBattery)
    return battery

def test_create_PbAcidBattery() -> PbAcidBattery:
    battery = create_battery_type(battery_type=PbAcidBattery)
    assert isinstance(battery, PbAcidBattery)
    return battery

def test_create_SolidStateBattery() -> SolidStateBattery:
    battery = create_battery_type(battery_type=SolidStateBattery)
    assert isinstance(battery, SolidStateBattery)
    return battery
