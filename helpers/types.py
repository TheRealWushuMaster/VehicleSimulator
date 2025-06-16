"""
Contains various types for use in the simulation.
"""

from dataclasses import dataclass
from enum import Enum

class PowerType(Enum):
    """
    A comprehensive list of types of power useable in the vehicle.
    Usable both for input and output of each block.
    """
    CHEMICAL  = "CHEMICAL"
    ELECTRIC   = "ELECTRIC"
    MECHANICAL = "MECHANICAL"


class StateOfMatter(Enum):
    """
    The list of the states of matter.
    """
    SOLID   = "SOLID"
    LIQUID  = "LIQUID"
    GASEOUS = "GASEOUS"
    PLASMA  = "PLASMA"


@dataclass(frozen=True)
class ConversionResult():
    """Stores the results of energy conversions."""
    input_power: float
    output_power: float
    power_loss: float
    energy_input: float
    energy_output: float
    energy_loss: float
