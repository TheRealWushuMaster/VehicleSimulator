"""
This module implements a simulator that resolve the state of each
component of a vehicle at each time step.
"""

from dataclasses import dataclass
from components.vehicle import Vehicle


@dataclass
class Simulator():
    vehicle: Vehicle
