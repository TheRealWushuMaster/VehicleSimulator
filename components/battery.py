"""This module contains definitions for different types of batteries."""

from dataclasses import dataclass
from components.energy_source import Battery
from simulation.constants import BATTERY_DEFAULT_SOH, BATTERY_EFFICIENCY_DEFAULT, \
    BATTERY_Al_AIR_ENERGY_DENSITY, BATTERY_Pb_ACID_ENERGY_DENSITY, \
    BATTERY_LiCo_ENERGY_DENSITY, BATTERY_LiMn_ENERGY_DENSITY, BATTERY_LiPh_ENERGY_DENSITY, \
    BATTERY_LiPo_ENERGY_DENSITY, BATTERY_NiCd_ENERGY_DENSITY, BATTERY_NiMH_ENERGY_DENSITY, \
    BATTERY_SOLID_STATE_ENERGY_DENSITY


@dataclass
class AlAirBattery(Battery):
    """Models a lead-acid battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_Al_AIR_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency)


@dataclass
class PbAcidBattery(Battery):
    """Models a lead-acid battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_Pb_ACID_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency)


@dataclass
class LiCoBattery(Battery):
    """Models a lead-acid battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_LiCo_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency)


@dataclass
class LiMnBattery(Battery):
    """Models a lead-acid battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_LiMn_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency)


@dataclass
class LiPhBattery(Battery):
    """Models a lead-acid battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_LiPh_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency)


@dataclass
class LiPoBattery(Battery):
    """Models a lead-acid battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_LiPo_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency)


@dataclass
class NiCdBattery(Battery):
    """Models a lead-acid battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_NiCd_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency)


@dataclass
class NiMHBattery(Battery):
    """Models a lead-acid battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_NiMH_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency)


@dataclass
class SolidStateBattery(Battery):
    """Models a lead-acid battery."""
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         battery_mass=nominal_energy/BATTERY_SOLID_STATE_ENERGY_DENSITY,
                         soh=soh,
                         efficiency=efficiency)
