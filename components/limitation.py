"""
This module contains routines for handling
components' state limitations.
"""

from collections.abc import Callable
from dataclasses import dataclass
from components.state import FullStateNoInput, FullStateWithInput
from helpers.functions import assert_type, assert_numeric, \
    assert_callable, assert_range


# =================
# VALUE LIMITATIONS
# =================


@dataclass
class AbsoluteLimitValue():
    """
    Contains absolute limit values.
    """
    max: float
    min: float=0.0

    def __post_init__(self):
        assert_numeric(self.max, self.min)
        assert_range(self.max,
                     more_than=self.min,
                     include_more=False)


@dataclass
class RelativeLimitValue():
    """
    Contains absolute limit values.
    The value of `max` must always be greater
    than `min`, for all input states.
    """
    max: Callable[[FullStateNoInput|FullStateWithInput], float]
    min: Callable[[FullStateNoInput|FullStateWithInput], float]=lambda s: 0.0

    def __post_init__(self):
        assert_callable(self.max, self.min)


# ====================
# INTERNAL LIMITATIONS
# ====================


@dataclass
class AbsoluteInternalLimitations():
    """
    Contains the absolute internal variables subject to limitations.
    """
    temperature: AbsoluteLimitValue

    def __post_init__(self):
        assert_type(self.temperature,
                    expected_type=AbsoluteLimitValue)


@dataclass
class RelativeInternalLimitations():
    """
    Contains the relative internal variables subject to limitations.
    """
    temperature: RelativeLimitValue

    def __post_init__(self):
        assert_type(self.temperature,
                    expected_type=RelativeLimitValue)


# ===============================================
# DOMAIN LIMITATIONS (ELECTRIC, MECHANICAL, FUEL)
# ===============================================


@dataclass
class AbsoluteElectricLimitations():
    """
    Contains the electric variables subject to limitations.
    """
    voltage: AbsoluteLimitValue
    current: AbsoluteLimitValue

    def __post_init__(self):
        assert_type(self.voltage, self.current,
                    expected_type=AbsoluteLimitValue)


@dataclass
class RelativeElectricLimitations():
    """
    Contains the electric variables subject to limitations.
    """
    voltage: RelativeLimitValue
    current: RelativeLimitValue

    def __post_init__(self):
        assert_type(self.voltage, self.current,
                    expected_type=RelativeLimitValue)


@dataclass
class AbsoluteMechanicalLimitations():
    """
    Contains the electric variables subject to limitations.
    """
    torque: AbsoluteLimitValue
    rpm: AbsoluteLimitValue

    def __post_init__(self):
        assert_type(self.torque, self.rpm,
                    expected_type=AbsoluteLimitValue)


@dataclass
class RelativeMechanicalLimitations():
    """
    Contains the electric variables subject to limitations.
    """
    torque: RelativeLimitValue
    rpm: RelativeLimitValue

    def __post_init__(self):
        assert_type(self.torque, self.rpm,
                    expected_type=RelativeLimitValue)


@dataclass
class AbsoluteLiquidFuelLimitations():
    """
    Contains the limitations on liquid fuel transfer.
    """
    fuel_liters: AbsoluteLimitValue

    def __post_init__(self):
        assert_type(self.fuel_liters,
                    expected_type=AbsoluteLimitValue)


@dataclass
class RelativeLiquidFuelLimitations():
    """
    Contains the limitations on liquid fuel transfer.
    """
    fuel_liters: RelativeLimitValue

    def __post_init__(self):
        assert_type(self.fuel_liters,
                    expected_type=RelativeLimitValue)


@dataclass
class AbsoluteGaseousFuelLimitations():
    """
    Contains the limitations on gaseous fuel transfer.
    """
    fuel_mass: AbsoluteLimitValue

    def __post_init__(self):
        assert_type(self.fuel_mass,
                    expected_type=AbsoluteLimitValue)


