"""This module contains definitions for different types of batteries."""

from dataclasses import dataclass
from typing import Optional
from components.consumption import RechargeableBatteryConsumption, \
    return_rechargeable_battery_consumption
from components.energy_source import BatteryRechargeable
from simulation.constants import BATTERY_DEFAULT_SOH, BATTERY_EFFICIENCY_DEFAULT, \
    BATTERY_Al_AIR_ENERGY_DENSITY, BATTERY_Pb_ACID_ENERGY_DENSITY, \
    BATTERY_LiCo_ENERGY_DENSITY, BATTERY_LiMn_ENERGY_DENSITY, BATTERY_LiPh_ENERGY_DENSITY, \
    BATTERY_LiPo_ENERGY_DENSITY, BATTERY_NiCd_ENERGY_DENSITY, BATTERY_NiMH_ENERGY_DENSITY, \
    BATTERY_SOLID_STATE_ENERGY_DENSITY

efficiency_default = return_rechargeable_battery_consumption(discharge_efficiency_func=lambda s: BATTERY_EFFICIENCY_DEFAULT,
                                                             recharge_efficiency_func=lambda s: BATTERY_EFFICIENCY_DEFAULT)


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
                 efficiency: Optional[RechargeableBatteryConsumption]=None):
        if efficiency is None:
            efficiency = efficiency_default
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
                 efficiency: Optional[RechargeableBatteryConsumption]=None):
        if efficiency is None:
            efficiency = efficiency_default
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
                 efficiency: Optional[RechargeableBatteryConsumption]=None):
        if efficiency is None:
            efficiency = efficiency_default
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
                 efficiency: Optional[RechargeableBatteryConsumption]=None):
        if efficiency is None:
            efficiency = efficiency_default
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
                 efficiency: Optional[RechargeableBatteryConsumption]=None):
        if efficiency is None:
            efficiency = efficiency_default
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
                 efficiency: Optional[RechargeableBatteryConsumption]=None):
        if efficiency is None:
            efficiency = efficiency_default
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
                 efficiency: Optional[RechargeableBatteryConsumption]=None):
        if efficiency is None:
            efficiency = efficiency_default
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
                 efficiency: Optional[RechargeableBatteryConsumption]=None):
        if efficiency is None:
            efficiency = efficiency_default
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
                 efficiency: Optional[RechargeableBatteryConsumption]=None):
        if efficiency is None:
            efficiency = efficiency_default
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_SOLID_STATE_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency,
                         nominal_voltage=nominal_voltage)
