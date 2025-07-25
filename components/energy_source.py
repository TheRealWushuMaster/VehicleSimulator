"""This module contains a base class for all power sources for the vehicle."""

from dataclasses import dataclass, field
from typing import Optional, Callable
from uuid import uuid4
from components.fuel_type import Fuel, LiquidFuel, GaseousFuel
from components.port import Port, PortInput, PortOutput, PortBidirectional, PortType
from components.state import EnergyStorageState, InternalState, State, \
    ElectricIOState, FuelIOState, RotatingIOState
from helpers.functions import assert_type, assert_type_and_range
from helpers.types import PowerType
from simulation.constants import BATTERY_EFFICIENCY_DEFAULT, \
    BATTERY_DEFAULT_SOH, LTS_TO_CUBIC_METERS, EPSILON


@dataclass
class EnergySource():
    """
    Base class for modules that only store and deliver energy.
    
    Attributes:
        - `id` (str): identifier for the object
        - `name` (str): the name of the energy source
        - `nominal_energy` (float): the maximum energy to be stored (Joules)
        - `input` (Port type or None): sets input port and marks whether the
                energy source can be recharged
        - `output` (Port type): sets the type of output port
        - `state` (EnergyState): includes the state values, including energy
        - `system_mass` (float): the mass of the system (kg) without including
                the mass of any fuel used
        - `soh` (float): models the degradation of the source [0.0-1.0]
        - `efficiency` (float): efficiency when delivering or receiving [0.0-1.0]
        - `rechargeable` (bool): allows the source to be recharged
    """
    name: str
    input: Optional[PortInput|PortBidirectional]
    output: PortOutput|PortBidirectional
    system_mass: float
    soh: float
    efficiency: Callable[[State], float]

    def __post_init__(self):
        assert_type(self.name,
                    expected_type=str)
        assert_type_and_range(self.nominal_energy,
                              self.system_mass,
                              more_than=0.0)
        assert_type_and_range(self.efficiency, self.soh,
                              more_than=0.0,
                              less_than=1.0)
        if self.input is not None:
            self.rechargeable = True
            assert self.input.exchange==self.output.exchange
        else:
            self.rechargeable = False
        st_list = []
        for obj in (self.input, self.output):
            if obj is not None:
                if isinstance(obj.exchange, Fuel):
                    st = FuelIOState(delivering=False,
                                     receiving=False,
                                     fuel=obj.exchange,
                                     energy=0.0)
                elif obj.exchange==PowerType.ELECTRIC:
                    st = ElectricIOState(delivering=False,
                                         receiving=False,
                                         power=0.0,
                                         current=0.0)
                elif obj.exchange==PowerType.MECHANICAL:
                    st = RotatingIOState(delivering=False,
                                         receiving=False,
                                         power=0.0,
                                         rpm=0.0)
                else:
                    raise TypeError("Must be a fuel, or electric/mechanical power.")
            else:
                st = None
            st_list.append(st)
        self.state = State(input=st_list[0],
                           output=st_list[1],
                           internal=InternalState(temperature=300.0,
                                                  on=True),
                           energy_storage=EnergyStorageState(energy=0.0,
                                                             fuel=self.output.exchange
                                                             if isinstance(self.output.exchange, Fuel)
                                                             else None))
        if self.input is not None:
            assert self.input.exchange==self.output.exchange
        self.nominal_energy = max(self.nominal_energy, EPSILON)
        self.id = f"EnergySource-{uuid4()}"

    @property
    def soc(self) -> float:
        """
        Returns the source's current state of charge (SOC).
        """
        assert self.state.energy_storage is not None
        return self.state.energy_storage.energy / self.nominal_energy / self.soh

    @property
    def energy_medium(self) -> Fuel|PowerType:
        """
        Returns the energy medium of the energy source.
        """
        return self.output.exchange

    @property
    def max_energy(self) -> float:
        """
        Returns the maximum amount of energy
        that can be held by the source.
        """
        raise NotImplementedError

    @property
    def is_empty(self) -> bool:
        """
        Check if the source has no usable energy left.
        """
        raise NotImplementedError

    @property
    def is_full(self) -> bool:
        """
        Check if the source cannot receive any more energy.
        """
        raise NotImplementedError

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
            assert self.state.energy_storage is not None
            return self.state.energy_storage.energy / self.energy_medium.energy_density
        return 0.0

    @property
    def total_mass(self) -> float:
        """
        Returns the total mass of the power source.
        """
        raise NotImplementedError

    def recharge(self, power: float, delta_t: float) -> float:
        """
        Attempts to recharge this source with the given power (W) over delta_t (s).
        Returns actual energy stored.
        """
        if self.rechargeable:
            input_energy = abs(power) * delta_t * self.efficiency
            assert self.state.energy_storage is not None
            self.state.energy_storage.energy = min(self.max_energy, self.state.energy_storage.energy + input_energy)
            return input_energy
        return 0.0

    def discharge(self, power: float, delta_t: float) -> float:
        """
        Discharges the source at a defined power over a delta_t duration, capping
        the output to the energy stored at the moment.
        Returns actual energy spent.
        """
        assert self.state.energy_storage is not None
        output_energy = min(abs(power) * delta_t / self.efficiency, self.state.energy_storage.energy)
        self.state.energy_storage.energy = max(0.0, self.state.energy_storage.energy - output_energy)
        return output_energy

    def return_port(self, which: PortType) -> Optional[Port]:
        """
        Returns the requested Port object.
        """
        assert_type(which,
                    expected_type=PortType)
        if which==PortType.INPUT_PORT:
            return self.input
        return self.output


