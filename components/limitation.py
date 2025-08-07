"""
This module contains routines for handling
components' state limitations.
"""

from abc import ABC
from dataclasses import dataclass
from typing import Callable
from components.state import FullStateNoInput, FullStateWithInput
from helpers.functions import assert_type, assert_numeric, assert_callable


# =================
# VALUE LIMITATIONS
# =================


@dataclass
class AbsoluteLimitValue():
    """
    Contains absolute limit values.
    """
    min: float
    max: float

    def __post_init__(self):
        assert_numeric(self.min, self.max)


@dataclass
class RelativeLimitValue():
    """
    Contains absolute limit values.
    """
    min: Callable[[FullStateNoInput|FullStateWithInput], float]
    max: Callable[[FullStateNoInput|FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.min, self.max)


# ====================
# INTERNAL LIMITATIONS
# ====================


@dataclass
class InternalLimitations():
    """
    Contains the internal variable subject to limitations.
    """
    temperature: AbsoluteLimitValue|RelativeLimitValue

    def __post_init__(self):
        assert_type(self.temperature,
                    expected_type=(AbsoluteLimitValue, RelativeLimitValue))


# ==============================================
# DOMAIN LIMITATIONS (ELECTRIC, MECHANICAL, ETC)
# ==============================================


@dataclass
class DomainLimitations():
    """
    Placeholder class for domain limitations.
    """


@dataclass
class ElectricLimitations(DomainLimitations):
    """
    Contains the electric variables subject to limitations.
    """
    voltage: AbsoluteLimitValue|RelativeLimitValue
    current: AbsoluteLimitValue|RelativeLimitValue

    def __post_init__(self):
        assert type(self.voltage)==type(self.current) and \
            type(self.voltage) in (AbsoluteLimitValue, RelativeLimitValue)


@dataclass
class MechanicalLimitations(DomainLimitations):
    """
    Contains the electric variables subject to limitations.
    """
    torque: AbsoluteLimitValue|RelativeLimitValue
    rpm: AbsoluteLimitValue|RelativeLimitValue

    def __post_init__(self):
        assert type(self.torque)==type(self.rpm) and \
            type(self.torque) in (AbsoluteLimitValue, RelativeLimitValue)


@dataclass
class FuelLimitations(DomainLimitations):
    """
    Placeholder for fuel limitations.
    """


@dataclass
class LiquidFuelLimitations(FuelLimitations):
    """
    Contains the limitations on liquid fuel transfer.
    """
    fuel_liters: AbsoluteLimitValue|RelativeLimitValue

    def __post_init__(self):
        assert_type(self.fuel_liters,
                    expected_type=(AbsoluteLimitValue, RelativeLimitValue))


@dataclass
class GaseousFuelLimitations(FuelLimitations):
    """
    Contains the limitations on gaseous fuel transfer.
    """
    fuel_mass: AbsoluteLimitValue|RelativeLimitValue

    def __post_init__(self):
        assert_type(self.fuel_mass,
                    expected_type=(AbsoluteLimitValue, RelativeLimitValue))


# ================
# FULL LIMITATIONS
# ================


@dataclass
class LimitsBase():
    """
    Contains the areas of limitations.
    """
    output: DomainLimitations
    internal: InternalLimitations

    def __post_init__(self):
        assert_type(self.output,
                    expected_type=DomainLimitations)
        assert_type(self.internal,
                    expected_type=InternalLimitations)


@dataclass
class LimitsWithInput(LimitsBase):
    """
    Adds an input to the limitations.
    """
    input: DomainLimitations

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=DomainLimitations)


class Limitation(ABC):
    """
    Base class for limitations.
    """
    absolute_limits: LimitsBase|LimitsWithInput
    relative_limits: LimitsBase|LimitsWithInput

    def __post_init__(self):
        assert_type(self.absolute_limits, self.relative_limits,
                    expected_type=(LimitsBase, LimitsWithInput))


# ===========================
# TAILORED LIMITATION CLASSES
# ===========================


