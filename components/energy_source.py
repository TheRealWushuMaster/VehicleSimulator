"""This module contains a base class for all power sources for the vehicle."""

from abc import ABC
from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4
from components.consumption import RechargeableBatteryConsumption, \
    NonRechargeableBatteryConsumption
from components.fuel_type import Fuel, LiquidFuel, GaseousFuel
from components.port import Port, PortInput, PortOutput, PortBidirectional, PortType
from components.state import \
    FullStateElectricEnergyStorageNoInput, FullStateElectricEnergyStorageWithInput, \
    FullStateFuelStorageNoInput, \
    LiquidFuelTankState, GaseousFuelTankState, \
    return_rechargeable_battery_state, return_non_rechargeable_battery_state, \
    return_liquid_fuel_tank_state, return_gaseous_fuel_tank_state
from helpers.functions import assert_type, assert_type_and_range, liters_to_cubic_meters
from helpers.types import PowerType, ElectricSignalType
from simulation.constants import BATTERY_DEFAULT_SOH


@dataclass
class EnergySource(ABC):
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
    state: FullStateElectricEnergyStorageNoInput| \
        FullStateFuelStorageNoInput| \
        FullStateElectricEnergyStorageWithInput

    def __post_init__(self):
        assert_type(self.name,
                    expected_type=str)
        assert_type_and_range(self.system_mass,
                              more_than=0.0)
        assert_type(self.state,
                    expected_type=(FullStateElectricEnergyStorageNoInput,
                                   FullStateElectricEnergyStorageWithInput,
                                   FullStateFuelStorageNoInput))
        if self.input is not None:
            assert self.input.exchange==self.output.exchange
            self.rechargeable = True
        else:
            self.rechargeable = False
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
    max_power: float
    efficiency: RechargeableBatteryConsumption|NonRechargeableBatteryConsumption
    soh: float=BATTERY_DEFAULT_SOH
    signal_type: ElectricSignalType=field(init=False)

    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 battery_mass: float,
                 rechargeable: bool,
                 nominal_voltage: float,
                 efficiency: RechargeableBatteryConsumption | NonRechargeableBatteryConsumption,
                 soh: float=BATTERY_DEFAULT_SOH):
        state: FullStateElectricEnergyStorageNoInput|FullStateElectricEnergyStorageWithInput
        if rechargeable:
            state = return_rechargeable_battery_state(energy=min(nominal_energy, energy),
                                                      nominal_voltage=nominal_voltage)
        else:
            state = return_non_rechargeable_battery_state(energy=min(nominal_energy, energy),
                                                          nominal_voltage=nominal_voltage)
        super().__init__(name=name,
                         input=PortInput(exchange=PowerType.ELECTRIC_DC) if rechargeable else None,
                         output=PortOutput(exchange=PowerType.ELECTRIC_DC),
                         system_mass=battery_mass,
                         state=state)
        assert_type_and_range(nominal_voltage, max_power,
                              more_than=0.0)
        assert_type_and_range(soh,
                              more_than=0.0,
                              less_than=1.0)
        self.nominal_energy = nominal_energy
        self.nominal_voltage = nominal_voltage
        self.max_power = max_power
        self.efficiency = efficiency
        self.soh = soh
        self.signal_type = ElectricSignalType.DC

    @property
    def soc(self) -> float:
        """
        Returns the source's current state of charge (SOC).
        """
        assert isinstance(self.state,
                          (FullStateElectricEnergyStorageNoInput,
                           FullStateElectricEnergyStorageWithInput))
        return self.state.electric_energy_storage.energy / self.nominal_energy / self.soh

    @property
    def max_energy(self):
        return self.nominal_energy * self.soh

    @property
    def is_empty(self):
        assert isinstance(self.state, (FullStateElectricEnergyStorageNoInput,
                                       FullStateElectricEnergyStorageWithInput))
        return self.state.electric_energy_storage.energy <= 0.0

    @property
    def is_full(self):
        assert isinstance(self.state, (FullStateElectricEnergyStorageNoInput,
                                       FullStateElectricEnergyStorageWithInput))
        return self.state.electric_energy_storage.energy == self.max_energy

    @property
    def total_mass(self):
        return self.system_mass


