"""This module contains definitions for energy conversion modules."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal, Optional
from uuid import uuid4
from components.dynamic_response import ForwardDynamicResponse, BidirectionalDynamicResponse
from components.fuel_type import LiquidFuel, GaseousFuel
from components.port import Port, PortInput, PortOutput, \
    PortBidirectional, PortType, PortDirection
from components.state import IOState, FullStateWithInput, InternalState, \
    LiquidFuelIOState, GaseousFuelIOState, ElectricIOState, RotatingIOState
from helpers.functions import assert_type, assert_type_and_range, assert_callable
from helpers.types import ElectricSignalType, PowerType


@dataclass
class Converter():
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
    state: FullStateWithInput=field(init=False)
    power_func: Callable[[IOState, InternalState], float]
    efficiency_func: Callable[[IOState, InternalState], float]
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
        assert PortDirection.BIDIRECTIONAL not in (self.input.direction, self.output.direction) and \
            self.input.direction!=self.output.direction or \
            self.input.direction==PortDirection.BIDIRECTIONAL==self.output.direction
        assert_callable(self.power_func)
        assert_callable(self.efficiency_func)
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
        Dynamically calculates the power at the input, if applicable.
        """
        return self.state.input.power

    @property
    def output_power(self) -> float:
        """
        Dynamically calculates the power at the output.
        """
        return self.state.output.power

    def _compute_conversion(self, delta_t: float,
                            state: Optional[IOState]=None,
                            reverse: bool=False) -> Optional[IOState]:
        """
        Returns the result of a conversion or recovery.
        """
        if reverse and not self.reversible:
            return None
        if state is None:
            state = self.state.input if not reverse else self.state.output
        assert self.state.internal is not None
        if not reverse:
            return self.dynamic_response.forward_response(state, self.state.internal, delta_t)
        assert isinstance(self.dynamic_response, BidirectionalDynamicResponse)
        return self.dynamic_response.reverse_response(state, self.state.internal, delta_t)

    def convert(self, delta_t: float,
                state: Optional[IOState]=None,
                update_state: bool=True) -> Optional[IOState]:
        """
        Calculates the forward conversion.
        """
        if state is None:
            state = self.state.input
        conv = self._compute_conversion(delta_t=delta_t,
                                        state=state,
                                        reverse=False)
        if not update_state:
            return conv
        if conv is not None:
            self.update_io_state(new_state=conv,
                                 which="out")
        return None

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
class ReversibleConverter(Converter):
    """
    Base class for reversible converters.
    """
    def __init__(self, name: str,
                 mass: float,
                 input_port: PortBidirectional,
                 output_port: PortBidirectional,
                 power_func: Callable[[IOState, InternalState], float],
                 efficiency_func: Callable[[IOState, InternalState], float],
                 dynamic_response: BidirectionalDynamicResponse):
        super().__init__(name=name,
                         mass=mass,
                         input=input_port,
                         output=output_port,
                         power_func=power_func,
                         efficiency_func=efficiency_func,
                         dynamic_response=dynamic_response)

    @property
    def reversible(self) -> bool:
        return True

    def recover(self, delta_t: float,
                state: Optional[IOState]=None,
                update_state: bool=True) -> Optional[IOState]:
        """
        Calculates the reverse conversion.
        """
        if state is None:
            state = self.state.output
        conv = self._compute_conversion(delta_t=delta_t,
                                        state=state,
                                        reverse=True)
        if not update_state:
            return conv
        if conv is not None:
            self.update_io_state(new_state=conv,
                                 which="in")
        return None


@dataclass
class ForwardConverter(Converter):
    """
    Base class for non-reversible converters.
    """
    def __init__(self, name: str,
                 mass: float,
                 input_port: PortInput,
                 output_port: PortOutput,
                 power_func: Callable[[IOState, InternalState], float],
                 efficiency_func: Callable[[IOState, InternalState], float],
                 dynamic_response: ForwardDynamicResponse):
        super().__init__(name=name,
                         mass=mass,
                         input=input_port,
                         output=output_port,
                         power_func=power_func,
                         efficiency_func=efficiency_func,
                         dynamic_response=dynamic_response)

    @property
    def reversible(self) -> bool:
        return False


@dataclass
class MechanicalConverter():
    """
    Models a mechanical converter, which involves movement.
    Adds inertia to the `Converter` base class.
    """
    inertia: float

    def __post_init__(self):
        assert_type_and_range(self.inertia,
                              more_than=0.0)


@dataclass
class ForwardVoltageConverter(ForwardConverter):
    """
    Models a non-reversible electrical converter.
    """
    nominal_voltage_in: float
    nominal_voltage_out: float

    def __init__(self,
                 name: str,
                 mass: float,
                 efficiency_func: Callable[[IOState, InternalState], float],
                 power_func: Callable[[IOState, InternalState], float],
                 dynamic_response: ForwardDynamicResponse,
                 in_type: ElectricSignalType,
                 out_type: ElectricSignalType,
                 nominal_voltage_in: float,
                 nominal_voltage_out: float):
        assert_type(in_type, out_type,
                    expected_type=ElectricSignalType)
        assert_type_and_range(nominal_voltage_in, nominal_voltage_out,
                              more_than=0.0,
                              include_more=False)
        super().__init__(name=name,
                         mass=mass,
                         input_port=PortInput(exchange=PowerType.ELECTRIC_AC
                                              if in_type==ElectricSignalType.AC
                                              else PowerType.ELECTRIC_DC),
                         output_port=PortOutput(exchange=PowerType.ELECTRIC_AC
                                                if out_type==ElectricSignalType.AC
                                                else PowerType.ELECTRIC_DC),
                         power_func=power_func,
                         efficiency_func=efficiency_func,
                         dynamic_response=dynamic_response)
        self.nominal_voltage_in = nominal_voltage_in
        self.nominal_voltage_out = nominal_voltage_out

    @property
    def in_type(self) -> ElectricSignalType:
        """
        Returns the type of input electric signal.
        """
        return (ElectricSignalType.AC
                if self.input.exchange == PowerType.ELECTRIC_AC
                else ElectricSignalType.DC)

    @property
    def out_type(self) -> ElectricSignalType:
        """
        Returns the type of output electric signal.
        """
        return (ElectricSignalType.AC
                if self.output.exchange==PowerType.ELECTRIC_AC
                else ElectricSignalType.DC)


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
