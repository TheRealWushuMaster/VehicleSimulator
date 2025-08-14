"""This module contains definitions for different types of batteries."""

from dataclasses import dataclass
from typing import Callable, Optional
from components.battery_curves import BatteryEfficiencyCurves
from components.energy_source import BatteryRechargeable
from helpers.functions import assert_type_and_range
from simulation.constants import BATTERY_DEFAULT_SOH, BATTERY_EFFICIENCY_DEFAULT, \
    BATTERY_Al_AIR_ENERGY_DENSITY, BATTERY_Pb_ACID_ENERGY_DENSITY, \
    BATTERY_LiCo_ENERGY_DENSITY, BATTERY_LiMn_ENERGY_DENSITY, BATTERY_LiPh_ENERGY_DENSITY, \
    BATTERY_LiPo_ENERGY_DENSITY, BATTERY_NiCd_ENERGY_DENSITY, BATTERY_NiMH_ENERGY_DENSITY, \
    BATTERY_SOLID_STATE_ENERGY_DENSITY


def default_callables(efficiency: Optional[Callable[[float], float]],
                      max_power: float) -> Callable[[float], float]:
    """
    Returns default callables for efficiency.
    """
    assert_type_and_range(max_power,
                          more_than=0.0)
    if efficiency is None:
        efficiency = BatteryEfficiencyCurves.constant(efficiency=BATTERY_EFFICIENCY_DEFAULT,
                                                      max_power=max_power)
    return efficiency


@dataclass
class AlAirBattery(BatteryRechargeable):
    """Models an Aluminium Air battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 nominal_voltage: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: Optional[Callable[[float], float]]=None):
        efficiency = default_callables(efficiency=efficiency,
                                       max_power=max_power)
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_Al_AIR_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency,
                         nominal_voltage=nominal_voltage)


@dataclass
class PbAcidBattery(BatteryRechargeable):
    """Models a lead-acid battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 nominal_voltage: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: Optional[Callable[[float], float]]=None):
        efficiency = default_callables(efficiency=efficiency,
                                       max_power=max_power)
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_Pb_ACID_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency,
                         nominal_voltage=nominal_voltage)


@dataclass
class LiCoBattery(BatteryRechargeable):
    """Models a Lithium-ion Cobalt battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 nominal_voltage: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: Optional[Callable[[float], float]]=None):
        efficiency = default_callables(efficiency=efficiency,
                                       max_power=max_power)
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_LiCo_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency,
                         nominal_voltage=nominal_voltage)


@dataclass
class LiMnBattery(BatteryRechargeable):
    """Models a Lithium-ion Manganese battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 nominal_voltage: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: Optional[Callable[[float], float]]=None):
        efficiency = default_callables(efficiency=efficiency,
                                       max_power=max_power)
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_LiMn_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency,
                         nominal_voltage=nominal_voltage)


@dataclass
class LiPhBattery(BatteryRechargeable):
    """Models a Lithium-ion Phosphate battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 nominal_voltage: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: Optional[Callable[[float], float]]=None):
        efficiency = default_callables(efficiency=efficiency,
                                       max_power=max_power)
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_LiPh_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency,
                         nominal_voltage=nominal_voltage)


@dataclass
class LiPoBattery(BatteryRechargeable):
    """Models a Lithium-ion Polymer battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 nominal_voltage: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: Optional[Callable[[float], float]]=None):
        efficiency = default_callables(efficiency=efficiency,
                                       max_power=max_power)
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_LiPo_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency,
                         nominal_voltage=nominal_voltage)


@dataclass
class NiCdBattery(BatteryRechargeable):
    """Models a Nickel Cadmium battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 nominal_voltage: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: Optional[Callable[[float], float]]=None):
        efficiency = default_callables(efficiency=efficiency,
                                       max_power=max_power)
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_NiCd_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency,
                         nominal_voltage=nominal_voltage)


@dataclass
class NiMHBattery(BatteryRechargeable):
    """Models a Nickel Metal Hydride battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 nominal_voltage: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: Optional[Callable[[float], float]]=None):
        efficiency = default_callables(efficiency=efficiency,
                                       max_power=max_power)
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_NiMH_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency,
                         nominal_voltage=nominal_voltage)


@dataclass
class SolidStateBattery(BatteryRechargeable):
    """Models a Solid State battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 nominal_voltage: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: Optional[Callable[[float], float]]=None):
        efficiency = default_callables(efficiency=efficiency,
                                       max_power=max_power)
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_SOLID_STATE_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency,
                         nominal_voltage=nominal_voltage)
