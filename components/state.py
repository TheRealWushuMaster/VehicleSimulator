"""This module defines the internal states of the components."""

from dataclasses import dataclass, field
from typing import Any, Optional
from components.fuel_type import Fuel
from helpers.functions import assert_type, assert_type_and_range, assert_range, \
    rpm_to_ang_vel, power_to_torque, kelvin_to_celsius, kelvin_to_fahrenheit


@dataclass
class BaseState():
    """
    Base class for all state classes.
    """
    def as_dict(self) -> dict[str, Any]:
        """
        Serializes the state into a dictionary.
        """
        return self.__dict__


@dataclass
class IOState(BaseState):
    """
    Base class for input and output states.
    """
    _is_del: Optional[bool]=field(init=False)

    def __post_init__(self):
        self._is_del = None

    def set_delivering(self):
        self._is_del = True

    def set_receiving(self):
        self._is_del = False

    @property
    def delivering(self):
        return self._is_del==True

    @property
    def receiving(self):
        return self._is_del==False

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["delivering"] = self.delivering
        base["receiving"] = self.receiving
        return base


@dataclass
class InternalState(BaseState):
    """
    Represents basic internal properties of the component.
    """
    temperature_kelvin: float
    on: bool

    def __post_init__(self):
        assert_type_and_range(self.temperature_kelvin,
                              more_than=0.0,
                              include_more=False)
        assert_type(self.on,
                    expected_type=bool)

    @property
    def temperature_celsius(self):
        """
        Dynamically calculate the temperature in Celsius.
        """
        return kelvin_to_celsius(t_kelvin=self.temperature_kelvin)

    @property
    def temperature_fahrenheit(self):
        """
        Dynamically calculate the temperature in Fahrenheit.
        """
        return kelvin_to_fahrenheit(t_kelvin=self.temperature_kelvin)

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["temperature_kelvin"] = self.temperature_kelvin
        base["temperature_celsius"] = self.temperature_celsius
        base["temperature_fahrenheit"] = self.temperature_fahrenheit
        base["on"] = self.on
        return base


#=============================


@dataclass
class ElectricEnergyStorageState(BaseState):
    """
    Represents the energy storage state of a component.
    """
    energy: float

    def __post_init__(self):
        assert_type_and_range(self.energy,
                              more_than=0.0)

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["energy"] = self.energy
        return base


@dataclass
class FuelStorageState(BaseState):
    """
    Represents the state of storing fuel.
    """
    fuel: Fuel

    def __post_init__(self):
        assert_type(self.fuel,
                    expected_type=Fuel)

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["fuel"] = self.fuel
        return base


@dataclass
class LiquidFuelStorageState(FuelStorageState):
    """
    Represents the liquid fuel storage of a fuel tank.
    """
    fuel_liters: float

    def __post_init__(self):
        assert_type_and_range(self.fuel_liters,
                              more_than=0.0)
        super().__post_init__()

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["fuel_liters"] = self.fuel_liters
        return base


@dataclass
class GaseousFuelStorageState(FuelStorageState):
    """
    Represents the gaseous fuel storage of a fuel tank.
    """
    fuel_mass: float

    def __post_init__(self):
        assert_type_and_range(self.fuel_mass,
                              more_than=0.0)
        super().__post_init__()

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["fuel_mass"] = self.fuel_mass
        return base


#=============================


@dataclass
class RotatingIOState(IOState):
    """
    Represents the state of a rotating component (motor, engine, etc).
    """
    power: float
    rpm: float

    def __post_init__(self):
        assert_range(self.power, self.rpm,
                     more_than=0.0)
        super().__post_init__()

    @property
    def torque(self) -> float:
        """
        Dynamically calculate torque.
        """
        return power_to_torque(power=self.power,
                               rpm=self.rpm)

    @property
    def ang_vel(self) -> float:
        """
        Dynamically calculate angular velocity.
        """
        return rpm_to_ang_vel(rpm=self.rpm)

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["torque"] = self.torque
        base["ang_vel"] = self.ang_vel
        return base


@dataclass
class ElectricIOState(IOState):
    """
    Represents the state of an electrical condition (voltage and current).
    """
    power: float
    current: float

    def __post_init__(self):
        assert_range(self.power,
                     more_than=0.0)
        super().__post_init__()

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["power"] = self.power
        base["current"] = self.current
        return base


@dataclass
class FuelIOState(IOState):
    """
    Represents the state of a fuel transfer.
    """
    fuel: Fuel

    def __post_init__(self):
        assert_type(self.fuel,
                    expected_type=Fuel)
        super().__post_init__()

    @property
    def energy(self):
        """
        Must implement a property to calculate the energy transfered.
        """
        raise NotImplementedError

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["fuel"] = self.fuel
        return base


@dataclass
class LiquidFuelIOState(FuelIOState):
    """
    Represents the state of liquid fuel transfer.
    """
    fuel_liters: float

    def __post_init__(self):
        assert_type_and_range(self.fuel_liters,
                              more_than=0.0)
        super().__post_init__()

    @property
    def energy(self) -> float:
        """
        Dynamically calculates the amount of energy transfered.
        """
        return self.fuel_liters * self.fuel.energy_density

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["energy"] = self.energy
        return base


@dataclass
class GaseousFuelIOState(FuelIOState):
    """
    Represents the state of gaseous fuel transfer.
    """
    fuel_mass: float

    def __post_init__(self):
        assert_type_and_range(self.fuel_mass,
                              more_than=0.0)
        super().__post_init__()

    @property
    def energy(self) -> float:
        """
        Dynamically calculates the amount of energy transfered.
        """
        return self.fuel_mass * self.fuel.energy_density

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["energy"] = self.energy
        return base


#=============================


@dataclass
class State():
    """
    Class containing all components' states.
    """
    input: Optional[IOState]
    output: IOState
    internal: Optional[InternalState]
    electric_energy_storage: Optional[ElectricEnergyStorageState]
    fuel_storage: Optional[FuelStorageState]

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=IOState,
                    allow_none=True)
        assert_type(self.output,
                    expected_type=IOState)
        assert_type(self.internal,
                    expected_type=InternalState)
        assert_type(self.electric_energy_storage,
                    expected_type=ElectricEnergyStorageState,
                    allow_none=True)
        assert_type(self.fuel_storage,
                    expected_type=FuelStorageState)


def zero_rotating_io_state() -> RotatingIOState:
    """
    Returns a mechanical rotating state with values set to zero.
    """
    return RotatingIOState(power=0.0,
                           rpm=0.0)

def zero_electric_io_state() -> ElectricIOState:
    """
    Returns an electric state with values set to zero.
    """
    return ElectricIOState(power=0.0,
                           current= 0.0)

def zero_liquid_fuel_io_state(fuel: Fuel) -> LiquidFuelIOState:
    """
    Returns a liquid fuel state with values set to zero.
    """
    return LiquidFuelIOState(fuel=fuel,
                             fuel_liters=0.0)

def zero_gaseous_fuel_io_state(fuel: Fuel) -> GaseousFuelIOState:
    """
    Returns a liquid fuel state with values set to zero.
    """
    return GaseousFuelIOState(fuel=fuel,
                              fuel_mass=0.0)

def zero_internal_state(temperature: float=300.0,
                        on: bool=False) -> InternalState:
    """
    Returns an internal state with values set to zero.
    """
    assert_type_and_range(temperature,
                          more_than=0.0)
    return InternalState(temperature_kelvin=temperature,
                         on=on)