@dataclass
class RechargeableBatteryLimits(Limitation):
    """
    Limits for a rechargeable battery.
    """
    def __init__(self,
                 absolute_voltage_in: AbsoluteLimitValue,
                 absolute_current_in: AbsoluteLimitValue,
                 absolute_voltage_out: AbsoluteLimitValue,
                 absolute_current_out: AbsoluteLimitValue,
                 absolute_temperature: AbsoluteLimitValue,
                 relative_voltage_in: RelativeLimitValue,
                 relative_current_in: RelativeLimitValue,
                 relative_voltage_out: RelativeLimitValue,
                 relative_current_out: RelativeLimitValue,
                 relative_temperature: RelativeLimitValue):
        assert_type(absolute_voltage_in, absolute_current_in,
                    absolute_voltage_out, absolute_current_out,
                    absolute_temperature,
                    expected_type=AbsoluteLimitValue)
        assert_type(relative_voltage_in, relative_current_in,
                    relative_voltage_out, relative_current_out,
                    relative_temperature,
                    expected_type=RelativeLimitValue)
        absolute_limits = LimitsWithInput(input=ElectricLimitations(voltage=absolute_voltage_in,
                                                                    current=absolute_current_in),
                                          output=ElectricLimitations(voltage=absolute_voltage_out,
                                                                     current=absolute_current_out),
                                          internal=InternalLimitations(temperature=absolute_temperature)
                                          )
        relative_limits = LimitsWithInput(input=ElectricLimitations(voltage=relative_voltage_in,
                                                                    current=relative_current_in),
                                          output=ElectricLimitations(voltage=relative_voltage_out,
                                                                     current=relative_current_out),
                                          internal=InternalLimitations(temperature=relative_temperature)
                                          )
        self.absolute_limits = absolute_limits
        self.relative_limits = relative_limits


@dataclass
class NonRechargeableBatteryLimits(Limitation):
    """
    Limits for a non rechargeable battery.
    """
    def __init__(self,
                 absolute_voltage_out: AbsoluteLimitValue,
                 absolute_current_out: AbsoluteLimitValue,
                 absolute_temperature: AbsoluteLimitValue,
                 relative_voltage_out: RelativeLimitValue,
                 relative_current_out: RelativeLimitValue,
                 relative_temperature: RelativeLimitValue):
        assert_type(absolute_voltage_out, absolute_current_out,
                    absolute_temperature,
                    expected_type=AbsoluteLimitValue)
        assert_type(relative_voltage_out, relative_current_out,
                    relative_temperature,
                    expected_type=RelativeLimitValue)
        absolute_limits = LimitsBase(output=ElectricLimitations(voltage=absolute_voltage_out,
                                                                current=absolute_current_out),
                                     internal=InternalLimitations(temperature=absolute_temperature)
                                     )
        relative_limits = LimitsBase(output=ElectricLimitations(voltage=relative_voltage_out,
                                                                current=relative_current_out),
                                     internal=InternalLimitations(temperature=relative_temperature)
                                     )
        self.absolute_limits = absolute_limits
        self.relative_limits = relative_limits


@dataclass
class FuelTankLimits(Limitation):
    """
    Limits for a liquid or gaseous fuel tank.
    """
    def __init__(self,
                 liquid_fuel: bool,
                 absolute_fuel_liters_out: AbsoluteLimitValue,
                 absolute_temperature: AbsoluteLimitValue,
                 relative_fuel_liters_out: RelativeLimitValue,
                 relative_temperature: RelativeLimitValue):
        assert_type(absolute_fuel_liters_out,
                    absolute_temperature,
                    expected_type=AbsoluteLimitValue)
        assert_type(relative_fuel_liters_out,
                    relative_temperature,
                    expected_type=RelativeLimitValue)
        abs_out = LiquidFuelLimitations(fuel_liters=absolute_fuel_liters_out) \
            if liquid_fuel else GaseousFuelLimitations(fuel_mass=absolute_fuel_liters_out)
        rel_out = LiquidFuelLimitations(fuel_liters=relative_fuel_liters_out) \
            if liquid_fuel else GaseousFuelLimitations(fuel_mass=relative_fuel_liters_out)
        absolute_limits = LimitsBase(output=abs_out,
                                     internal=InternalLimitations(temperature=absolute_temperature)
                                     )
        relative_limits = LimitsBase(output=rel_out,
                                     internal=InternalLimitations(temperature=relative_temperature)
                                     )
        self.absolute_limits = absolute_limits
        self.relative_limits = relative_limits


