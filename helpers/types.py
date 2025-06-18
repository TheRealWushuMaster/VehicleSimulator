"""
Contains various types for use in the simulation.
"""

from dataclasses import dataclass, field
from enum import Enum
from helpers.functions import assert_type_and_range
from simulation.constants import RPM_TO_ANG_VEL

class PowerType(Enum):
    """
    A comprehensive list of types of power useable in the vehicle.
    Usable both for input and output of each block.
    """
    CHEMICAL   = "CHEMICAL"
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


@dataclass(frozen=True)
class MotorOperationPoint():
    """
    Represents the operation of a motor or engine at a specific
    combination of power and RPM.
    """
    power: float
    rpm: float
    torque: float = field(init=False)

    def __post_init__(self):
        assert_type_and_range(self.power, self.rpm,
                              more_than=0.0)
        torque = self.power / self.rpm / RPM_TO_ANG_VEL if self.rpm > 0.0 else 0.0
        object.__setattr__(self, 'torque', torque)
