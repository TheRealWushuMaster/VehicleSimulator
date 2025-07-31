"""This module contains a base class for all power sources for the vehicle."""

from dataclasses import dataclass
from typing import Optional, Callable
from uuid import uuid4
from components.fuel_type import Fuel, LiquidFuel, GaseousFuel
from components.port import Port, PortInput, PortOutput, PortBidirectional, PortType
from components.state import ElectricEnergyStorageState, InternalState, State, \
    ElectricIOState, LiquidFuelIOState, GaseousFuelIOState, RotatingIOState, \
    LiquidFuelStorageState, GaseousFuelStorageState
from helpers.functions import assert_type, assert_type_and_range, liters_to_cubic_meters
from helpers.types import PowerType
from simulation.constants import BATTERY_DEFAULT_SOH, DEFAULT_TEMPERATURE


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

    def __post_init__(self):
        assert_type(self.name,
                    expected_type=str)
        assert_type_and_range(self.system_mass,
                              more_than=0.0)
        if self.input is not None:
            assert self.input.exchange==self.output.exchange
            self.rechargeable = True
        else:
            self.rechargeable = False
        self.state = return_energy_source_base_state(es=self)
        if self.input is not None:
            assert self.input.exchange==self.output.exchange
        self.id = f"EnergySource-{uuid4()}"

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
    def total_mass(self) -> float:
        """
        Returns the total mass of the power source.
        """
        raise NotImplementedError

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
    max_current: float
    voltage_vs_current: Callable[[float], float]
    efficiency: Callable[[float], float]
    soh: float=BATTERY_DEFAULT_SOH

    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_current: float,
                 energy: float,
                 battery_mass: float,
                 rechargeable: bool,
                 nominal_voltage: float,
                 efficiency: Callable[[float], float],
                 voltage_vs_current: Callable[[float], float],
                 soh: float=BATTERY_DEFAULT_SOH):
        super().__init__(name=name,
                         input=PortInput(exchange=PowerType.ELECTRIC) if rechargeable else None,
                         output=PortOutput(exchange=PowerType.ELECTRIC),
                         system_mass=battery_mass)
        assert self.state.electric_energy_storage is not None
        self.state.electric_energy_storage.energy = min(nominal_energy, energy)
        assert_type_and_range(nominal_voltage, max_current,
                              more_than=0.0)
        assert_type_and_range(soh,
                              more_than=0.0,
                              less_than=1.0)
        self.nominal_energy = nominal_energy
        self.nominal_voltage = nominal_voltage
        self.max_current = max_current
        self.voltage_vs_current = voltage_vs_current
        self.efficiency = efficiency
        self.soh = soh

    @property
    def soc(self) -> float:
        """
        Returns the source's current state of charge (SOC).
        """
        assert self.state.electric_energy_storage is not None
        return self.state.electric_energy_storage.energy / self.nominal_energy / self.soh

    @property
    def max_energy(self):
        return self.nominal_energy * self.soh

    @property
    def is_empty(self):
        assert self.state.electric_energy_storage is not None
        return self.state.electric_energy_storage.energy <= 0.0

    @property
    def is_full(self):
        assert self.state.electric_energy_storage is not None
        return self.state.electric_energy_storage.energy == self.max_energy

    @property
    def total_mass(self):
        return self.system_mass

    def discharge(self, power: float, delta_t: float) -> float:
        """
        Discharges the battery at a defined power over a delta_t duration,
        capping the output to the energy stored at the moment.
        Returns actual energy spent.
        """
        assert self.state.electric_energy_storage is not None
        assert isinstance(self.state.output, ElectricIOState)
        output_energy = min(abs(power) * delta_t / self.efficiency(self.state.output.current), # pylint: disable=no-member
                            self.state.electric_energy_storage.energy)
        self.state.electric_energy_storage.energy = max(0.0, self.state.electric_energy_storage.energy - output_energy)
        return output_energy


