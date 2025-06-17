"""
This module contains definitions for creating a complete vehicle
for the simulation.
"""

from dataclasses import dataclass
from components.body import Body
from components.brake import Brake
from components.drive_train import DriveTrain
from components.ecu import ECU
from components.energy_source import EnergySource
from components.power_converter import PowerConverter


@dataclass
class Vehicle():
    """
    Combines all vehicle components into a comprehensive model.
    """
    energy_sources: list[EnergySource]
    power_converters: list[PowerConverter]
    body: Body
    brake: Brake
    drive_train: DriveTrain
    ecu: ECU