@dataclass
class BatteryRechargeable(Battery):
    """
    Models a generic, rechargeable battery.
    """
    efficiency: RechargeableBatteryConsumption  # type: ignore

    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 battery_mass: float,
                 soh: float,
                 efficiency: RechargeableBatteryConsumption,
                 nominal_voltage: float):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=battery_mass,
                         soh=soh,
                         efficiency=efficiency,
                         rechargeable=True,
                         nominal_voltage=nominal_voltage)


@dataclass
class BatteryNonRechargeable(Battery):
    """
    Models a generic, non rechargeable battery type.
    """
    efficiency: NonRechargeableBatteryConsumption  # type: ignore

    def __init__(self,
                 name: str,
                 nominal_energy: float,
                 max_power: float,
                 energy: float,
                 battery_mass: float,
                 soh: float,
                 efficiency: NonRechargeableBatteryConsumption,
                 nominal_voltage: float):
        super().__init__(name=name,
                         nominal_energy=nominal_energy,
                         max_power=max_power,
                         energy=energy,
                         battery_mass=battery_mass,
                         soh=soh,
                         efficiency=efficiency,
                         rechargeable=False,
                         nominal_voltage=nominal_voltage)


@dataclass
class FuelTank(EnergySource):
    """
    Base class for fuel tanks.
    """
    fuel: Fuel

    def __init__(self,
                 name: str,
                 fuel: Fuel,
                 tank_mass: float,
                 state: FullStateFuelStorageNoInput):
        super().__init__(name=name,
                         input=None,
                         output=PortOutput(exchange=fuel),
                         system_mass=tank_mass,
                         state=state)

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
    fuel: LiquidFuel # type: ignore
    capacity_liters: float
    state: LiquidFuelTankState # type: ignore

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
        state = return_liquid_fuel_tank_state(fuel=fuel,
                                              fuel_liters_stored=liters)
        super().__init__(name=name,
                         fuel=fuel,
                         tank_mass=tank_mass,
                         state=state)
        self.capacity_liters = capacity_liters

    @property
    def fuel_mass(self):
        return liters_to_cubic_meters(self.state.fuel_storage.fuel_liters) * \
            self.state.fuel_storage.fuel.mass_density

    @property
    def is_empty(self) -> bool:
        return self.state.fuel_storage.fuel_liters==0.0

    @property
    def is_full(self) -> bool:
        return self.state.fuel_storage.fuel_liters==self.capacity_liters

    @property
    def max_energy(self) -> float:
        return liters_to_cubic_meters(liters=self.state.fuel_storage.fuel_liters) * \
            self.state.fuel_storage.fuel.mass_density * self.state.fuel_storage.fuel.energy_density

    @property
    def filled_percentage(self) -> float:
        return self.state.fuel_storage.fuel_liters / self.capacity_liters


@dataclass
class GaseousFuelTank(FuelTank):
    """
    Models a gaseous fuel tank.
    """
    fuel: GaseousFuel # type: ignore
    capacity_mass: float
    state: GaseousFuelTankState # type: ignore

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
        state = return_gaseous_fuel_tank_state(fuel=fuel,
                                               fuel_mass_stored=fuel_mass)
        super().__init__(name=name,
                         fuel=fuel,
                         tank_mass=tank_mass,
                         state=state)
        self.capacity_mass = capacity_mass

    @property
    def fuel_mass(self):
        return self.state.fuel_storage.fuel_mass

    @property
    def is_empty(self) -> bool:
        return self.state.fuel_storage.fuel_mass==0.0

    @property
    def is_full(self) -> bool:
        return self.state.fuel_storage.fuel_mass==self.capacity_mass

    @property
    def max_energy(self) -> float:
        return liters_to_cubic_meters(liters=self.state.fuel_storage.fuel_mass) * \
            self.state.fuel_storage.fuel.energy_density

    @property
    def filled_percentage(self) -> float:
        return self.state.fuel_storage.fuel_mass / self.capacity_mass