@dataclass
class RelativeGaseousFuelLimitations():
    """
    Contains the limitations on gaseous fuel transfer.
    """
    fuel_mass: RelativeLimitValue

    def __post_init__(self):
        assert_type(self.fuel_mass,
                    expected_type=RelativeLimitValue)


# ========================
# INPUT/OUTPUT LIMITATIONS
# ========================


@dataclass
class AbsoluteBaseLimitWithInternal():
    internal: AbsoluteInternalLimitations

    def __post_init__(self):
        assert_type(self.internal,
                    expected_type=AbsoluteInternalLimitations)

@dataclass
class RelativeBaseLimitWithInternal():
    internal: RelativeInternalLimitations

    def __post_init__(self):
        assert_type(self.internal,
                    expected_type=RelativeInternalLimitations)

@dataclass
class RechargeableBatteryAbsoluteLimits(AbsoluteBaseLimitWithInternal):
    input: AbsoluteElectricLimitations
    output: AbsoluteElectricLimitations

    def __post_init__(self):
        assert_type(self.input, self.output,
                    expected_type=AbsoluteElectricLimitations)

@dataclass
class RechargeableBatteryRelativeLimits(RelativeBaseLimitWithInternal):
    input: RelativeElectricLimitations
    output: RelativeElectricLimitations

    def __post_init__(self):
        assert_type(self.input, self.output,
                    expected_type=RelativeElectricLimitations)

@dataclass
class NonRechargeableBatteryAbsoluteLimits(AbsoluteBaseLimitWithInternal):
    output: AbsoluteElectricLimitations

    def __post_init__(self):
        assert_type(self.output,
                    expected_type=AbsoluteElectricLimitations)

@dataclass
class NonRechargeableBatteryRelativeLimits(RelativeBaseLimitWithInternal):
    output: RelativeElectricLimitations

    def __post_init__(self):
        assert_type(self.output,
                    expected_type=RelativeElectricLimitations)

@dataclass
class ElectricMotorAbsoluteLimits(AbsoluteBaseLimitWithInternal):
    input: AbsoluteElectricLimitations
    output: AbsoluteMechanicalLimitations

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=AbsoluteElectricLimitations)
        assert_type(self.output,
                    expected_type=AbsoluteMechanicalLimitations)

@dataclass
class ElectricMotorRelativeLimits(RelativeBaseLimitWithInternal):
    input: RelativeElectricLimitations
    output: RelativeMechanicalLimitations

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=RelativeElectricLimitations)
        assert_type(self.output,
                    expected_type=RelativeMechanicalLimitations)

@dataclass
class LiquidCombustionEngineAbsoluteLimits(AbsoluteBaseLimitWithInternal):
    input: AbsoluteLiquidFuelLimitations
    output: AbsoluteMechanicalLimitations

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=AbsoluteLiquidFuelLimitations)
        assert_type(self.output,
                    expected_type=AbsoluteMechanicalLimitations)

@dataclass
class LiquidCombustionEngineRelativeLimits(RelativeBaseLimitWithInternal):
    input: RelativeLiquidFuelLimitations
    output: RelativeMechanicalLimitations

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=RelativeLiquidFuelLimitations)
        assert_type(self.output,
                    expected_type=RelativeMechanicalLimitations)

@dataclass
class GaseousCombustionEngineAbsoluteLimits(AbsoluteBaseLimitWithInternal):
    input: AbsoluteGaseousFuelLimitations
    output: AbsoluteMechanicalLimitations

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=AbsoluteGaseousFuelLimitations)
        assert_type(self.output,
                    expected_type=AbsoluteMechanicalLimitations)

@dataclass
class GaseousCombustionEngineRelativeLimits(RelativeBaseLimitWithInternal):
    input: RelativeGaseousFuelLimitations
    output: RelativeMechanicalLimitations

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=RelativeGaseousFuelLimitations)
        assert_type(self.output,
                    expected_type=RelativeMechanicalLimitations)

