"""This module contains definitions for energy conversion modules."""

from dataclasses import dataclass, field
from typing import Literal, Generic, TypeVar
from uuid import uuid4
from components.consumption import ConverterConsumption
from components.dynamic_response import ForwardDynamicResponse, BidirectionalDynamicResponse
from components.fuel_type import LiquidFuel, GaseousFuel
from components.limitation import ConverterLimits
from components.port import Port, PortInput, PortOutput, \
    PortBidirectional, PortType, PortDirection
from components.state import IOState, FullStateWithInput, \
    LiquidFuelIOState, GaseousFuelIOState, ElectricIOState, RotatingIOState
from helpers.functions import assert_type, assert_type_and_range
from helpers.types import ElectricSignalType, PowerType

state_type = TypeVar('StateType', bound=FullStateWithInput)

@dataclass
class Converter(Generic[state_type]):
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
    state: state_type  #FullStateWithInput=field(init=False)
    limits: ConverterLimits
    consumption: ConverterConsumption
    dynamic_response: ForwardDynamicResponse|BidirectionalDynamicResponse

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
                    expected_type=(ForwardDynamicResponse, BidirectionalDynamicResponse))
        self.id = f"Converter-{uuid4()}"
        self.state = default_full_state(obj=self)

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


@dataclass
class MechanicalConverter(GenericConverter):
    """
    Models a mechanical converter, which involves movement.
    Adds inertia to the `Converter` base class.
    """
    inertia: float

    def __post_init__(self):
        assert_type_and_range(self.inertia,
                              more_than=0.0)

    @property
    def reversible(self) -> bool:
        """
        Returns if the converter is reversible.
        """
        raise NotImplementedError


def default_full_state(obj: Converter) -> FullStateWithInput:
    """
    Returns a default full state for the `Converter` class.
    """
    input_state = return_io_state(port=obj.input)
    output_state = return_io_state(port=obj.output)
    return FullStateWithInput(input=input_state,
                              output=output_state,
                              internal=None)

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
