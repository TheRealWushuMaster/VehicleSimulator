"""This module contains definitions for energy conversion modules."""

from dataclasses import dataclass
from typing import Optional
from components.fuel_type import Fuel
from helpers.functions import clamp, assert_type
from helpers.types import PowerType, ConversionResult
from simulation.constants import EPSILON


@dataclass
class Converter():
    """
    Base class for modules that convert energy between types.
    Includes engines, motors, and fuel cells.
    
    Attributes:
        - name (str): a name for the power converter
        - input (PowerType or Fuel): the input to convert from
        - output (PowerType or Fuel): the output to convert to
        - max_power (float): the maximum power it can handle (W)
        - efficiency (float): accounts for power losses [0.0-1.0]
        - reverse_efficiency (float or None): allows to convert
                power [0.0-1.0] in reverse if the value is not None
    """
    name: str
    mass: float
    input: PowerType|Fuel
    output: PowerType|Fuel
    max_power: float
    efficiency: float
    reverse_efficiency: Optional[float]

    def __post_init__(self):
        assert_type(self.name,
                    expected_type=str)
        assert_type(self.input, self.output,
                    expected_type=(PowerType, Fuel))
        assert_type(self.mass, self.max_power, self.efficiency,
                    expected_type=float)
        assert_type(self.reverse_efficiency,
                    expected_type=float,
                    allow_none=True)
        self.mass = max(self.mass, 0.0)
        self.efficiency = clamp(val=self.efficiency,
                                min_val=EPSILON,
                                max_val=1.0)
        if self.reverse_efficiency:
            self.reverse_efficiency = clamp(val=self.reverse_efficiency,
                                            min_val=0.0,
                                            max_val=1.0)
        self.max_power = max(self.max_power, 0.0)

    def _compute_conversion(self, input_power: float, delta_t: float,
                           reverse: bool) -> ConversionResult:
        """Calculates a power conversion result."""
        input_power = abs(input_power)
        if reverse:
            if self.reverse_efficiency:
                eff = self.reverse_efficiency
            else:
                eff = 0.0
        else:
            eff = self.efficiency
        output_power = clamp(val=input_power*eff,
                             min_val=0.0,
                             max_val=self.max_power)
        power_loss = input_power - output_power
        return ConversionResult(input_power=input_power,
                                output_power=output_power,
                                power_loss=power_loss,
                                energy_input=input_power*delta_t,
                                energy_output=output_power*delta_t,
                                energy_loss=power_loss*delta_t)

    def convert_power(self, input_power: float,
                      delta_t: float) -> ConversionResult:
        """Calculates the power delivered."""
        return self._compute_conversion(input_power=input_power,
                                        delta_t=delta_t,
                                        reverse=False)

    def recover_power(self, input_power: float,
                      delta_t: float) -> ConversionResult:
        """Calculates the reverse power delivered, if applicable."""
        return self._compute_conversion(input_power=input_power,
                                        delta_t=delta_t,
                                        reverse=True)
