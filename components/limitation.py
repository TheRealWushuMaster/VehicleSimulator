"""
This module contains routines for handling
components' state limitations.
"""

from collections.abc import Callable
from dataclasses import dataclass
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
    max: float
    min: float=0.0

    def __post_init__(self):
        assert_numeric(self.max, self.min)


@dataclass
class RelativeLimitValue():
    """
    Contains absolute limit values.
    """
    max: Callable[[FullStateNoInput|FullStateWithInput], float]
    min: Callable[[FullStateNoInput|FullStateWithInput], float]=lambda s: 0.0

    def __post_init__(self):
        assert_callable(self.max, self.min)


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
class BaseLimitWithInternal():
    internal: InternalLimitations

@dataclass
class RechargeableBatteryAbsoluteLimits(BaseLimitWithInternal):
    input: AbsoluteElectricLimitations
    output: AbsoluteElectricLimitations

@dataclass
class RechargeableBatteryRelativeLimits(BaseLimitWithInternal):
    input: RelativeElectricLimitations
    output: RelativeElectricLimitations

@dataclass
class NonRechargeableBatteryAbsoluteLimits(BaseLimitWithInternal):
    output: AbsoluteElectricLimitations

@dataclass
class NonRechargeableBatteryRelativeLimits(BaseLimitWithInternal):
    output: RelativeElectricLimitations

@dataclass
class ElectricMotorAbsoluteLimits(BaseLimitWithInternal):
    input: AbsoluteElectricLimitations
    output: AbsoluteMechanicalLimitations

@dataclass
class ElectricMotorRelativeLimits(BaseLimitWithInternal):
    input: RelativeElectricLimitations
    output: RelativeMechanicalLimitations

@dataclass
class LiquidCombustionEngineAbsoluteLimits(BaseLimitWithInternal):
    input: AbsoluteLiquidFuelLimitations
    output: AbsoluteMechanicalLimitations

@dataclass
class LiquidCombustionEngineRelativeLimits(BaseLimitWithInternal):
    input: RelativeLiquidFuelLimitations
    output: RelativeMechanicalLimitations

@dataclass
class GaseousCombustionEngineAbsoluteLimits(BaseLimitWithInternal):
    input: AbsoluteGaseousFuelLimitations
    output: AbsoluteMechanicalLimitations

@dataclass
class GaseousCombustionEngineRelativeLimits(BaseLimitWithInternal):
    input: RelativeGaseousFuelLimitations
    output: RelativeMechanicalLimitations

@dataclass
class ElectricGeneratorAbsoluteLimits(BaseLimitWithInternal):
    input: AbsoluteMechanicalLimitations
    output: AbsoluteElectricLimitations

@dataclass
class ElectricGeneratorRelativeLimits(BaseLimitWithInternal):
    input: RelativeMechanicalLimitations
    output: RelativeElectricLimitations

@dataclass
class PureElectricAbsoluteLimits(BaseLimitWithInternal):
    input: AbsoluteElectricLimitations
    output: AbsoluteElectricLimitations

@dataclass
class PureElectricRelativeLimits(BaseLimitWithInternal):
    input: RelativeElectricLimitations
    output: RelativeElectricLimitations

@dataclass
class PureMechanicalAbsoluteLimits(BaseLimitWithInternal):
    input: AbsoluteMechanicalLimitations
    output: AbsoluteMechanicalLimitations

@dataclass
class PureMechanicalRelativeLimits(BaseLimitWithInternal):
    input: RelativeMechanicalLimitations
    output: RelativeMechanicalLimitations


# ===========================
# TAILORED LIMITATION CLASSES
# ===========================


@dataclass
class RechargeableBattery():
    """
    Holds the limitations of a rechargeable battery.
    """
    absolute_limits: RechargeableBatteryAbsoluteLimits
    relative_limits: RechargeableBatteryRelativeLimits


@dataclass
class NonRechargeableBattery():
    """
    Holds the limitations of a non rechargeable battery.
    """
    absolute_limits: NonRechargeableBatteryAbsoluteLimits
    relative_limits: NonRechargeableBatteryRelativeLimits


@dataclass
class LiquidCombustionEngine():
    """
    Holds the limitations of a liquid fuel combustion engine.
    """
    absolute_limits: LiquidCombustionEngineAbsoluteLimits
    relative_limits: LiquidCombustionEngineRelativeLimits


@dataclass
class GaseousCombustionEngine():
    """
    Holds the limitations of a gaseous fuel combustion engine.
    """
    absolute_limits: GaseousCombustionEngineAbsoluteLimits
    relative_limits: GaseousCombustionEngineRelativeLimits


@dataclass
class ElectricGenerator():
    """
    Holds the limitations of an electric generator.
    """
    absolute_limits: ElectricGeneratorAbsoluteLimits
    relative_limits: ElectricGeneratorRelativeLimits


@dataclass
class MechanicalToMechanical():
    """
    Holds the limitations of a mechanical to
    mechanical converter (gears, etc).
    """
    absolute_limits: PureMechanicalAbsoluteLimits
    relative_limits: PureMechanicalRelativeLimits


@dataclass
class ElectricToElectric():
    """
    Holds the limitations of an electric to
    electric converter (rectifier, inverter, etc).
    """
    absolute_limits: PureElectricAbsoluteLimits
    relative_limits: PureElectricRelativeLimits