@dataclass
class ElectricGeneratorAbsoluteLimits(AbsoluteBaseLimitWithInternal):
    input: AbsoluteMechanicalLimitations
    output: AbsoluteElectricLimitations

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=AbsoluteMechanicalLimitations)
        assert_type(self.output,
                    expected_type=AbsoluteElectricLimitations)

@dataclass
class ElectricGeneratorRelativeLimits(RelativeBaseLimitWithInternal):
    input: RelativeMechanicalLimitations
    output: RelativeElectricLimitations

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=RelativeMechanicalLimitations)
        assert_type(self.output,
                    expected_type=RelativeElectricLimitations)

@dataclass
class FuelCellAbsoluteLimits(AbsoluteBaseLimitWithInternal):
    input: AbsoluteGaseousFuelLimitations
    output: AbsoluteElectricLimitations

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=AbsoluteGaseousFuelLimitations)
        assert_type(self.output,
                    expected_type=AbsoluteElectricLimitations)

@dataclass
class FuelCellRelativeLimits(RelativeBaseLimitWithInternal):
    input: RelativeGaseousFuelLimitations
    output: RelativeElectricLimitations

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=RelativeGaseousFuelLimitations)
        assert_type(self.output,
                    expected_type=RelativeElectricLimitations)

@dataclass
class PureElectricAbsoluteLimits(AbsoluteBaseLimitWithInternal):
    input: AbsoluteElectricLimitations
    output: AbsoluteElectricLimitations

    def __post_init__(self):
        assert_type(self.input, self.output,
                    expected_type=AbsoluteElectricLimitations)

@dataclass
class PureElectricRelativeLimits(RelativeBaseLimitWithInternal):
    input: RelativeElectricLimitations
    output: RelativeElectricLimitations

    def __post_init__(self):
        assert_type(self.input, self.output,
                    expected_type=RelativeElectricLimitations)

@dataclass
class PureMechanicalAbsoluteLimits(AbsoluteBaseLimitWithInternal):
    input: AbsoluteMechanicalLimitations
    output: AbsoluteMechanicalLimitations

    def __post_init__(self):
        assert_type(self.input, self.output,
                    expected_type=AbsoluteMechanicalLimitations)

@dataclass
class PureMechanicalRelativeLimits(RelativeBaseLimitWithInternal):
    input: RelativeMechanicalLimitations
    output: RelativeMechanicalLimitations

    def __post_init__(self):
        assert_type(self.input, self.output,
                    expected_type=RelativeMechanicalLimitations)


# ===========================
# TAILORED LIMITATION CLASSES
# ===========================


@dataclass
class RechargeableBatteryLimits():
    """
    Holds the limitations of a rechargeable battery.
    """
    absolute_limits: RechargeableBatteryAbsoluteLimits
    relative_limits: RechargeableBatteryRelativeLimits


@dataclass
class NonRechargeableBatteryLimits():
    """
    Holds the limitations of a non rechargeable battery.
    """
    absolute_limits: NonRechargeableBatteryAbsoluteLimits
    relative_limits: NonRechargeableBatteryRelativeLimits


@dataclass
class ElectricMotorLimits():
    """
    Holds the limitations of an electric motor.
    """
    absolute_limits: ElectricMotorAbsoluteLimits
    relative_limits: ElectricMotorRelativeLimits


@dataclass
class LiquidCombustionEngineLimits():
    """
    Holds the limitations of a liquid fuel combustion engine.
    """
    absolute_limits: LiquidCombustionEngineAbsoluteLimits
    relative_limits: LiquidCombustionEngineRelativeLimits


@dataclass
class GaseousCombustionEngineLimits():
    """
    Holds the limitations of a gaseous fuel combustion engine.
    """
    absolute_limits: GaseousCombustionEngineAbsoluteLimits
    relative_limits: GaseousCombustionEngineRelativeLimits


@dataclass
class FuelCellLimits():
    """
    Holds the limitations of a fuel cell.
    """
    absolute_limits: FuelCellAbsoluteLimits
    relative_limits: FuelCellRelativeLimits


