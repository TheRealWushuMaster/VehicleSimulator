"""This module contains test routines for the Battery class."""

from typing import Callable, TypedDict
from components.battery import AlAirBattery, LiCoBattery, LiPoBattery, LiMnBattery, \
    LiPhBattery, NiCdBattery, NiMHBattery, PbAcidBattery, SolidStateBattery
from components.battery_curves import BatteryEfficiencyCurves, BatteryVoltageVSCurrent
from components.energy_source import BatteryRechargeable, BatteryNonRechargeable


class TestBatteryParams(TypedDict):
    """
    Default test parameters for batteries.
    """
    name: str
    nominal_energy: float
    max_current: float
    energy: float
    battery_mass: float
    soh: float
    efficiency: Callable[[float], float]
    nominal_voltage: float
    voltage_vs_current: Callable[[float], float]

voltage: float = 400.0
current: float = 200.0
efficiency: float = 0.96
battery_dict: TestBatteryParams = {"name": "Test battery",
                                   "nominal_energy": 1_000.0,
                                   "max_current": 200.0,
                                   "energy": 500.0,
                                   "battery_mass": 50.0,
                                   "soh": 1.0,
                                   "efficiency": BatteryEfficiencyCurves.constant(efficiency=efficiency,
                                                                                  max_current=current),
                                   "nominal_voltage": voltage,
                                   "voltage_vs_current": BatteryVoltageVSCurrent.constant_voltage(voltage=voltage,
                                                                                                  max_current=current)}

def create_rechargeable_battery() -> BatteryRechargeable:
    battery = BatteryRechargeable(name=battery_dict["name"],
                                  nominal_energy=battery_dict["nominal_energy"],
                                  max_current=battery_dict["max_current"],
                                  energy=battery_dict["energy"],
                                  battery_mass=battery_dict["battery_mass"],
                                  soh=battery_dict["soh"],
                                  efficiency=battery_dict["efficiency"],
                                  nominal_voltage=battery_dict["nominal_voltage"],
                                  voltage_vs_current=battery_dict["voltage_vs_current"])
    return battery

def create_non_rechargeable_battery() -> BatteryNonRechargeable:
    battery = BatteryNonRechargeable(name=battery_dict["name"],
                                     nominal_energy=battery_dict["nominal_energy"],
                                     max_current=battery_dict["max_current"],
                                     energy=battery_dict["energy"],
                                     battery_mass=battery_dict["battery_mass"],
                                     soh=battery_dict["soh"],
                                     efficiency=battery_dict["efficiency"],
                                     nominal_voltage=battery_dict["nominal_voltage"],
                                     voltage_vs_current=battery_dict["voltage_vs_current"])
    return battery

def create_battery_type(battery_type) -> BatteryRechargeable|BatteryNonRechargeable:
    assert issubclass(battery_type, BatteryRechargeable|BatteryNonRechargeable)
    assert battery_type in (AlAirBattery, LiCoBattery, LiPoBattery, LiMnBattery, LiPhBattery,
                            NiCdBattery, NiMHBattery, PbAcidBattery, SolidStateBattery)
    battery = battery_type(name=battery_dict["name"],
                           nominal_energy=battery_dict["nominal_energy"],
                           max_current=battery_dict["max_current"],
                           energy=battery_dict["energy"],
                           soh=battery_dict["soh"],
                           efficiency=battery_dict["efficiency"],
                           nominal_voltage=battery_dict["nominal_voltage"],
                           voltage_vs_current=battery_dict["voltage_vs_current"])
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
