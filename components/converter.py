"""This module contains definitions for energy conversion modules."""

from abc import ABC
from dataclasses import dataclass, field
from typing import Literal, Optional
from uuid import uuid4
from components.consumption import ConverterConsumption
from components.dynamic_response import BaseDynamicResponse
from components.fuel_type import LiquidFuel, GaseousFuel
from components.limitation import ConverterLimits
from components.port import Port, PortInput, PortOutput, \
    PortBidirectional, PortType, PortDirection
from components.state import IOState, FullStateWithInput, \
    LiquidFuelIOState, GaseousFuelIOState, ElectricIOState, RotatingIOState
from helpers.functions import assert_type, assert_type_and_range
from helpers.types import ElectricSignalType, PowerType


@dataclass
class Converter(ABC):
    """
    Base class for modules that convert energy between types.
    Includes engines, motors, and fuel cells.
    
    Attributes:
        - `id` (str): identifier for the object
        - `name` (str): a name for the power converter
        - `mass` (float): the mass of the converter
        - `input` (Port type): input port to convert from
        - `output` (Port type): output port converting to
        - `state` (State): the converter's full state
        - `control_signal` (float): the value of control signal
        - `max_power` (float): the maximum power it can handle (W)
        - `power_func` (State -> float): the function determining
                the maximum power at the converter's state
        - `efficiency_func` (State -> float): accounts for power
                losses [0.0-1.0]
        - `reverse_efficiency` (float or None): allows to convert
                power [0.0-1.0] in reverse if the value is not None
    """
    id: str=field(init=False)
    name: str
    mass: float
    input: PortInput|PortBidirectional
    output: PortOutput|PortBidirectional
    state: FullStateWithInput
    limits: ConverterLimits
    consumption: ConverterConsumption
    dynamic_response: BaseDynamicResponse

    def __post_init__(self):
        assert_type(self.name,
                    expected_type=str)
        assert_type(self.input,
                    expected_type=(PortInput, PortBidirectional))
        assert_type(self.output,
                    expected_type=(PortOutput, PortBidirectional))
        assert_type_and_range(self.mass,
                              more_than=0.0)
        assert_type(self.limits,
                    expected_type=ConverterLimits)
        assert_type(self.consumption,
                    expected_type=ConverterConsumption)
        assert PortDirection.BIDIRECTIONAL not in (self.input.direction,
                                                   self.output.direction) and \
            self.input.direction!=self.output.direction or \
            self.input.direction==PortDirection.BIDIRECTIONAL==self.output.direction
        assert_type(self.dynamic_response,
                    expected_type=BaseDynamicResponse)
        self.id = f"Converter-{uuid4()}"

    @property
    def efficiency(self) -> float:
        """Returns the efficiency value at the current state."""
        return self.state.efficiency

    @property
    def reversible(self) -> bool:
        """
        Returns if the converter is reversible.
        """
        raise NotImplementedError

    @property
    def input_power(self) -> float:
        """
        Returns the power at the input.
        """
        return self.state.input.power

    @property
    def output_power(self) -> float:
        """
        Returns the power at the output.
        """
        return self.state.output.power

    def update_io_state(self, new_state: IOState,
                     which: Literal["in", "out"]="out") -> None:
        """
        Updates the internal state of the converter.
        """
        assert which in ("in", "out")
        assert_type(new_state,
                    expected_type=IOState)
        if which=="out":
            self.state.output = new_state
        elif self.reversible:
            self.state.input = new_state

    def return_port(self, which: PortType) -> Port:
        """
        Returns the requested Port object.
        """
        assert_type(which,
                    expected_type=PortType)
        if which==PortType.INPUT_PORT:
            return self.input
        return self.output

    def return_which_port(self, port: PortInput|PortOutput|PortBidirectional) -> Optional[PortType]:
        """
        Returns whether the port is the converter's input or output port.
        """
        if self.input == port:
            return PortType.INPUT_PORT
        if self.output == port:
            return PortType.OUTPUT_PORT
        return None


@dataclass
class MechanicalConverter(Converter):
    """
    Models a mechanical converter, which involves movement.
    Adds inertia to the `Converter` base class.
    """
    inertia: float

    def __post_init__(self):
        super().__post_init__()
        assert_type_and_range(self.inertia,
                              more_than=0.0)

    @property
    def reversible(self) -> bool:
        """
        Returns if the converter is reversible.
        """
        raise NotImplementedError


def return_io_state(port: Port) -> IOState:
    """
    Returns the `IOState` for a type of port.
    """
    if isinstance(port.exchange, LiquidFuel):
        return LiquidFuelIOState(fuel=port.exchange)
    if isinstance(port.exchange, GaseousFuel):
        return GaseousFuelIOState(fuel=port.exchange)
    if port.exchange==PowerType.ELECTRIC_AC:
        return ElectricIOState(signal_type=ElectricSignalType.AC)
    if port.exchange==PowerType.ELECTRIC_DC:
        return ElectricIOState(signal_type=ElectricSignalType.DC)
    if port.exchange==PowerType.MECHANICAL:
        return RotatingIOState()
    raise ValueError
