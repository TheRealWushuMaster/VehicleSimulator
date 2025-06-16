"""This module contains a base class for all power sources for the vehicle."""

from abc import ABC
from dataclasses import dataclass
from typing import Optional
from components.fuel_type import FuelType, Biodiesel, Ethanol, Diesel, \
    Gasoline, Hydrogen, Methanol
from helpers.functions import clamp
from helpers.power_types import PowerType
from simulation.constants import BATTERY_EFFICIENCY_DEFAULT, HYDROGEN_FUEL_CELL_EFFICIENCY_DEFAULT


@dataclass
class PowerSource(ABC):
    """
    Abstract base class for any power-providing (or receiving)
    unit in the vehicle.
    """
    name: str
    nominal_energy: float   # Joules
    energy: float           # Joules
    mass: float
    power_output: PowerType
    rechargeable: bool
    soh: float
    efficiency: float
    fuel_type: Optional[FuelType]

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
        return self.mass + self.fuel_mass

    def recharge(self, power: float, delta_t: float) -> float:
        """
        Attempts to recharge this source with the given power (W) over delta_t (s).
        Returns actual energy stored.
        """
        if self.rechargeable:
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


class Battery(PowerSource):
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 mass: float,
                 soh: float=1.0,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         mass=mass,
                         power_output=PowerType.ELECTRIC,
                         rechargeable=True,
                         soh=soh,
                         efficiency=efficiency,
                         fuel_type=None)

class GasolineTank(PowerSource):
    def __init__(self,
                 name: str,
                 capacity_litres: float,
                 litres: float,
                 mass: float):
        source = Gasoline()
        super().__init__(name=name,
                         nominal_energy=capacity_litres*source.energy_density,
                         energy=litres*source.energy_density,
                         mass=mass,
                         power_output=PowerType.THERMAL,
                         rechargeable=False,
                         soh=1.0,
                         efficiency=1.0,
                         fuel_type=source)


class DieselTank(PowerSource):
    def __init__(self,
                 name: str,
                 capacity_litres: float,
                 litres: float,
                 mass: float):
        source = Diesel()
        super().__init__(name=name,
                         nominal_energy=capacity_litres*source.energy_density,
                         energy=litres*source.energy_density,
                         mass=mass,
                         power_output=PowerType.THERMAL,
                         rechargeable=False,
                         soh=1.0,
                         efficiency=1.0,
                         fuel_type=source)


class HydrogenTank(PowerSource):
    def __init__(self,
                 name: str,
                 capacity_kg: float,
                 kg: float,
                 mass: float):
        source = Hydrogen()
        super().__init__(name=name,
                         nominal_energy=capacity_kg*source.energy_density,
                         energy=kg*source.energy_density,
                         mass=mass,
                         power_output=PowerType.THERMAL,
                         rechargeable=False,
                         soh=1.0,
                         efficiency=1.0,
                         fuel_type=source)


class EthanolTank(PowerSource):
    def __init__(self,
                 name: str,
                 capacity_litres: float,
                 litres: float,
                 mass: float):
        source = Ethanol()
        super().__init__(name=name,
                         nominal_energy=capacity_litres*source.energy_density,
                         energy=litres*source.energy_density,
                         mass=mass,
                         power_output=PowerType.THERMAL,
                         rechargeable=False,
                         soh=1.0,
                         efficiency=1.0,
                         fuel_type=source)


class MethanolTank(PowerSource):
    def __init__(self,
                 name: str,
                 capacity_litres: float,
                 litres: float,
                 mass: float):
        source = Methanol()
        super().__init__(name=name,
                         nominal_energy=capacity_litres*source.energy_density,
                         energy=litres*source.energy_density,
                         mass=mass,
                         power_output=PowerType.THERMAL,
                         rechargeable=False,
                         soh=1.0,
                         efficiency=1.0,
                         fuel_type=source)


class BiodieselTank(PowerSource):
    def __init__(self,
                 name: str,
                 capacity_litres: float,
                 litres: float,
                 mass: float):
        source = Biodiesel()
        super().__init__(name=name,
                         nominal_energy=capacity_litres*source.energy_density,
                         energy=litres*source.energy_density,
                         mass=mass,
                         power_output=PowerType.THERMAL,
                         rechargeable=False,
                         soh=1.0,
                         efficiency=1.0,
                         fuel_type=source)


class HydrogenFuelCell(PowerSource):
    def __init__(self,
                 name: str,
                 capacity_kg: float,
                 kg: float,
                 mass: float):
        source = Hydrogen()
        super().__init__(name=name,
                         nominal_energy=capacity_kg*source.energy_density,
                         energy=kg*source.energy_density,
                         mass=mass,
                         power_output=PowerType.ELECTRIC,
                         rechargeable=False,
                         soh=1.0,
                         efficiency=HYDROGEN_FUEL_CELL_EFFICIENCY_DEFAULT,
                         fuel_type=source)