@dataclass
class ElectricGeneratorLimits():
    """
    Holds the limitations of an electric generator.
    """
    absolute_limits: ElectricGeneratorAbsoluteLimits
    relative_limits: ElectricGeneratorRelativeLimits


@dataclass
class MechanicalToMechanicalLimits():
    """
    Holds the limitations of a mechanical to
    mechanical converter (gears, etc).
    """
    absolute_limits: PureMechanicalAbsoluteLimits
    relative_limits: PureMechanicalRelativeLimits


@dataclass
class ElectricToElectricLimits():
    """
    Holds the limitations of an electric to
    electric converter (rectifier, inverter, etc).
    """
    absolute_limits: PureElectricAbsoluteLimits
    relative_limits: PureElectricRelativeLimits


# ==================
# CREATION FUNCTIONS
# ==================

def return_rechargeable_battery_limits(abs_max_temp: float, abs_min_temp: float,
                                       abs_max_voltage_in: float, abs_min_voltage_in: float,
                                       abs_max_current_in: float, abs_min_current_in: float,
                                       abs_max_voltage_out: float, abs_min_voltage_out: float,
                                       abs_max_current_out: float, abs_min_current_out: float,
                                       rel_max_temp: Callable, rel_min_temp: Callable,
                                       rel_max_voltage_in: Callable, rel_min_voltage_in: Callable,
                                       rel_max_current_in: Callable, rel_min_current_in: Callable,
                                       rel_max_voltage_out: Callable, rel_min_voltage_out: Callable,
                                       rel_max_current_out: Callable, rel_min_current_out: Callable) -> RechargeableBatteryLimits:
    return RechargeableBatteryLimits(absolute_limits=RechargeableBatteryAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                                           min=abs_min_temp)),
                                                                                       input=AbsoluteElectricLimitations(voltage=AbsoluteLimitValue(max=abs_max_voltage_in,
                                                                                                                                                    min=abs_min_voltage_in),
                                                                                                                         current=AbsoluteLimitValue(max=abs_max_current_in,
                                                                                                                                                    min=abs_min_current_in)),
                                                                                       output=AbsoluteElectricLimitations(voltage=AbsoluteLimitValue(max=abs_max_voltage_out,
                                                                                                                                                     min=abs_min_voltage_out),
                                                                                                                          current=AbsoluteLimitValue(max=abs_max_current_out,
                                                                                                                                                     min=abs_min_current_out))),
                                     relative_limits=RechargeableBatteryRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                           min=rel_min_temp)),
                                                                                       input=RelativeElectricLimitations(voltage=RelativeLimitValue(max=rel_max_voltage_in,
                                                                                                                                                    min=rel_min_voltage_in),
                                                                                                                         current=RelativeLimitValue(max=rel_max_current_in,
                                                                                                                                                    min=rel_min_current_in)),
                                                                                       output=RelativeElectricLimitations(voltage=RelativeLimitValue(max=rel_max_voltage_out,
                                                                                                                                                     min=rel_min_voltage_out),
                                                                                                                          current=RelativeLimitValue(max=rel_max_current_out,
                                                                                                                                                     min=rel_min_current_out)))
                                     )

def return_non_rechargeable_battery_limits(abs_max_temp: float, abs_min_temp: float,
                                           abs_max_voltage_out: float, abs_min_voltage_out: float,
                                           abs_max_current_out: float, abs_min_current_out: float,
                                           rel_max_temp: Callable, rel_min_temp: Callable,
                                           rel_max_voltage_out: Callable, rel_min_voltage_out: Callable,
                                           rel_max_current_out: Callable, rel_min_current_out: Callable) -> NonRechargeableBatteryLimits:
    return NonRechargeableBatteryLimits(absolute_limits=NonRechargeableBatteryAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                                                 min=abs_min_temp)),
                                                                                             output=AbsoluteElectricLimitations(voltage=AbsoluteLimitValue(max=abs_max_voltage_out,
                                                                                                                                                           min=abs_min_voltage_out),
                                                                                                                                current=AbsoluteLimitValue(max=abs_max_current_out,
                                                                                                                                                           min=abs_min_current_out))),
                                        relative_limits=NonRechargeableBatteryRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                                 min=rel_min_temp)),
                                                                                             output=RelativeElectricLimitations(voltage=RelativeLimitValue(max=rel_max_voltage_out,
                                                                                                                                                           min=rel_min_voltage_out),
                                                                                                                                current=RelativeLimitValue(max=rel_max_current_out,
                                                                                                                                                           min=rel_min_current_out)))
                                        )