@dataclass
class BatteryRechargeable(Battery):
    """
    Models a generic, rechargeable battery.
    """
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_current: float,
                 energy: float,
                 battery_mass: float,
                 soh: float,
                 efficiency: Callable[[float], float],
                 nominal_voltage: float,
                 voltage_vs_current: Callable[[float], float]):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_current=max_current,
                         energy=energy,
                         battery_mass=battery_mass,
                         soh=soh,
                         efficiency=efficiency,
                         rechargeable=True,
                         nominal_voltage=nominal_voltage,
                         voltage_vs_current=voltage_vs_current)

    def recharge(self, power: float, delta_t: float) -> float:
        """
        Recharges the battery with the given power (W) over delta_t (s).
        Returns actual energy stored.
        """
        assert self.state.electric_energy_storage is not None
        assert isinstance(self.state.input, ElectricIOState)
        input_energy = abs(power) * delta_t * self.efficiency(self.state.input.current)
        self.state.electric_energy_storage.energy = min(self.max_energy,
                                                        self.state.electric_energy_storage.energy + input_energy)
        return input_energy


@dataclass
class BatteryNonRechargeable(Battery):
    """
    Models a generic, non rechargeable battery type.
    """
    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_current: float,
                 energy: float,
                 battery_mass: float,
                 soh: float,
                 efficiency: Callable[[float], float],
                 nominal_voltage: float,
                 voltage_vs_current: Callable[[float], float]):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_current=max_current,
                         energy=energy,
                         battery_mass=battery_mass,
                         soh=soh,
                         efficiency=efficiency,
                         rechargeable=False,
                         nominal_voltage=nominal_voltage,
                         voltage_vs_current=voltage_vs_current)


@dataclass
class FuelTank(EnergySource):
    """
    Base class for fuel tanks.
    """
    fuel: Fuel

    def __init__(self,
                 name: str,
                 fuel: Fuel,
                 tank_mass: float):
        super().__init__(name=name,
                         input=None,
                         output=PortOutput(exchange=fuel),
                         system_mass=tank_mass)

    @property
    def filled_percentage(self) -> float:
        """
        Returns the amount of fuel contents
        with respect to its maximum capacity.
        """
        raise NotImplementedError

    @property
    def fuel_mass(self) -> float:
        """
        Returns the mass of fuel contained.
        """
        raise NotImplementedError

    @property
    def is_empty(self) -> bool:
        raise NotImplementedError

    @property
    def is_full(self) -> bool:
        raise NotImplementedError

    @property
    def max_energy(self) -> float:
        raise NotImplementedError

    @property
    def total_mass(self) -> float:
        """
        Returns the total mass of the fuel tank.
        """
        return self.system_mass + self.fuel_mass


@dataclass
class LiquidFuelTank(FuelTank):
    """
    Models a liquid fuel tank.
    """
    capacity_liters: float

    def __init__(self,
                 name: str,
                 fuel: LiquidFuel,
                 capacity_liters: float,
                 liters: float,
                 tank_mass: float):
        assert_type(fuel,
                    expected_type=LiquidFuel)
        assert_type_and_range(capacity_liters,
                              more_than=0.0)
        assert_type_and_range(liters,
                              more_than=0.0,
                              less_than=capacity_liters)
        super().__init__(name=name,
                         fuel=fuel,
                         tank_mass=tank_mass)
        self.capacity_liters = capacity_liters
        assert isinstance(self.state.fuel_storage, LiquidFuelStorageState)
        self.state.fuel_storage.fuel_liters = liters

    @property
    def fuel_mass(self):
        assert isinstance(self.state.fuel_storage, LiquidFuelStorageState)
        assert isinstance(self.state.fuel_storage.fuel, LiquidFuel)
        return liters_to_cubic_meters(self.state.fuel_storage.fuel_liters) * \
            self.state.fuel_storage.fuel.mass_density

    @property
    def is_empty(self) -> bool:
        assert isinstance(self.state.fuel_storage, LiquidFuelStorageState)
        return self.state.fuel_storage.fuel_liters == 0.0

    @property
    def is_full(self) -> bool:
        assert isinstance(self.state.fuel_storage, LiquidFuelStorageState)
        return self.state.fuel_storage.fuel_liters == self.capacity_liters

    @property
    def max_energy(self) -> float:
        assert isinstance(self.state.fuel_storage, LiquidFuelStorageState)
        assert isinstance(self.state.fuel_storage.fuel, LiquidFuel)
        return liters_to_cubic_meters(liters=self.state.fuel_storage.fuel_liters) * \
            self.state.fuel_storage.fuel.mass_density * self.state.fuel_storage.fuel.energy_density

    @property
    def filled_percentage(self) -> float:
        assert isinstance(self.state.fuel_storage, LiquidFuelStorageState)
        return self.state.fuel_storage.fuel_liters / self.capacity_liters


