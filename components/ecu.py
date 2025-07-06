"""
This module contains definitions for different types of ECUs.
"""

from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from components.vehicle import Vehicle

@dataclass
class ECU():
    """
    This class simulates the operation of
    a vehicle's Electronic Control Unit.
    """
    vehicle: Optional["Vehicle"]=field(default=None)


@dataclass
class ElectricECU(ECU):
    ...


@dataclass
class HybridECU(ECU):
    ...


@dataclass
class PluginHybridECU(ECU):
    ...
