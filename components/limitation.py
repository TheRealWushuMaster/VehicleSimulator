"""
This module contains routines for handling
components' state limitations.
"""

from collections.abc import Callable
from dataclasses import dataclass
from components.state import FullStateNoInput, FullStateWithInput
from helpers.functions import assert_type, assert_numeric, \
    assert_callable, assert_range, assert_type_and_range


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
    power: AbsoluteLimitValue

    def __post_init__(self):
        assert_type(self.power,
                    expected_type=AbsoluteLimitValue)


@dataclass
class RelativeElectricLimitations():
    """
    Contains the electric variables subject to limitations.
    """
    power: RelativeLimitValue

    def __post_init__(self):
        assert_type(self.power,
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
    Contains the limitations on liquid fuel transfer and storage.
    """
    fuel_liters_transfer: AbsoluteLimitValue

    def __post_init__(self):
        assert_type(self.fuel_liters_transfer,
                    expected_type=AbsoluteLimitValue)


@dataclass
class RelativeLiquidFuelLimitations():
    """
    Contains the limitations on liquid fuel transfer and storage.
    """
    fuel_liters_transfer: RelativeLimitValue

    def __post_init__(self):
        assert_type(self.fuel_liters_transfer,
                    expected_type=RelativeLimitValue)


@dataclass
class AbsoluteGaseousFuelLimitations():
    """
    Contains the limitations on gaseous fuel transfer.
    """
    fuel_mass_transfer: AbsoluteLimitValue

    def __post_init__(self):
        assert_type(self.fuel_mass_transfer,
                    expected_type=AbsoluteLimitValue)


@dataclass
class RelativeGaseousFuelLimitations():
    """
    Contains the limitations on gaseous fuel transfer.
    """
    fuel_mass_transfer: RelativeLimitValue

    def __post_init__(self):
        assert_type(self.fuel_mass_transfer,
                    expected_type=RelativeLimitValue)


# ===================
# STORAGE LIMITATIONS
# ===================


@dataclass
class AbsoluteElectricEnergyStorageLimitations():
    electric_energy_capacity: float

    def __post_init__(self):
        assert_type_and_range(self.electric_energy_capacity,
                              more_than=0.0,
                              include_more=False)


@dataclass
class RelativeElectricEnergyStorageLimitations():
    electric_energy_capacity: Callable[[FullStateNoInput|FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.electric_energy_capacity)


@dataclass
class AbsoluteLiquidFuelStorageLimitations():
    fuel_liters_capacity: float

    def __post_init__(self):
        assert_type_and_range(self.fuel_liters_capacity,
                              more_than=0.0,
                              include_more=False)


@dataclass
class RelativeLiquidFuelStorageLimitations():
    fuel_liters_capacity: Callable[[FullStateNoInput], float]

    def __post_init__(self):
        assert_callable(self.fuel_liters_capacity)


@dataclass
class AbsoluteGaseousFuelStorageLimitations():
    fuel_mass_capacity: float

    def __post_init__(self):
        assert_type_and_range(self.fuel_mass_capacity,
                              more_than=0.0,
                              include_more=False)


@dataclass
class RelativeGaseousFuelStorageLimitations():
    fuel_mass_capacity: Callable[[FullStateNoInput], float]

    def __post_init__(self):
        assert_callable(self.fuel_mass_capacity)


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

@dataclass
class LiquidFuelTankAbsoluteLimits(AbsoluteBaseLimitWithInternal):
    output: AbsoluteLiquidFuelLimitations

    def __post_init__(self):
        assert_type(self.output,
                    expected_type=AbsoluteLiquidFuelLimitations)

@dataclass
class LiquidFuelTankRelativeLimits(RelativeBaseLimitWithInternal):
    output: RelativeLiquidFuelLimitations

    def __post_init__(self):
        assert_type(self.output,
                    expected_type=RelativeLiquidFuelLimitations)

@dataclass
class GaseousFuelTankAbsoluteLimits(AbsoluteBaseLimitWithInternal):
    output: AbsoluteGaseousFuelLimitations

    def __post_init__(self):
        assert_type(self.output,
                    expected_type=AbsoluteGaseousFuelLimitations)

@dataclass
class GaseousFuelTankRelativeLimits(RelativeBaseLimitWithInternal):
    output: RelativeGaseousFuelLimitations

    def __post_init__(self):
        assert_type(self.output,
                    expected_type=RelativeGaseousFuelLimitations)


# ===========================
# TAILORED LIMITATION CLASSES
# ===========================


@dataclass
class EnergySourceLimits():
    """
    Placeholder for energy sources' tailored limits.
    """


@dataclass
class ConverterLimits():
    """
    Placeholder for converters' tailored limits.
    """


@dataclass
class RechargeableBatteryLimits(EnergySourceLimits, AbsoluteElectricEnergyStorageLimitations):
    """
    Holds the limitations of a rechargeable battery.
    """
    absolute_limits: RechargeableBatteryAbsoluteLimits
    relative_limits: RechargeableBatteryRelativeLimits


@dataclass
class NonRechargeableBatteryLimits(EnergySourceLimits, AbsoluteElectricEnergyStorageLimitations):
    """
    Holds the limitations of a non rechargeable battery.
    """
    absolute_limits: NonRechargeableBatteryAbsoluteLimits
    relative_limits: NonRechargeableBatteryRelativeLimits


@dataclass
class ElectricMotorLimits(ConverterLimits):
    """
    Holds the limitations of an electric motor.
    """
    absolute_limits: ElectricMotorAbsoluteLimits
    relative_limits: ElectricMotorRelativeLimits


@dataclass
class LiquidCombustionEngineLimits(ConverterLimits):
    """
    Holds the limitations of a liquid fuel combustion engine.
    """
    absolute_limits: LiquidCombustionEngineAbsoluteLimits
    relative_limits: LiquidCombustionEngineRelativeLimits


@dataclass
class GaseousCombustionEngineLimits(ConverterLimits):
    """
    Holds the limitations of a gaseous fuel combustion engine.
    """
    absolute_limits: GaseousCombustionEngineAbsoluteLimits
    relative_limits: GaseousCombustionEngineRelativeLimits


@dataclass
class FuelCellLimits(ConverterLimits):
    """
    Holds the limitations of a fuel cell.
    """
    absolute_limits: FuelCellAbsoluteLimits
    relative_limits: FuelCellRelativeLimits


@dataclass
class ElectricGeneratorLimits(ConverterLimits):
    """
    Holds the limitations of an electric generator.
    """
    absolute_limits: ElectricGeneratorAbsoluteLimits
    relative_limits: ElectricGeneratorRelativeLimits


@dataclass
class MechanicalToMechanicalLimits(ConverterLimits):
    """
    Holds the limitations of a mechanical to
    mechanical converter (gears, etc).
    """
    absolute_limits: PureMechanicalAbsoluteLimits
    relative_limits: PureMechanicalRelativeLimits


@dataclass
class ElectricToElectricLimits(ConverterLimits):
    """
    Holds the limitations of an electric to
    electric converter (rectifier, inverter, etc).
    """
    absolute_limits: PureElectricAbsoluteLimits
    relative_limits: PureElectricRelativeLimits


@dataclass
class LiquidFuelTankLimits(EnergySourceLimits, AbsoluteLiquidFuelStorageLimitations):
    absolute_limits: LiquidFuelTankAbsoluteLimits


@dataclass
class GaseousFuelTankLimits(EnergySourceLimits, AbsoluteGaseousFuelStorageLimitations):
    absolute_limits: GaseousFuelTankAbsoluteLimits


# ==================
# CREATION FUNCTIONS
# ==================

def return_rechargeable_battery_limits(abs_max_temp: float, abs_min_temp: float,
                                       abs_max_power_in: float, abs_min_power_in: float,
                                       abs_max_power_out: float, abs_min_power_out: float,
                                       rel_max_temp: Callable, rel_min_temp: Callable,
                                       rel_max_power_in: Callable, rel_min_power_in: Callable,
                                       rel_max_power_out: Callable, rel_min_power_out: Callable,
                                       electric_energy_capacity: float) -> RechargeableBatteryLimits:
    return RechargeableBatteryLimits(absolute_limits=RechargeableBatteryAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                                           min=abs_min_temp)),
                                                                                       input=AbsoluteElectricLimitations(power=AbsoluteLimitValue(max=abs_max_power_in,
                                                                                                                                                  min=abs_min_power_in)),
                                                                                       output=AbsoluteElectricLimitations(power=AbsoluteLimitValue(max=abs_max_power_out,
                                                                                                                                                   min=abs_min_power_out))),
                                     relative_limits=RechargeableBatteryRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                           min=rel_min_temp)),
                                                                                       input=RelativeElectricLimitations(power=RelativeLimitValue(max=rel_max_power_in,
                                                                                                                                                  min=rel_min_power_in)),
                                                                                       output=RelativeElectricLimitations(power=RelativeLimitValue(max=rel_max_power_out,
                                                                                                                                                   min=rel_min_power_out))),
                                     electric_energy_capacity=electric_energy_capacity
                                     )

def return_non_rechargeable_battery_limits(abs_max_temp: float, abs_min_temp: float,
                                       abs_max_power_out: float, abs_min_power_out: float,
                                       rel_max_temp: Callable, rel_min_temp: Callable,
                                       rel_max_power_out: Callable, rel_min_power_out: Callable,
                                       electric_energy_capacity: float) -> NonRechargeableBatteryLimits:
    return NonRechargeableBatteryLimits(absolute_limits=NonRechargeableBatteryAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                                                 min=abs_min_temp)),
                                                                                             output=AbsoluteElectricLimitations(power=AbsoluteLimitValue(max=abs_max_power_out,
                                                                                                                                                         min=abs_min_power_out))),
                                        relative_limits=NonRechargeableBatteryRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                                 min=rel_min_temp)),
                                                                                             output=RelativeElectricLimitations(power=RelativeLimitValue(max=rel_max_power_out,
                                                                                                                                                         min=rel_min_power_out))),
                                        electric_energy_capacity=electric_energy_capacity
                                        )

def return_electric_motor_limits(abs_max_temp: float, abs_min_temp: float,
                                 abs_max_power_in: float, abs_min_power_in: float,
                                 abs_max_torque_out: float, abs_min_torque_out: float,
                                 abs_max_rpm_out: float, abs_min_rpm_out: float,
                                 rel_max_temp: Callable, rel_min_temp: Callable,
                                 rel_max_power_in: Callable, rel_min_power_in: Callable,
                                 rel_max_torque_out: Callable, rel_min_torque_out: Callable,
                                 rel_max_rpm_out: Callable, rel_min_rpm_out: Callable) -> ElectricMotorLimits:
    return ElectricMotorLimits(absolute_limits=ElectricMotorAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                               min=abs_min_temp)),
                                                                           input=AbsoluteElectricLimitations(power=AbsoluteLimitValue(max=abs_max_power_in,
                                                                                                                                      min=abs_min_power_in)),
                                                                           output=AbsoluteMechanicalLimitations(torque=AbsoluteLimitValue(max=abs_max_torque_out,
                                                                                                                                          min=abs_min_torque_out),
                                                                                                                rpm=AbsoluteLimitValue(max=abs_max_rpm_out,
                                                                                                                                       min=abs_min_rpm_out))),
                               relative_limits=ElectricMotorRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                               min=rel_min_temp)),
                                                                           input=RelativeElectricLimitations(power=RelativeLimitValue(max=rel_max_power_in,
                                                                                                                                      min=rel_min_power_in)),
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
                                                                                             input=AbsoluteLiquidFuelLimitations(fuel_liters_transfer=AbsoluteLimitValue(max=abs_max_fuel_liters_in,
                                                                                                                                                                         min=abs_min_fuel_liters_in)),
                                                                                             output=AbsoluteMechanicalLimitations(torque=AbsoluteLimitValue(max=abs_max_torque_out,
                                                                                                                                                            min=abs_min_torque_out),
                                                                                                                                  rpm=AbsoluteLimitValue(max=abs_max_rpm_out,
                                                                                                                                                         min=abs_min_rpm_out))),
                                        relative_limits=LiquidCombustionEngineRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                                 min=rel_min_temp)),
                                                                                             input=RelativeLiquidFuelLimitations(fuel_liters_transfer=RelativeLimitValue(max=rel_max_fuel_liters_in,
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
                                                                                               input=AbsoluteGaseousFuelLimitations(fuel_mass_transfer=AbsoluteLimitValue(max=abs_max_fuel_mass_in,
                                                                                                                                                                 min=abs_min_fuel_mass_in)),
                                                                                               output=AbsoluteMechanicalLimitations(torque=AbsoluteLimitValue(max=abs_max_torque_out,
                                                                                                                                                              min=abs_min_torque_out),
                                                                                                                                    rpm=AbsoluteLimitValue(max=abs_max_rpm_out,
                                                                                                                                                           min=abs_min_rpm_out))),
                                         relative_limits=GaseousCombustionEngineRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                                  min=rel_min_temp)),
                                                                                               input=RelativeGaseousFuelLimitations(fuel_mass_transfer=RelativeLimitValue(max=rel_max_fuel_mass_in,
                                                                                                                                                                 min=rel_min_fuel_mass_in)),
                                                                                               output=RelativeMechanicalLimitations(torque=RelativeLimitValue(max=rel_max_torque_out,
                                                                                                                                                              min=rel_min_torque_out),
                                                                                                                                    rpm=RelativeLimitValue(max=rel_max_rpm_out,
                                                                                                                                                           min=rel_min_rpm_out)))
                                         )

def return_fuel_cell_limits(abs_max_temp: float, abs_min_temp: float,
                            abs_max_fuel_mass_in: float, abs_min_fuel_mass_in: float,
                            abs_max_power_out: float, abs_min_power_out: float,
                            rel_max_temp: Callable, rel_min_temp: Callable,
                            rel_max_fuel_mass_in: Callable, rel_min_fuel_mass_in: Callable,
                            rel_max_power_out: Callable, rel_min_power_out: Callable) -> FuelCellLimits:
    return FuelCellLimits(absolute_limits=FuelCellAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                     min=abs_min_temp)),
                                                                 input=AbsoluteGaseousFuelLimitations(fuel_mass_transfer=AbsoluteLimitValue(max=abs_max_fuel_mass_in,
                                                                                                                                   min=abs_min_fuel_mass_in)),
                                                                 output=AbsoluteElectricLimitations(power=AbsoluteLimitValue(max=abs_max_power_out,
                                                                                                                             min=abs_min_power_out))),
                          relative_limits=FuelCellRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                     min=rel_min_temp)),
                                                                 input=RelativeGaseousFuelLimitations(fuel_mass_transfer=RelativeLimitValue(max=rel_max_fuel_mass_in,
                                                                                                                                   min=rel_min_fuel_mass_in)),
                                                                 output=RelativeElectricLimitations(power=RelativeLimitValue(max=rel_max_power_out,
                                                                                                                             min=rel_min_power_out)))
                          )

def return_electric_generator_limits(abs_max_temp: float, abs_min_temp: float,
                                     abs_max_torque_in: float, abs_min_torque_in: float,
                                     abs_max_rpm_in: float, abs_min_rpm_in: float,
                                     abs_max_power_out: float, abs_min_power_out: float,
                                     rel_max_temp: Callable, rel_min_temp: Callable,
                                     rel_max_torque_in: Callable, rel_min_torque_in: Callable,
                                     rel_max_rpm_in: Callable, rel_min_rpm_in: Callable,
                                     rel_max_power_out: Callable, rel_min_power_out: Callable) -> ElectricGeneratorLimits:
    return ElectricGeneratorLimits(absolute_limits=ElectricGeneratorAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                                       min=abs_min_temp)),
                                                                                   input=AbsoluteMechanicalLimitations(torque=AbsoluteLimitValue(max=abs_max_torque_in,
                                                                                                                                                 min=abs_min_torque_in),
                                                                                                                       rpm=AbsoluteLimitValue(max=abs_max_rpm_in,
                                                                                                                                              min=abs_min_rpm_in)),
                                                                                   output=AbsoluteElectricLimitations(power=AbsoluteLimitValue(max=abs_max_power_out,
                                                                                                                                               min=abs_min_power_out))),
                                   relative_limits=ElectricGeneratorRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                       min=rel_min_temp)),
                                                                                   input=RelativeMechanicalLimitations(torque=RelativeLimitValue(max=rel_max_torque_in,
                                                                                                                                                 min=rel_min_torque_in),
                                                                                                                       rpm=RelativeLimitValue(max=rel_max_rpm_in,
                                                                                                                                              min=rel_min_rpm_in)),
                                                                                   output=RelativeElectricLimitations(power=RelativeLimitValue(max=rel_max_power_out,
                                                                                                                                               min=rel_min_power_out)))
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
                                       abs_max_power_in: float, abs_min_power_in: float,
                                       abs_max_power_out: float, abs_min_power_out: float,
                                       rel_max_temp: Callable, rel_min_temp: Callable,
                                       rel_max_power_in: Callable, rel_min_power_in: Callable,
                                       rel_max_power_out: Callable, rel_min_power_out: Callable) -> ElectricToElectricLimits:
    return ElectricToElectricLimits(absolute_limits=PureElectricAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temp,
                                                                                                                                                   min=abs_min_temp)),
                                                                               input=AbsoluteElectricLimitations(power=AbsoluteLimitValue(max=abs_max_power_in,
                                                                                                                                          min=abs_min_power_in)),
                                                                               output=AbsoluteElectricLimitations(power=AbsoluteLimitValue(max=abs_max_power_out,
                                                                                                                                           min=abs_min_power_out))),
                                    relative_limits=PureElectricRelativeLimits(internal=RelativeInternalLimitations(temperature=RelativeLimitValue(max=rel_max_temp,
                                                                                                                                                   min=rel_min_temp)),
                                                                               input=RelativeElectricLimitations(power=RelativeLimitValue(max=rel_max_power_in,
                                                                                                                                          min=rel_min_power_in)),
                                                                               output=RelativeElectricLimitations(power=RelativeLimitValue(max=rel_max_power_out,
                                                                                                                                           min=rel_min_power_out)))
                                    )

def return_liquid_fuel_tank_limits(abs_max_temperature: float, abs_min_temperature: float,
                                   abs_max_fuel_liters_transfer: float, abs_min_fuel_liters_transfer: float,
                                   fuel_liters_capacity: float) -> LiquidFuelTankLimits:
    return LiquidFuelTankLimits(absolute_limits=LiquidFuelTankAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temperature,
                                                                                                                                                 min=abs_min_temperature)),
                                                                             output=AbsoluteLiquidFuelLimitations(fuel_liters_transfer=AbsoluteLimitValue(max=abs_max_fuel_liters_transfer,
                                                                                                                                                          min=abs_min_fuel_liters_transfer))),
                                fuel_liters_capacity=fuel_liters_capacity
                                )

def return_gaseous_fuel_tank_limits(abs_max_temperature: float, abs_min_temperature: float,
                                    abs_max_fuel_mass_transfer: float, abs_min_fuel_mass_transfer: float,
                                    fuel_mass_capacity: float) -> GaseousFuelTankLimits:
    return GaseousFuelTankLimits(absolute_limits=GaseousFuelTankAbsoluteLimits(internal=AbsoluteInternalLimitations(temperature=AbsoluteLimitValue(max=abs_max_temperature,
                                                                                                                                                   min=abs_min_temperature)),
                                                                               output=AbsoluteGaseousFuelLimitations(fuel_mass_transfer=AbsoluteLimitValue(max=abs_max_fuel_mass_transfer,
                                                                                                                                                           min=abs_min_fuel_mass_transfer))),
                                 fuel_mass_capacity=fuel_mass_capacity
                                )