def return_electric_motor_limits(abs_max_temp: float, abs_min_temp: float,
                                 abs_max_voltage_in: float, abs_min_voltage_in: float,
                                 abs_max_current_in: float, abs_min_current_in: float,
                                 abs_max_torque_out: float, abs_min_torque_out: float,
                                 abs_max_rpm_out: float, abs_min_rpm_out: float,
                                 rel_max_temp: Callable, rel_min_temp: Callable,
                                 rel_max_voltage_in: Callable, rel_min_voltage_in: Callable,
                                 rel_max_current_in: Callable, rel_min_current_in: Callable,
                                 rel_max_torque_out: Callable, rel_min_torque_out: Callable,
                                 rel_max_rpm_out: Callable, rel_min_rpm_out: Callable) -> ElectricMotorLimits:
    return ElectricMotorLimits(absolute_limits=ElectricMotorAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                               min=abs_min_temp)),
                                                                           input=AbsoluteElectricLimitations(voltage=AbsoluteLimitValue(max=abs_max_voltage_in,
                                                                                                                                        min=abs_min_voltage_in),
                                                                                                             current=AbsoluteLimitValue(max=abs_max_current_in,
                                                                                                                                        min=abs_min_current_in)),
                                                                           output=AbsoluteMechanicalLimitations(torque=AbsoluteLimitValue(max=abs_max_torque_out,
                                                                                                                                          min=abs_min_torque_out),
                                                                                                                rpm=AbsoluteLimitValue(max=abs_max_rpm_out,
                                                                                                                                       min=abs_min_rpm_out))),
                               relative_limits=ElectricMotorRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                               min=rel_min_temp)),
                                                                           input=RelativeElectricLimitations(voltage=RelativeLimitValue(max=rel_max_voltage_in,
                                                                                                                                        min=rel_min_voltage_in),
                                                                                                             current=RelativeLimitValue(max=rel_max_current_in,
                                                                                                                                        min=rel_min_current_in)),
                                                                           output=RelativeMechanicalLimitations(torque=RelativeLimitValue(max=rel_max_torque_out,
                                                                                                                                          min=rel_min_torque_out),
                                                                                                                rpm=RelativeLimitValue(max=rel_max_rpm_out,
                                                                                                                                       min=rel_min_rpm_out)))
                               )

def return_liquid_combustion_engine_limits(abs_max_temp: float, abs_min_temp: float,
                                           abs_max_fuel_liters_in: float, abs_min_fuel_liters_in: float,
                                           abs_max_torque_out: float, abs_min_torque_out: float,
                                           abs_max_rpm_out: float, abs_min_rpm_out: float,
                                           rel_max_temp: Callable, rel_min_temp: Callable,
                                           rel_max_fuel_liters_in: Callable, rel_min_fuel_liters_in: Callable,
                                           rel_max_torque_out: Callable, rel_min_torque_out: Callable,
                                           rel_max_rpm_out: Callable, rel_min_rpm_out: Callable) -> LiquidCombustionEngineLimits:
    return LiquidCombustionEngineLimits(absolute_limits=LiquidCombustionEngineAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                                                 min=abs_min_temp)),
                                                                                             input=AbsoluteLiquidFuelLimitations(fuel_liters=AbsoluteLimitValue(max=abs_max_fuel_liters_in,
                                                                                                                                                                min=abs_min_fuel_liters_in)),
                                                                                             output=AbsoluteMechanicalLimitations(torque=AbsoluteLimitValue(max=abs_max_torque_out,
                                                                                                                                                            min=abs_min_torque_out),
                                                                                                                                  rpm=AbsoluteLimitValue(max=abs_max_rpm_out,
                                                                                                                                                         min=abs_min_rpm_out))),
                                        relative_limits=LiquidCombustionEngineRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                                 min=rel_min_temp)),
                                                                                             input=RelativeLiquidFuelLimitations(fuel_liters=RelativeLimitValue(max=rel_max_fuel_liters_in,
                                                                                                                                                                min=rel_min_fuel_liters_in)),
                                                                                             output=RelativeMechanicalLimitations(torque=RelativeLimitValue(max=rel_max_torque_out,
                                                                                                                                                            min=rel_min_torque_out),
                                                                                                                                  rpm=RelativeLimitValue(max=rel_max_rpm_out,
                                                                                                                                                         min=rel_min_rpm_out)))
                                        )