@dataclass
class GaseousFuelTank(FuelTank):
    """
    Models a gaseous fuel tank.
    """
    capacity_mass: float

    def __init__(self,
                 name: str,
                 fuel: GaseousFuel,
                 capacity_mass: float,
                 fuel_mass: float,
                 tank_mass: float):
        assert_type(fuel,
                    expected_type=GaseousFuel)
        assert_type_and_range(capacity_mass,
                              more_than=0.0)
        assert_type_and_range(fuel_mass,
                              more_than=0.0,
                              less_than=capacity_mass)
        super().__init__(name=name,
                         fuel=fuel,
                         tank_mass=tank_mass)
        self.capacity_mass = capacity_mass
        assert isinstance(self.state.fuel_storage, GaseousFuelStorageState)
        self.state.fuel_storage.fuel_mass = fuel_mass

    @property
    def fuel_mass(self):
        assert isinstance(self.state.fuel_storage, GaseousFuelStorageState)
        return self.state.fuel_storage.fuel_mass

    @property
    def is_empty(self) -> bool:
        assert isinstance(self.state.fuel_storage, GaseousFuelStorageState)
        return self.state.fuel_storage.fuel_mass == 0.0

    @property
    def is_full(self) -> bool:
        assert isinstance(self.state.fuel_storage, GaseousFuelStorageState)
        return self.state.fuel_storage.fuel_mass == self.capacity_mass

    @property
    def max_energy(self) -> float:
        assert isinstance(self.state.fuel_storage, GaseousFuelStorageState)
        return liters_to_cubic_meters(liters=self.state.fuel_storage.fuel_mass) * \
            self.state.fuel_storage.fuel.energy_density

    @property
    def filled_percentage(self) -> float:
        assert isinstance(self.state.fuel_storage, GaseousFuelStorageState)
        return self.state.fuel_storage.fuel_mass / self.capacity_mass


def return_energy_source_base_state(es: EnergySource) -> State:
    """
    Returns an appropriate base state for an energy source.
    """
    st_list: list[Optional[LiquidFuelIOState|GaseousFuelIOState|\
        ElectricIOState|RotatingIOState]] = []
    for obj in (es.input, es.output):
        if obj is not None:
            if isinstance(obj.exchange, LiquidFuel):
                st_list.append(LiquidFuelIOState(fuel=obj.exchange,
                                                    fuel_liters=0.0))
            elif isinstance(obj.exchange, GaseousFuel):
                st_list.append(GaseousFuelIOState(fuel=obj.exchange,
                                                    fuel_mass=0.0))
            elif obj.exchange==PowerType.ELECTRIC:
                st_list.append(ElectricIOState(voltage=0.0,
                                               current=0.0))
            elif obj.exchange==PowerType.MECHANICAL:
                st_list.append(RotatingIOState(torque=0.0,
                                               rpm=0.0))
            else:
                raise TypeError("Must be a fuel or electric/mechanical power.")
        else:
            st_list.append(None)
    ees: Optional[ElectricEnergyStorageState] = None
    fs: Optional[LiquidFuelStorageState|GaseousFuelStorageState] = None
    if isinstance(es.output.exchange, LiquidFuel):
        fs = LiquidFuelStorageState(fuel=es.output.exchange,
                                    fuel_liters=0.0)
    elif isinstance(es.output.exchange, GaseousFuel):
        fs = GaseousFuelStorageState(fuel=es.output.exchange,
                                     fuel_mass=0.0)
    elif es.output.exchange==PowerType.ELECTRIC:
        ees = ElectricEnergyStorageState(energy=0.0)
    assert st_list[1] is not None
    return State(input=st_list[0],
                 output=st_list[1],
                 internal=InternalState(temperature_kelvin=DEFAULT_TEMPERATURE,
                                        on=True),
                 electric_energy_storage=ees,
                 fuel_storage=fs)
