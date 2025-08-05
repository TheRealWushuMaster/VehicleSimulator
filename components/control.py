"""This module contains class definitions for controlling
classes for drivable components."""

from abc import ABC
from typing import Optional
from dataclasses import dataclass
from helpers.functions import assert_type, assert_type_and_range


@dataclass
class ControlBase(ABC):
    """
    Base class for controller objects.
    """
    _throttle: float
    _brake: Optional[float]
    reversible: bool

    def __init__(self, reversible: bool,
                 can_brake: bool) -> None:
        assert_type(reversible, can_brake,
                    expected_type=bool)
        self._throttle: float = 0.0
        self._brake: Optional[float] = 0.0 if can_brake else None
        self.reversible = reversible

    def __post_init__(self):
        assert_type_and_range(self._throttle,
                              more_than=0.0,
                              less_than=1.0)
        assert_type_and_range(self._brake,
                              more_than=0.0,
                              less_than=1.0,
                              allow_none=True)

    def set_throttle(self, value: float, delta_t: float) -> None:
        """
        Sets the throttle value and
        triggers a resource request.
        """
        assert_type_and_range(value,
                              more_than=-1.0 if self.reversible else 0.0,
                              less_than=1.0)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        self._throttle = value
        self.request_input(delta_t=delta_t)

    def set_brake(self, value: float) -> None:
        """
        Sets the brake value, if applicable.
        """
        if self._brake is not None:
            assert_type_and_range(value,
                                  more_than=0.0,
                                  less_than=1.0)
            self._brake = value

    def request_input(self, delta_t: float) -> None:
        """
        Requests required input for a throttle
        value and a provided delta_t time step.
        """
        raise NotImplementedError


@dataclass
class VoltageDriver(ControlBase):
    """
    Driver for voltage-controlled components.
    """
    max_voltage: float

    def __post_init__(self):
        super().__post_init__()
        assert_type_and_range(self.max_voltage,
                              more_than=0.0)

    def request_input(self, delta_t: float) -> None:
        return super().request_input(delta_t)