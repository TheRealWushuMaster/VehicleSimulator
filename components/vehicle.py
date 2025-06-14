"""
This module contains definitions for creating a complete vehicle
for the simulation.
"""

from dataclasses import dataclass
from typing import Optional
from components.battery import Battery
from components.body import Body
from components.brake import DiskBrake, DrumBrake
from components.drive_train import DriveTrain
from components.ecu import ElectricECU, HybridECU, PluginHybridECU
from components.fuel_cell import HydrogenFuelCell
from components.motor import ElectricMotor, InternalCombustionEngine


@dataclass
class Vehicle():
    """
    Combines all vehicle components into a comprehensive model.
    """
    battery: Optional[Battery]
    body: Body
    brake: DiskBrake|DrumBrake
    drive_train: DriveTrain
    ecu: ElectricECU|HybridECU|PluginHybridECU
    fuel_cell: Optional[HydrogenFuelCell]
    fuel_type: Optional[float]
    motor: list[ElectricMotor|InternalCombustionEngine]