@dataclass
class Battery(EnergySource):
    """
    Models a generic battery.
    """
    nominal_energy: float
    nominal_voltage: float
    voltage_vs_current: Callable[[State], float]
    efficiency: Callable[[State], float]

    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 battery_mass: float,
                 rechargeable: bool,
                 nominal_voltage: float,
                 efficiency: Callable[[State], float],
                 voltage_vs_current: Callable[[State], float],
                 soh: float=BATTERY_DEFAULT_SOH):
        super().__init__(name=name,
                         input=PortInput(exchange=PowerType.ELECTRIC) if rechargeable else None,
                         output=PortOutput(exchange=PowerType.ELECTRIC),
                         system_mass=battery_mass,
                         soh=soh,
                         efficiency=efficiency)
        assert self.state.energy_storage is not None
        self.state.energy_storage.energy = min(nominal_energy, energy)
        assert_type_and_range(nominal_voltage,
                              more_than=0.0)
        self.nominal_energy = nominal_energy
        self.nominal_voltage = nominal_voltage
        self.voltage_vs_current = voltage_vs_current
        self.efficiency = efficiency

    @property
    def max_energy(self):
        return self.nominal_energy * self.soh

    @property
    def is_empty(self):
        assert self.state.energy_storage is not None
        return self.state.energy_storage.energy <= 0.0

    @property
    def is_full(self):
        assert self.state.energy_storage is not None
        return self.state.energy_storage.energy == self.max_energy

    @property
    def total_mass(self):
        return self.system_mass


@dataclass
class BatteryRechargeable(Battery):
    """
    Models a generic, rechargeable battery.
    """
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 battery_mass: float,
                 soh: float,
                 efficiency: Callable[[State], float],
                 nominal_voltage: float,
                 voltage_vs_current: Callable[[State], float]):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         battery_mass=battery_mass,
                         soh=soh,
                         efficiency=efficiency,
                         rechargeable=True,
                         nominal_voltage=nominal_voltage,
                         voltage_vs_current=voltage_vs_current)


@dataclass
class BatteryNonRechargeable(Battery):
    """
    Models a generic, rechargeable battery type.
    """
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 energy: float,
                 battery_mass: float,
                 soh: float,
                 efficiency: Callable[[State], float],
                 nominal_voltage: float,
                 voltage_vs_current: Callable[[State], float]):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         energy=energy,
                         battery_mass=battery_mass,
                         soh=soh,
                         efficiency=efficiency,
                         rechargeable=False,
                         nominal_voltage=nominal_voltage,
                         voltage_vs_current=voltage_vs_current)


@dataclass
class LiquidFuelTank(EnergySource):
    """
    Models a fuel tank for a liquid fuel.
    """
    max_liters: float
    fuel: LiquidFuel

    def __init__(self,
                 name: str,
                 fuel: LiquidFuel,
                 max_liters: float,
                 liters: float,
                 tank_mass: float):
        assert_type(fuel,
                    expected_type=LiquidFuel)
        assert fuel.density is not None
        conversion = fuel.energy_density * fuel.density * LTS_TO_CUBIC_METERS
        super().__init__(name=name,
                         input=None,
                         output=PortOutput(exchange=fuel),
                         system_mass=tank_mass,
                         soh=1.0,
                         efficiency=1.0)
        assert self.state.energy_storage is not None
        self.state.energy_storage.energy = liters * conversion


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
        assert_type(fuel,
                    expected_type=GaseousFuel)
        super().__init__(name=name,
                         nominal_energy=capacity_kg*fuel.energy_density,
                         input=None,
                         output=PortOutput(exchange=fuel),
                         system_mass=tank_mass,
                         soh=1.0,
                         efficiency=1.0)
        assert self.state.energy_storage is not None
        self.state.energy_storage.energy = kg * fuel.energy_density
