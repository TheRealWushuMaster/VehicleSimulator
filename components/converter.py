"""This module contains definitions for energy conversion modules."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal, Optional
from uuid import uuid4
from components.dynamic_response import ForwardDynamicResponse, BidirectionalDynamicResponse
from components.port import Port, PortInput, PortOutput, PortBidirectional, PortType, PortDirection
from components.state import IOState, ElectricIOState, FuelIOState, FullStateWithInput, InternalState
from helpers.functions import assert_type, \
    assert_type_and_range, assert_callable, electric_power
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
        assert PortDirection.BIDIRECTIONAL not in (self.input.direction, self.output.direction) and \
            self.input.direction!=self.output.direction or \
            self.input.direction==PortDirection.BIDIRECTIONAL==self.output.direction
        assert_callable(self.power_func)
        assert_callable(self.efficiency_func)
        assert_type(self.dynamic_response,
                    expected_type=(ForwardDynamicResponse, BidirectionalDynamicResponse))
        self.mass = max(self.mass, 0.0)
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
    def power_at_input(self) -> float:
        """
        Dynamically calculates the power at the input, if applicable.
        """
        raise NotImplementedError

    @property
    def power_at_output(self) -> float:
        """
        Dynamically calculates the power at the output.
        """
        raise NotImplementedError

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


@dataclass
class PureElectricConverter(Converter):
    """
    Models a purely electrical converter.
    """
    in_type: ElectricSignalType
    out_type: ElectricSignalType
    nominal_voltage_in: float=field(init=False)
    nominal_voltage_out: float=field(init=False)
    nominal_current_in: float=field(init=False)
    nominal_current_out: float=field(init=False)

    def __init__(self,
                 name: str,
                 mass: float,
                 max_power: float,
                 eff_func: Callable[[State], float],
                 reverse_efficiency: float,
                 power_func: Callable[[State], float],
                 reversible: bool,
                 in_type: ElectricSignalType,
                 out_type: ElectricSignalType,
                 nominal_voltage_in: Optional[float]=None,
                 nominal_voltage_out: Optional[float]=None,
                 nominal_current_in: Optional[float]=None,
                 nominal_current_out: Optional[float]=None):
        assert_type(in_type, out_type,
                    expected_type=ElectricSignalType)
        assert_type_and_range(nominal_voltage_in, nominal_voltage_out,
                              nominal_current_in, nominal_current_out,
                              more_than=0.0,
                              include_more=False,
                              allow_none=True)
        input_port: PortInput|PortBidirectional
        output_port: PortOutput|PortBidirectional
        if reversible:
            input_port = PortBidirectional(exchange=PowerType.ELECTRIC)
            output_port = PortBidirectional(exchange=PowerType.ELECTRIC)
        else:
            input_port = PortInput(exchange=PowerType.ELECTRIC)
            output_port = PortOutput(exchange=PowerType.ELECTRIC)
        super().__init__(name=name,
                         mass=mass,
                         input=input_port,
                         output=output_port,
                         control_signal=344,
                         max_power=max_power,
                         power_func=power_func,
                         efficiency_func=eff_func,
                         dynamic_response=dyn_resp,
                         reverse_dynamic_response=rev_dyn_resp,
                         reverse_efficiency=234)
        self.in_type = in_type
        self.out_type = out_type
        volt = nominal_voltage_in is not None and nominal_voltage_out is not None
        curr = nominal_current_in is not None and nominal_current_out is not None
        assert volt and not curr or curr and not volt
        if volt:
            assert nominal_voltage_in is not None and nominal_voltage_out is not None
            self.nominal_voltage_in = nominal_voltage_in
            self.nominal_voltage_out = nominal_voltage_out
        else:
            assert nominal_current_in is not None and nominal_current_out is not None
            self.nominal_current_in = nominal_current_in
            self.nominal_current_out = nominal_current_out

    @property
    def power_at_input(self) -> float:
        assert isinstance(self.state.input, ElectricIOState)
        return electric_power(voltage=self.state.input.voltage,
                              current=self.state.input.current)

    @property
    def power_at_output(self) -> float:
        assert isinstance(self.state.output, ElectricIOState)
        return electric_power(voltage=self.state.output.voltage,
                              current=self.state.output.current)
