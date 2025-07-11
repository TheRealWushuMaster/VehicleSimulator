"""This module contains test routines for the Battery class."""

from typing import TypedDict
from components.battery import AlAirBattery, LiCoBattery, LiPoBattery, LiMnBattery, \
    LiPhBattery, NiCdBattery, NiMHBattery, PbAcidBattery, SolidStateBattery
from components.energy_source import Battery, BatteryNonRechargeable


class TestBatteryParams(TypedDict):
    name: str
    nominal_energy: float
    energy: float
    battery_mass: float
    soh: float
    efficiency: float


battery_dict: TestBatteryParams = {"name": "Test battery",
                                   "nominal_energy": 1_000.0,
                                   "energy": 500.0,
                                   "battery_mass": 50.0,
                                   "soh": 1.0,
                                   "efficiency": 0.96}

def create_battery(battery_type: type[Battery | BatteryNonRechargeable] = Battery
                   ) -> Battery | BatteryNonRechargeable:
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
        raise TypeError(
            "The argument `battery_type` must be of type `Battery` or `BatteryNonRechargeable`.")
    return battery

# ===============================


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