@dataclass
class ElectricMotorLimits(Limitation):
    """
    Limits for an electric motor.
    """
    def __init__(self,
                 absolute_voltage_in: AbsoluteLimitValue,
                 absolute_current_in: AbsoluteLimitValue,
                 absolute_torque_out: AbsoluteLimitValue,
                 absolute_rpm_out: AbsoluteLimitValue,
                 absolute_temperature: AbsoluteLimitValue,
                 relative_voltage_in: RelativeLimitValue,
                 relative_current_in: RelativeLimitValue,
                 relative_torque_out: RelativeLimitValue,
                 relative_rpm_out: RelativeLimitValue,
                 relative_temperature: RelativeLimitValue):
        assert_type(absolute_voltage_in, absolute_current_in,
                    absolute_torque_out, absolute_rpm_out,
                    absolute_temperature,
                    expected_type=AbsoluteLimitValue)
        assert_type(relative_voltage_in, relative_current_in,
                    relative_torque_out, relative_rpm_out,
                    relative_temperature,
                    expected_type=RelativeLimitValue)
        absolute_limits = LimitsWithInput(input=ElectricLimitations(voltage=absolute_voltage_in,
                                                                    current=absolute_current_in),
                                          output=MechanicalLimitations(torque=absolute_torque_out,
                                                                       rpm=absolute_rpm_out),
                                          internal=InternalLimitations(temperature=absolute_temperature)
                                          )
        relative_limits = LimitsWithInput(input=ElectricLimitations(voltage=relative_voltage_in,
                                                                    current=relative_current_in),
                                          output=MechanicalLimitations(torque=relative_torque_out,
                                                                       rpm=relative_rpm_out),
                                          internal=InternalLimitations(temperature=relative_temperature)
                                          )
        self.absolute_limits = absolute_limits
        self.relative_limits = relative_limits


@dataclass
class ICELimits(Limitation):
    """
    Limits for an internal combustion engine.
    """
    def __init__(self,
                 liquid_fuel: bool,
                 absolute_fuel_in: AbsoluteLimitValue,
                 absolute_torque_out: AbsoluteLimitValue,
                 absolute_rpm_out: AbsoluteLimitValue,
                 absolute_temperature: AbsoluteLimitValue,
                 relative_fuel_in: RelativeLimitValue,
                 relative_torque_out: RelativeLimitValue,
                 relative_rpm_out: RelativeLimitValue,
                 relative_temperature: RelativeLimitValue):
        assert_type(absolute_fuel_in,
                    absolute_torque_out, absolute_rpm_out,
                    absolute_temperature,
                    expected_type=AbsoluteLimitValue)
        assert_type(relative_fuel_in,
                    relative_torque_out, relative_rpm_out,
                    relative_temperature,
                    expected_type=RelativeLimitValue)
        abs_input = LiquidFuelLimitations(fuel_liters=absolute_fuel_in) \
            if liquid_fuel else GaseousFuelLimitations(fuel_mass=absolute_fuel_in)
        rel_input = LiquidFuelLimitations(fuel_liters=relative_fuel_in) \
            if liquid_fuel else GaseousFuelLimitations(fuel_mass=relative_fuel_in)
        absolute_limits = LimitsWithInput(input=abs_input,
                                          output=MechanicalLimitations(torque=absolute_torque_out,
                                                                       rpm=absolute_rpm_out),
                                          internal=InternalLimitations(temperature=absolute_temperature)
                                          )
        relative_limits = LimitsWithInput(input=rel_input,
                                          output=MechanicalLimitations(torque=relative_torque_out,
                                                                       rpm=relative_rpm_out),
                                          internal=InternalLimitations(temperature=relative_temperature)
                                          )
        self.absolute_limits = absolute_limits
        self.relative_limits = relative_limits


@dataclass
class ElectricGeneratorLimits(Limitation):
    """
    Limits for an electric generator.
    """


@dataclass
class MechanicalToMechanicalLimits(Limitation):
    """
    Limits for a pure mechanical component.
    """