def return_gaseous_combustion_engine_limits(abs_max_temp: float, abs_min_temp: float,
                                            abs_max_fuel_mass_in: float, abs_min_fuel_mass_in: float,
                                            abs_max_torque_out: float, abs_min_torque_out: float,
                                            abs_max_rpm_out: float, abs_min_rpm_out: float,
                                            rel_max_temp: Callable, rel_min_temp: Callable,
                                            rel_max_fuel_mass_in: Callable, rel_min_fuel_mass_in: Callable,
                                            rel_max_torque_out: Callable, rel_min_torque_out: Callable,
                                            rel_max_rpm_out: Callable, rel_min_rpm_out: Callable) -> GaseousCombustionEngineLimits:
    return GaseousCombustionEngineLimits(absolute_limits=GaseousCombustionEngineAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                                                   min=abs_min_temp)),
                                                                                               input=AbsoluteGaseousFuelLimitations(fuel_mass=AbsoluteLimitValue(max=abs_max_fuel_mass_in,
                                                                                                                                                                 min=abs_min_fuel_mass_in)),
                                                                                               output=AbsoluteMechanicalLimitations(torque=AbsoluteLimitValue(max=abs_max_torque_out,
                                                                                                                                                              min=abs_min_torque_out),
                                                                                                                                    rpm=AbsoluteLimitValue(max=abs_max_rpm_out,
                                                                                                                                                           min=abs_min_rpm_out))),
                                         relative_limits=GaseousCombustionEngineRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                                  min=rel_min_temp)),
                                                                                               input=RelativeGaseousFuelLimitations(fuel_mass=RelativeLimitValue(max=rel_max_fuel_mass_in,
                                                                                                                                                                 min=rel_min_fuel_mass_in)),
                                                                                               output=RelativeMechanicalLimitations(torque=RelativeLimitValue(max=rel_max_torque_out,
                                                                                                                                                              min=rel_min_torque_out),
                                                                                                                                    rpm=RelativeLimitValue(max=rel_max_rpm_out,
                                                                                                                                                           min=rel_min_rpm_out)))
                                         )

def return_fuel_cell_limits(abs_max_temp: float, abs_min_temp: float,
                            abs_max_fuel_mass_in: float, abs_min_fuel_mass_in: float,
                            abs_max_voltage_out: float, abs_min_voltage_out: float,
                            abs_max_current_out: float, abs_min_current_out: float,
                            rel_max_temp: Callable, rel_min_temp: Callable,
                            rel_max_fuel_mass_in: Callable, rel_min_fuel_mass_in: Callable,
                            rel_max_voltage_out: Callable, rel_min_voltage_out: Callable,
                            rel_max_current_out: Callable, rel_min_current_out: Callable) -> FuelCellLimits:
    return FuelCellLimits(absolute_limits=FuelCellAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                     min=abs_min_temp)),
                                                                 input=AbsoluteGaseousFuelLimitations(fuel_mass=AbsoluteLimitValue(max=abs_max_fuel_mass_in,
                                                                                                                                   min=abs_min_fuel_mass_in)),
                                                                 output=AbsoluteElectricLimitations(voltage=AbsoluteLimitValue(max=abs_max_voltage_out,
                                                                                                                               min=abs_min_voltage_out),
                                                                                                    current=AbsoluteLimitValue(max=abs_max_current_out,
                                                                                                                               min=abs_min_current_out))),
                          relative_limits=FuelCellRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                     min=rel_min_temp)),
                                                                 input=RelativeGaseousFuelLimitations(fuel_mass=RelativeLimitValue(max=rel_max_fuel_mass_in,
                                                                                                                                   min=rel_min_fuel_mass_in)),
                                                                 output=RelativeElectricLimitations(voltage=RelativeLimitValue(max=rel_max_voltage_out,
                                                                                                                               min=rel_min_voltage_out),
                                                                                                    current=RelativeLimitValue(max=rel_max_current_out,
                                                                                                                               min=rel_min_current_out)))
                          )

