"""
Contains the types of power that power sources and motors can use.
"""

from enum import Enum

class PowerType(Enum):
    """
    A comprehensive list of types of power useable in the vehicle.
    Usable both for input and output of each block.
    """
    THERMAL = "THERMAL"
    ELECTRIC = "ELECTRIC"
    MECHANICAL = "MECHANICAL"
