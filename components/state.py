"""This module defines the internal states of the components."""

from dataclasses import dataclass, field
from typing import Any, Optional
from helpers.functions import assert_type, assert_type_and_range
from simulation.constants import RPM_TO_ANG_VEL

@dataclass
class State():
    """
    Base class for the internal states during simulation.
    """
    delivering: bool
    receiving: bool

    def __post_init__(self):
        assert_type(self.delivering, self.receiving,
                    expected_type=bool)

    def as_dict(self) -> dict[str, Any]:
        """
        Serializes the state into a dictionary.
        """
        return self.__dict__


@dataclass
class EnergySourceState(State):
    """
    The internal state of a battery or fuel tank.
    """
    energy: float
    power: float

    def __post_init__(self):
        super().__post_init__()
        assert_type_and_range(self.energy, self.power,
                              more_than=0.0)


@dataclass
class MotorState(State):
    """
    The internal state of a motor or engine.
    """
    power: float
    rpm: float
    torque: float = field(init=False)
    efficiency: float
    on: bool

    def __post_init__(self):
        super().__post_init__()
        assert_type_and_range(self.power, self.rpm,
                              more_than=0.0)
        assert_type_and_range(self.efficiency,
                              more_than=0.0,
                              less_than=1.0)
        assert_type(self.on,
                    expected_type=bool)
        self.torque = self.power / self.rpm / RPM_TO_ANG_VEL if self.rpm > 0.0 else 0.0


@dataclass
class FuelCellState(State):
    """
    The internal state of a fuel cell.
    """
    power: float
    efficiency: float
    on: bool

    def __post_init__(self):
        super().__post_init__()
        assert_type_and_range(self.power,
                              more_than=0.0)
        assert_type_and_range(self.efficiency,
                              more_than=0.0,
                              less_than=1.0)
        assert_type(self.on,
                    expected_type=bool)