def return_electric_generator_limits(abs_max_temp: float, abs_min_temp: float,
                                     abs_max_torque_in: float, abs_min_torque_in: float,
                                     abs_max_rpm_in: float, abs_min_rpm_in: float,
                                     abs_max_voltage_out: float, abs_min_voltage_out: float,
                                     abs_max_current_out: float, abs_min_current_out: float,
                                     rel_max_temp: Callable, rel_min_temp: Callable,
                                     rel_max_torque_in: Callable, rel_min_torque_in: Callable,
                                     rel_max_rpm_in: Callable, rel_min_rpm_in: Callable,
                                     rel_max_voltage_out: Callable, rel_min_voltage_out: Callable,
                                     rel_max_current_out: Callable, rel_min_current_out: Callable) -> ElectricGeneratorLimits:
    return ElectricGeneratorLimits(absolute_limits=ElectricGeneratorAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                                       min=abs_min_temp)),
                                                                                   input=AbsoluteMechanicalLimitations(torque=AbsoluteLimitValue(max=abs_max_torque_in,
                                                                                                                                                 min=abs_min_torque_in),
                                                                                                                       rpm=AbsoluteLimitValue(max=abs_max_rpm_in,
                                                                                                                                              min=abs_min_rpm_in)),
                                                                                   output=AbsoluteElectricLimitations(voltage=AbsoluteLimitValue(max=abs_max_voltage_out,
                                                                                                                                                 min=abs_min_voltage_out),
                                                                                                                      current=AbsoluteLimitValue(max=abs_max_current_out,
                                                                                                                                                 min=abs_min_current_out))),
                                   relative_limits=ElectricGeneratorRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                       min=rel_min_temp)),
                                                                                   input=RelativeMechanicalLimitations(torque=RelativeLimitValue(max=rel_max_torque_in,
                                                                                                                                                 min=rel_min_torque_in),
                                                                                                                       rpm=RelativeLimitValue(max=rel_max_rpm_in,
                                                                                                                                              min=rel_min_rpm_in)),
                                                                                   output=RelativeElectricLimitations(voltage=RelativeLimitValue(max=rel_max_voltage_out,
                                                                                                                                                 min=rel_min_voltage_out),
                                                                                                                      current=RelativeLimitValue(max=rel_max_current_out,
                                                                                                                                                 min=rel_min_current_out)))
                                   )

