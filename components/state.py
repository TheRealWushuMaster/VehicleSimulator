"""This module defines the internal states of the components."""

from dataclasses import dataclass
from typing import Any
from helpers.functions import assert_type, assert_type_and_range
from simulation.constants import RPM_TO_ANG_VEL


@dataclass
class State():
    """
    Base class for the internal states during simulation.
    """
    power: float
    efficiency: float
    delivering: bool
    receiving: bool

    def __post_init__(self):
        assert_type(self.delivering, self.receiving,
                    expected_type=bool)
        assert_type_and_range(self.power,
                              more_than=0.0)
        assert_type_and_range(self.efficiency,
                              more_than=0.0,
                              less_than=1.0)

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
class EnergyState(State):
    """
    The internal state of a battery or fuel tank.
    """
    energy: float

    def __post_init__(self):
        super().__post_init__()
        assert_type_and_range(self.energy,
                              more_than=0.0)


def zero_mechanical_state(on: bool=True) -> MechanicalState:
    """
    Returns an initial mechanical state with values set at zero.
    """
    assert_type(on,
                expected_type=bool)
    return MechanicalState(power=0.0,
                           efficiency=0.0,
                           delivering=False,
                           receiving=False,
                           rpm=0.0,
                           on=on)

def zero_electrical_state(on: bool=True) -> ElectricalState:
    """
    Returns an initial electrical state with values set at zero.
    """
    assert_type(on,
                expected_type=bool)
    return ElectricalState(power=0.0,
                           efficiency=0.0,
                           delivering=False,
                           receiving=False,
                           on=on)

def zero_energy_state(energy: float=0.0) -> EnergyState:
    """
    Returns an initial energy state with values set at zero.
    """
    assert_type_and_range(energy,
                          more_than=0.0)
    return EnergyState(energy=0.0,
                       power=0.0,
                       efficiency=0.0,
                       delivering=False,
                       receiving=False)
