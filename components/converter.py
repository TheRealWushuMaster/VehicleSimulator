"""This module contains definitions for energy conversion modules."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4
from components.port import Port, PortInput, PortOutput, PortBidirectional, PortType
from components.state import MechanicalState, ElectricalState, FuelState
from helpers.functions import clamp, assert_type, assert_numeric
from helpers.types import ConversionResult


@dataclass
class Converter():
    """
    Base class for modules that convert energy between types.
    Includes engines, motors, and fuel cells.
    
    Attributes:
        - id (str): identifier for the object
        - name (str): a name for the power converter
        - mass (float): the mass of the converter
        - input (Port type): input port to convert from
        - output (Port type): output port converting to
        - max_power (float): the maximum power it can handle (W)
        - efficiency (float): accounts for power losses [0.0-1.0]
        - reverse_efficiency (float or None): allows to convert
                power [0.0-1.0] in reverse if the value is not None
    """
    id: str=field(init=False)
    name: str
    mass: float
    input: PortInput|PortBidirectional
    output: PortOutput|PortBidirectional
    input_state: ElectricalState|MechanicalState|FuelState
    output_state: ElectricalState|MechanicalState
    control_signal: Optional[float]
    #internal_state: MechanicalState|ElectricalState
    max_power: float
    power_func: Callable[[MechanicalState|ElectricalState], float]
    efficiency_func: Callable[[MechanicalState|ElectricalState], float]
    reverse_efficiency: Optional[float]

    def __post_init__(self):
        assert_type(self.name,
                    expected_type=str)
        assert_type(self.input,
                    expected_type=(PortInput, PortBidirectional))
        assert_type(self.output,
                    expected_type=(PortOutput, PortBidirectional))
        assert_numeric(self.mass, self.max_power)
        assert_type(self.reverse_efficiency,
                    expected_type=float,
                    allow_none=True)
        assert_type(self.efficiency_func,
                    expected_type=Callable)  # type: ignore[arg-type]
        self.mass = max(self.mass, 0.0)
        if self.reverse_efficiency:
            self.reverse_efficiency = clamp(val=self.reverse_efficiency,
                                            min_val=0.0,
                                            max_val=1.0)
        self.max_power = max(self.max_power, 0.0)
        self.id = f"Converter-{uuid4()}"
        assert_numeric(self.control_signal,
                       allow_none=True)

    @property
    def efficiency(self) -> float:
        """Returns the efficiency value at the current state."""
        return self.efficiency_func(self.state)

    def _compute_conversion(self, input_magnitude: float, delta_t: float,
                           reverse: bool) -> ConversionResult:
        """Calculates a power conversion result."""
        input_power = abs(input_magnitude)
        if reverse:
            if self.reverse_efficiency:
                eff = self.reverse_efficiency
            else:
                eff = 0.0
        else:
            eff = self.efficiency
        output_power = clamp(val=input_magnitude*eff,
                             min_val=0.0,
                             max_val=self.max_power)
        power_loss = input_power - output_power
        return ConversionResult(input_power=input_power,
                                output_power=output_power,
                                power_loss=power_loss,
                                energy_input=input_power*delta_t,
                                energy_output=output_power*delta_t,
                                energy_loss=power_loss*delta_t)

    def convert(self, input_magnitude: float,
                delta_t: float) -> ConversionResult:
        """Calculates the conversion."""
        return self._compute_conversion(input_magnitude=input_magnitude,
                                        delta_t=delta_t,
                                        reverse=False)

    def recover(self, input_magnitude: float,
                delta_t: float) -> ConversionResult:
        """Calculates the reverse delivery, if applicable."""
        return self._compute_conversion(input_magnitude=input_magnitude,
                                        delta_t=delta_t,
                                        reverse=True)

    def return_port(self, which: PortType) -> Port:
        """
        Returns the requested Port object.
        """
        assert_type(which,
                    expected_type=PortType)
        if which==PortType.INPUT_PORT:
            return self.input
        return self.output
