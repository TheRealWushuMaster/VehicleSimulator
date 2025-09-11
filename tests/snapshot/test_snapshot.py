"""This module contains test routines for the component snapshot classes."""

from components.component_snapshot import ElectricMotorSnapshot, ElectricGeneratorSnapshot, \
    LiquidCombustionEngineSnapshot, GaseousCombustionEngineSnapshot, FuelCellSnapshot, \
    ElectricInverterSnapshot, ElectricRectifierSnapshot, GearBoxSnapshot


electric_power_in: float = 10_000.0
electric_power_out: float = 9_100.0
torque_in: float = 20.0
rpm_in: float = 1_200.0
torque_out: float = 15.0
rpm_out: float = 1_100.0

def create_electric_motor_snapshot() -> ElectricMotorSnapshot:
    return ElectricMotorSnapshot(io)