def return_mechanical_to_mechanical_limits(abs_max_temp: float, abs_min_temp: float,
                                           abs_max_torque_in: float, abs_min_torque_in: float,
                                           abs_max_rpm_in: float, abs_min_rpm_in: float,
                                           abs_max_torque_out: float, abs_min_torque_out: float,
                                           abs_max_rpm_out: float, abs_min_rpm_out: float,
                                           rel_max_temp: Callable, rel_min_temp: Callable,
                                           rel_max_torque_in: Callable, rel_min_torque_in: Callable,
                                           rel_max_rpm_in: Callable, rel_min_rpm_in: Callable,
                                           rel_max_torque_out: Callable, rel_min_torque_out: Callable,
                                           rel_max_rpm_out: Callable, rel_min_rpm_out: Callable) -> MechanicalToMechanicalLimits:
    return MechanicalToMechanicalLimits(absolute_limits=PureMechanicalAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                                         min=abs_min_temp)),
                                                                                     input=AbsoluteMechanicalLimitations(torque=AbsoluteLimitValue(max=abs_max_torque_in,
                                                                                                                                                   min=abs_min_torque_in),
                                                                                                                         rpm=AbsoluteLimitValue(max=abs_max_rpm_in,
                                                                                                                                                min=abs_min_rpm_in)),
                                                                                     output=AbsoluteMechanicalLimitations(torque=AbsoluteLimitValue(max=abs_max_torque_out,
                                                                                                                                                    min=abs_min_torque_out),
                                                                                                                          rpm=AbsoluteLimitValue(max=abs_max_rpm_out,
                                                                                                                                                 min=abs_min_rpm_out))),
                                        relative_limits=PureMechanicalRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                         min=rel_min_temp)),
                                                                                     input=RelativeMechanicalLimitations(torque=RelativeLimitValue(max=rel_max_torque_in,
                                                                                                                                                   min=rel_min_torque_in),
                                                                                                                         rpm=RelativeLimitValue(max=rel_max_rpm_in,
                                                                                                                                                min=rel_min_rpm_in)),
                                                                                     output=RelativeMechanicalLimitations(torque=RelativeLimitValue(max=rel_max_torque_out,
                                                                                                                                                    min=rel_min_torque_out),
                                                                                                                          rpm=RelativeLimitValue(max=rel_max_rpm_out,
                                                                                                                                                 min=rel_min_rpm_out)))
                                        )

def return_electric_to_electric_limits(abs_max_temp: float, abs_min_temp: float,
                                       abs_max_voltage_in: float, abs_min_voltage_in: float,
                                       abs_max_current_in: float, abs_min_current_in: float,
                                       abs_max_voltage_out: float, abs_min_voltage_out: float,
                                       abs_max_current_out: float, abs_min_current_out: float,
                                       rel_max_temp: Callable, rel_min_temp: Callable,
                                       rel_max_voltage_in: Callable, rel_min_voltage_in: Callable,
                                       rel_max_current_in: Callable, rel_min_current_in: Callable,
                                       rel_max_voltage_out: Callable, rel_min_voltage_out: Callable,
                                       rel_max_current_out: Callable, rel_min_current_out: Callable) -> ElectricToElectricLimits:
    return ElectricToElectricLimits(absolute_limits=PureElectricAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                                   min=abs_min_temp)),
                                                                               input=AbsoluteElectricLimitations(voltage=AbsoluteLimitValue(max=abs_max_voltage_in,
                                                                                                                                            min=abs_min_voltage_in),
                                                                                                                 current=AbsoluteLimitValue(max=abs_max_current_in,
                                                                                                                                            min=abs_min_current_in)),
                                                                               output=AbsoluteElectricLimitations(voltage=AbsoluteLimitValue(max=abs_max_voltage_out,
                                                                                                                                             min=abs_min_voltage_out),
                                                                                                                  current=AbsoluteLimitValue(max=abs_max_current_out,
                                                                                                                                             min=abs_min_current_out))),
                                    relative_limits=PureElectricRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                   min=rel_min_temp)),
                                                                               input=RelativeElectricLimitations(voltage=RelativeLimitValue(max=rel_max_voltage_in,
                                                                                                                                            min=rel_min_voltage_in),
                                                                                                                 current=RelativeLimitValue(max=rel_max_current_in,
                                                                                                                                            min=rel_min_current_in)),
                                                                               output=RelativeElectricLimitations(voltage=RelativeLimitValue(max=rel_max_voltage_out,
                                                                                                                                             min=rel_min_voltage_out),
                                                                                                                  current=RelativeLimitValue(max=rel_max_current_out,
                                                                                                                                             min=rel_min_current_out)))
                                    )
