"""This module contains a base class for all power sources for the vehicle."""

from dataclasses import dataclass, field
from typing import Optional
from components.fuel_type import Fuel, LiquidFuel, GaseousFuel
from components.port import PortInput, PortOutput, PortBidirectional
from components.state import EnergySourceState
from helpers.functions import clamp, assert_type
from helpers.types import PowerType
from simulation.constants import BATTERY_EFFICIENCY_DEFAULT, \
    BATTERY_DEFAULT_SOH, LTS_TO_CUBIC_METERS, EPSILON


@dataclass
class EnergySource():
    """
    Base class for any module that stores energy.
    
    Attributes:
        - name (str): the name of the energy source
        - nominal_energy (float): the maximum energy to be stored (Joules)
        - energy (float): the starting energy stored (Joules)
        - system_mass (float): the mass of the system (kg) without including
                the mass of any fuel used
        - energy_medium (PowerType or Fuel): what the source stores
        - soh (float): models the degradation of the source [0.0-1.0]
        - efficiency (float): efficiency when delivering or receiving [0.0-1.0]
        - rechargeable (bool): allows the source to be recharged
    """
    name: str
    nominal_energy: float
    input: Optional[PortInput|PortBidirectional]
    output: PortOutput|PortBidirectional
    state: EnergySourceState
    energy: float
    system_mass: float
    soh: float
    efficiency: float
    energy_medium: PowerType|Fuel = field(init=False)
    rechargeable: bool = field(init=False)

    def __post_init__(self):
        assert_type(self.name,
                    expected_type=str)
        assert_type(self.nominal_energy, self.energy,
                    self.system_mass, self.soh, self.efficiency,
                    expected_type=float)
        assert_type(self.energy_medium,
                    expected_type=(PowerType, Fuel))
        assert_type(self.rechargeable,
                    expected_type=bool)
        if self.input is not None:
            assert self.input.exchange==self.output.exchange
        self.nominal_energy = max(self.nominal_energy, EPSILON)
        self.system_mass = max(self.system_mass, EPSILON)
        self.energy = clamp(val=self.energy,
                            min_val=0.0,
                            max_val=self.max_energy)
        self.soh = clamp(val=self.soh,
                         min_val=EPSILON,
                         max_val=1.0)
        self.efficiency = clamp(val=self.efficiency,
                                min_val=EPSILON,
                                max_val=1.0)
        self.energy_medium = self.output.exchange
        self.rechargeable = self.input is not None

    @property
    def soc(self) -> float:
        """
        Returns the source's current state of charge (SOC).
        """
        return self.state.energy / self.nominal_energy / self.soh

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
        return self.state.energy <= 0

    @property
    def is_full(self) -> bool:
        """
        Check if the source cannot receive any more energy.
        """
        return self.state.energy==self.max_energy

    @property
    def max_fuel_mass(self) -> float:
        """
        If applicable, returns the maximum mass of fuel [kg]
        based on current energy and fuel's energy density.
        """
        if isinstance(self.energy_medium, Fuel):
            return self.max_energy / self.energy_medium.energy_density
        return 0.0

    @property
    def fuel_mass(self) -> float:
        """
        If applicable, returns the estimated remaining mass of fuel [kg]
        based on current energy and fuel's energy density.
        """
        if isinstance(self.energy_medium, Fuel):
            return self.state.energy / self.energy_medium.energy_density
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
        if self.rechargeable:
            input_energy = abs(power) * delta_t * self.efficiency
            self.state.energy = min(self.max_energy, self.state.energy + input_energy)
            return input_energy
        return 0.0

    def discharge(self, power: float, delta_t: float) -> float:
        """
        Discharges the source at a defined power over a delta_t duration, capping
        the output to the energy stored at the moment.
        Returns actual energy spent.
        """
        output_energy = min(abs(power) * delta_t / self.efficiency, self.state.energy)
        self.energy = max(0.0, self.state.energy - output_energy)
        return output_energy


@dataclass
class Battery(EnergySource):
    """
    Models a generic, rechargeable battery type.
    """
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 battery_mass: float,
                 soh: float=BATTERY_DEFAULT_SOH,
                 efficiency: float=BATTERY_EFFICIENCY_DEFAULT):
        state = EnergySourceState(delivering=False,
                                  receiving=False,
                                  energy=energy,
                                  power=0.0)
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         system_mass=battery_mass,
                         soh=soh,
                         efficiency=efficiency)


@dataclass
class BatteryNonRechargeable(EnergySource):
    """
    Models a generic, non rechargeable battery type.
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
                         energy_medium=PowerType.ELECTRIC,
                         soh=soh,
                         efficiency=efficiency,
                         rechargeable=False)


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
        assert fuel.density is not None
        conversion = fuel.energy_density * fuel.density * LTS_TO_CUBIC_METERS
        super().__init__(name=name,
                         nominal_energy=capacity_litres*conversion,
                         energy=litres*conversion,
                         system_mass=tank_mass,
                         energy_medium=fuel,
                         soh=1.0,
                         efficiency=1.0,
                         rechargeable=False)


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
                         energy_medium=fuel,
                         soh=1.0,
                         efficiency=1.0,
                         rechargeable=False)
