"""This module contains a base class for all power sources for the vehicle."""

from dataclasses import dataclass
from typing import Optional
from components.fuel_type import Fuel, LiquidFuel, GaseousFuel
from helpers.functions import clamp
from helpers.types import PowerType
from simulation.constants import BATTERY_EFFICIENCY_DEFAULT, BATTERY_DEFAULT_SOH


@dataclass
class EnergySource():
    """
    Abstract base class for any power-providing
    (or receiving) unit in the vehicle.
    """
    name: str
    nominal_energy: float   # Joules
    energy: float           # Joules
    system_mass: float
    power_input: Optional[PowerType]
    power_output: Optional[PowerType]
    soh: float
    efficiency: float
    fuel_type: Optional[Fuel]

    def __post_init__(self):
        self.nominal_energy = max(self.nominal_energy, 0.0)
        self.mass = max(self.mass, 0.0)
        self.energy = clamp(val=self.energy,
                            min_val=0.0,
                            max_val=self.max_energy)
        self.soh = clamp(val=self.soh,
                         min_val=0.0,
                         max_val=1.0)
        self.efficiency = clamp(val=self.efficiency,
                                min_val=0.0,
                                max_val=1.0)

    @property
    def soc(self) -> float:
        """
        Returns the source's current state of charge (SOC).
        """
        return self.energy / self.nominal_energy / self.soh

    @property
    def max_energy(self) -> float:
        """
        Returns the maximum amount of energy
        that can be held by the source.
        """
        return self.nominal_energy * self.soh

    @property
    def is_empty(self) -> bool:
        """
        Check if the source has no usable energy left.
        """
        return self.energy<=0

    @property
    def is_full(self) -> bool:
        """
        Check if the source cannot receive any more energy.
        """
        return self.energy==self.max_energy

    @property
    def max_fuel_mass(self) -> float:
        """
        If applicable, returns the maximum mass of fuel [kg]
        based on current energy and fuel's energy density.
        """
        if self.fuel_type:
            return self.max_energy / self.fuel_type.energy_density
        return 0.0

    @property
    def fuel_mass(self) -> float:
        """
        If applicable, returns the estimated remaining mass of fuel [kg]
        based on current energy and fuel's energy density.
        """
        if self.fuel_type:
            return self.energy / self.fuel_type.energy_density
        return 0.0

    @property
    def total_mass(self) -> float:
        """
        Returns the total mass of the power source.
        """
        return self.system_mass + self.fuel_mass

    def recharge(self, power: float, delta_t: float) -> float:
        """
        Attempts to recharge this source with the given power (W) over delta_t (s).
        Returns actual energy stored.
        """
        if self.power_input:
            input_energy = abs(power) * delta_t * self.efficiency
            self.energy = min(self.max_energy, self.energy + input_energy)
            return input_energy
        return 0.0

    def discharge(self, power: float, delta_t: float) -> float:
        """
        Discharges the source at a defined power over a delta_t duration.
        Returns actual energy spent.
        """
        output_energy = abs(power) * delta_t / self.efficiency
        self.energy = max(0.0, self.energy - output_energy)
        return output_energy


@dataclass
class Battery(EnergySource):
    """
    Models a generic battery type.
    """
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 battery_mass: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         system_mass=battery_mass,
                         power_input=PowerType.ELECTRIC,
                         power_output=PowerType.ELECTRIC,
                         soh=soh,
                         efficiency=efficiency,
                         fuel_type=None)


@dataclass
class LiquidFuelTank(EnergySource):
    """
    Models a fuel tank for a liquid fuel.
    """
    def __init__(self,
                 name: str,
                 fuel: LiquidFuel,
                 capacity_litres: float,
                 litres: float,
                 tank_mass: float):
        super().__init__(name=name,
                         nominal_energy=capacity_litres*fuel.energy_density,
                         energy=litres*fuel.energy_density,
                         system_mass=tank_mass,
                         power_input=None,
                         power_output=None,
                         soh=1.0,
                         efficiency=1.0,
                         fuel_type=fuel)


@dataclass
class GaseousFuelTank(EnergySource):
    """
    Models a fuel tank for a gaseous fuel.
    """
    def __init__(self,
                 name: str,
                 fuel: GaseousFuel,
                 capacity_kg: float,
                 kg: float,
                 tank_mass: float):
        super().__init__(name=name,
                         nominal_energy=capacity_kg*fuel.energy_density,
                         energy=kg*fuel.energy_density,
                         system_mass=tank_mass,
                         power_input=None,
                         power_output=None,
                         soh=1.0,
                         efficiency=1.0,
                         fuel_type=fuel)
