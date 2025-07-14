"""This module defines the internal states of the components."""

from dataclasses import dataclass
from typing import Any
from components.fuel_type import Fuel
from helpers.functions import assert_type, assert_type_and_range, assert_range
from simulation.constants import RPM_TO_ANG_VEL


@dataclass
class IOState():
    """
    Base class for input and output states.
    """
    pass


@dataclass
class InternalState():
    """
    Represents the internal state of a component.
    """
    pass


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

    @property
    def torque(self) -> float:
        """
        Dynamically calculate torque.
        """
        return self.power / self.ang_vel if self.rpm > 0.0 else 0.0

    @property
    def ang_vel(self) -> float:
        """
        Dynamically calculate angular velocity.
        """
        return self.rpm * RPM_TO_ANG_VEL


@dataclass
class ElectricalIOState(IOState):
    """
    Represents the state of an electrical condition (voltage and current).
    """
    power: float

    def __post_init__(self):
        assert_range(self.power,
                     more_than=0.0)


@dataclass
class FuelIOState(IOState):
    """
    Represents the state of fuel transfer.
    """
    fuel: Fuel
    fuel_amount: float

    @property
    def energy(self):
        """
        Dinamically calculates the energy transfered.
        """
        return self.fuel_amount * self.fuel.energy_density

    @property
    def fuel_state(self):
        """
        Returns the state of the transfered fuel.
        """
        return self.fuel.state


@dataclass
class PhysicalState(InternalState):
    """
    Represents basic physical properties of the component.
    """
    temperature: float


@dataclass
class State():
    """
    Base class for the internal states during simulation.
    """
    power: float
    delivering: bool
    receiving: bool

    def __post_init__(self):
        assert_type(self.delivering, self.receiving,
                    expected_type=bool)
        assert_type_and_range(self.power,
                              more_than=0.0)

    def as_dict(self) -> dict[str, Any]:
        """
        Serializes the state into a dictionary.
        """
        return self.__dict__


@dataclass
class MechanicalState(State):
    """
    State that represents components with mechanical moving parts.
    Includes motors, engines, transmissions, and others.
    """
    rpm: float
    on: bool

    def __post_init__(self):
        super().__post_init__()
        assert_type_and_range(self.power, self.rpm,
                              more_than=0.0)
        assert_type(self.on,
                    expected_type=bool)

    @property
    def torque(self) -> float:
        """
        Dynamically calculate torque.
        """
        return self.power / self.rpm / RPM_TO_ANG_VEL if self.rpm > 0.0 else 0.0

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["torque"] = self.torque
        return base


@dataclass
class ElectricalState(State):
    """
    State that represents components of pure electrical behavior.
    Includes Fuel Cells.
    """
    on: bool

    def __post_init__(self):
        super().__post_init__()
        assert_type(self.on,
                    expected_type=bool)


@dataclass
class EnergyInternalState(State):
    """
    The internal state of a battery or fuel tank.
    """
    energy: float

    def __post_init__(self):
        super().__post_init__()
        assert_type_and_range(self.energy,
                              more_than=0.0)


@dataclass
class FuelState(EnergyInternalState):
    """
    The state of a fuel tank.
    """
    fuel: Fuel
    fuel_amount: float

    def __post_init__(self):
        super().__post_init__()
        assert_type_and_range(self.fuel_amount,
                              more_than=0.0)


def zero_mechanical_state(on: bool=True) -> MechanicalState:
    """
    Returns a mechanical state with values set to zero.
    """
    assert_type(on,
                expected_type=bool)
    return MechanicalState(power=0.0,
                           delivering=False,
                           receiving=False,
                           rpm=0.0,
                           on=on)

def zero_electrical_state(on: bool=True) -> ElectricalState:
    """
    Returns an electrical state with values set to zero.
    """
    assert_type(on,
                expected_type=bool)
    return ElectricalState(power=0.0,
                           delivering=False,
                           receiving=False,
                           on=on)

def zero_energy_internal_state(energy: float=0.0) -> EnergyInternalState:
    """
    Returns a fuel state with values set to zero.
    """
    assert_range(energy,
                 more_than=0.0)
    return EnergyInternalState(energy=energy,
                               power=0.0,
                               delivering=False,
                               receiving=False)

def zero_fuel_state(fuel: Fuel) -> FuelState:
    """
    Returns a fuel state with values set to zero.
    """
    assert_type(fuel,
                expected_type=Fuel)
    return FuelState(energy=0.0,
                     power=0.0,
                     fuel=fuel,
                     fuel_amount=0.0,
                     delivering=False,
                     receiving=False)
