"""This module defines the internal states of the components."""

from dataclasses import dataclass
from typing import Any, Optional
from components.fuel_type import Fuel
from helpers.functions import assert_type, assert_type_and_range, assert_range, \
    rpm_to_ang_vel, power_to_torque


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
    delivering: bool
    receiving: bool

    def __post_init__(self):
        assert_type(self.delivering, self.receiving,
                    expected_type=bool)

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
    temperature: float
    on: bool

    def __post_init__(self):
        assert_type_and_range(self.temperature,
                              more_than=0.0,
                              include_more=False)
        assert_type(self.on,
                    expected_type=bool)

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["temperature"] = self.temperature
        return base


@dataclass
class EnergyStorageState(BaseState):
    """
    Represents the energy storage state of a component.
    """
    energy: float
    fuel: Optional[Fuel]

    def __post_init__(self):
        assert_type_and_range(self.energy,
                              more_than=0.0)
        assert_type(self.fuel,
                    expected_type=Fuel,
                    allow_none=True)

    @property
    def fuel_amount(self) -> float:
        """
        Returns the amount of fuel left, if applicable.
        """
        if self.fuel is not None:
            return self.energy * self.fuel.energy_density
        return 0.0

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["energy"] = self.energy
        if self.fuel is not None:
            base["fuel"] = self.fuel
            base["fuel_amount"] = self.fuel_amount
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
        return base


@dataclass
class FuelIOState(IOState):
    """
    Represents the state of fuel transfer.
    """
    fuel: Fuel
    energy: float

    def __post_init__(self):
        assert_type(self.fuel,
                    expected_type=Fuel)
        assert_type_and_range(self.energy,
                              more_than=0.0)
        super().__post_init__()

    @property
    def fuel_amount(self) -> float:
        """
        Dynamically calculates the amount of fuel transfered.
        """
        return self.energy / self.fuel.energy_density

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["fuel_amount"] = self.fuel_amount
        return base


#=============================


@dataclass
class State():
    """
    Class containing all component's states.
    """
    input: Optional[IOState]
    output: IOState
    internal: InternalState
    energy_storage: Optional[EnergyStorageState]

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=IOState,
                    allow_none=True)
        assert_type(self.output,
                    expected_type=IOState)
        assert_type(self.internal,
                    expected_type=InternalState)
        assert_type(self.energy_storage,
                    expected_type=EnergyStorageState,
                    allow_none=True)


def zero_rotating_io_state() -> RotatingIOState:
    """
    Returns a mechanical rotating state with values set to zero.
    """
    return RotatingIOState(delivering=False,
                           receiving=False,
                           power=0.0,
                           rpm=0.0)

def zero_electric_io_state() -> ElectricIOState:
    """
    Returns an electric state with values set to zero.
    """
    return ElectricIOState(delivering=False,
                           receiving=False,
                           power=0.0)

def zero_fuel_io_state(fuel: Fuel) -> FuelIOState:
    """
    Returns a fuel state with values set to zero.
    """
    return FuelIOState(delivering=False,
                       receiving=False,
                       fuel=fuel,
                       energy=0.0)

def zero_internal_state(temperature: float=300.0,
                        on: bool=True) -> InternalState:
    """
    Returns an internal state with values set to zero.
    """
    return InternalState(temperature=temperature,
                         on=on)
