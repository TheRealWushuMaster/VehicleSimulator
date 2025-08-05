"""This module contains definitions for energy conversion modules."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal, Optional
from uuid import uuid4
from components.port import Port, PortInput, PortOutput, PortBidirectional, PortType, PortDirection
from components.state import State, ElectricIOState
from helpers.functions import assert_type, assert_numeric, \
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
    state: State=field(init=False)
    control_signal: float
    max_power: float
    power_func: Callable[[State], float]
    efficiency_func: Callable[[State], float]
    dynamic_response: Callable[[State, float, float], State] # Depends on the state, control signal, and delta time
    reverse_dynamic_response: Optional[Callable[[State, float, float], State]]
    reverse_efficiency: Optional[float]

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
        assert_type_and_range(self.mass, self.max_power,
                              more_than=0.0)
        assert_type_and_range(self.reverse_efficiency,
                              more_than=0.0,
                              less_than=1.0,
                              allow_none=True)
        assert_callable(self.efficiency_func)
        self.mass = max(self.mass, 0.0)
        self.id = f"Converter-{uuid4()}"
        assert_numeric(self.control_signal)

    @property
    def efficiency(self) -> float:
        """Returns the efficiency value at the current state."""
        return self.efficiency_func(self.state)

    @property
    def reversible(self) -> bool:
        """
        Returns if the converter is reversible.
        """
        return self.reverse_dynamic_response is not None

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
                            state: Optional[State]=None,
                            reverse: bool=False) -> Optional[State]:
        """
        Returns the result of a conversion or recovery.
        """
        if reverse and not self.reversible:
            return None
        if state is None:
            state = self.state
        if not reverse:
            return self.dynamic_response(state, self.control_signal, delta_t)
        assert self.reverse_dynamic_response is not None
        return self.reverse_dynamic_response(state, self.control_signal, delta_t)

    def convert(self, state: Optional[State],
                delta_t: float,
                update_state: bool=True) -> Optional[State]:
        """
        Calculates the conversion.
        """
        conv = self._compute_conversion(delta_t=delta_t,
                                        state=state,
                                        reverse=False)
        if not update_state:
            return conv
        if conv is not None:
            self.update_state(state=conv)
        return None

    def recover(self, state: Optional[State],
                delta_t: float) -> Optional[State]:
        """Calculates the reverse delivery, if applicable."""
        return self._compute_conversion(delta_t=delta_t,
                                        state=state,
                                        reverse=True)

    def update_state(self, state: State,
                     which: Literal["in", "out"]="out") -> None:
        """
        Updates the internal state of the converter.
        """
        assert which in ("in", "out")
        assert_type(state,
                    expected_type=State)
        if which=="out":
            self.state.output = state.output
        elif self.reversible:
            self.state.input = state.input

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
