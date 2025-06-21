"""This module defines input and ouput ports for the components to interact."""

from enum import Enum
from dataclasses import dataclass
from components.fuel_type import Fuel
from helpers.functions import assert_type
from helpers.types import PowerType


class PortDirection(Enum):
    INPUT         = "INPUT"
    OUTPUT        = "OUTPUT"
    BIDIRECTIONAL = "BIDIRECTIONAL"


class PortType(Enum):
    INPUT_PORT  = "INPUT_PORT"
    OUTPUT_PORT = "OUTPUT_PORT"


@dataclass
class Port():
    """
    Defines a port for a component to interface with other components.
    """
    direction: PortDirection
    exchange: PowerType|Fuel

    def __post_init__(self):
        assert_type(self.direction,
                    expected_type=PortDirection)
        assert_type(self.exchange,
                    expected_type=(PowerType, Fuel))

    def is_compatible_with(self, other: "Port") -> bool:
        if self.exchange!=other.exchange:
            return False
        if PortDirection.BIDIRECTIONAL in (self.direction, other.direction):
            return True
        return self.direction != other.direction


@dataclass
class PortInput(Port):
    """
    Defines an input port.
    """
    def __init__(self, exchange: PowerType|Fuel) -> None:
        super().__init__(direction=PortDirection.INPUT,
                         exchange=exchange)


@dataclass
class PortOutput(Port):
    """
    Defines an output port.
    """
    def __init__(self, exchange: PowerType | Fuel) -> None:
        super().__init__(direction=PortDirection.OUTPUT,
                         exchange=exchange)


@dataclass
class PortBidirectional(Port):
    """
    Defines a bidirectional port.
    """
    def __init__(self, exchange: PowerType | Fuel) -> None:
        super().__init__(direction=PortDirection.BIDIRECTIONAL,
                         exchange=exchange)
