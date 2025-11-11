"""This module contains routines for managing
energy and fuel consumption for all components."""

from typing import Callable, TypeVar, Generic
from dataclasses import dataclass
from components.component_snapshot import EnergySourceSnapshot, \
    RechargeableBatterySnapshot, NonRechargeableBatterySnapshot, \
    ConverterSnapshot, \
    LiquidCombustionEngineSnapshot, GaseousCombustionEngineSnapshot, \
    FuelCellSnapshot, LiquidFuelTankSnapshot, GaseousFuelTankSnapshot, \
    ElectricMotorSnapshot, ElectricGeneratorSnapshot, \
    GearBoxSnapshot, ElectricInverterSnapshot, ElectricRectifierSnapshot
from helpers.functions import assert_type, assert_type_and_range, assert_callable


# ============
# BASE CLASSES
# ============

InternalToOutSnapshot = TypeVar("InternalToOutSnapshot",
                                bound=RechargeableBatterySnapshot|NonRechargeableBatterySnapshot)
InOutSnapshot = TypeVar("InOutSnapshot",
                        bound=ConverterSnapshot|EnergySourceSnapshot)
FuelTankSnapshot = TypeVar("FuelTankSnapshot",
                           bound=LiquidFuelTankSnapshot|GaseousFuelTankSnapshot)
InFuelSnapshot = TypeVar("InFuelSnapshot",
                         bound=LiquidCombustionEngineSnapshot|
                               GaseousCombustionEngineSnapshot|
                               FuelCellSnapshot)


@dataclass
class InternalToOutEnergyConsumption(Generic[InternalToOutSnapshot]):
    """
    Base class for modeling internal energy
    consumption of a component.
    Applies to components that store their
    own energy (batteries and others).
    """
    internal_to_out_efficiency_func: Callable[[InternalToOutSnapshot], float]

    def __post_init__(self):
        assert_callable(self.internal_to_out_efficiency_func)

    def compute_internal_to_out(self, snap: InternalToOutSnapshot,
                                delta_t: float) -> float:
        """
        Calculates energy consumption from internal
        source being delivered to the output.
        """
        assert_type(snap,
                    expected_type=(RechargeableBatterySnapshot, NonRechargeableBatterySnapshot))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        return snap.power_out * delta_t / self.internal_to_out_efficiency_value(snap=snap)

    def internal_to_out_efficiency_value(self, snap: InternalToOutSnapshot) -> float:
        """
        Returns the efficiency value at a given state.
        """
        assert_type(snap,
                    expected_type=(RechargeableBatterySnapshot, NonRechargeableBatterySnapshot))
        return self.internal_to_out_efficiency_func(snap)


@dataclass
class OutToInternalEnergyConsumption():
    """
    Base class for modeling internal reversible
    energy consumption from a component.
    Applies to components that store their
    own energy (batteries and others).
    """
    out_to_internal_efficiency_func: Callable[[RechargeableBatterySnapshot], float]

    def __post_init__(self):
        assert_callable(self.out_to_internal_efficiency_func)

    def compute_out_to_internal(self, snap: RechargeableBatterySnapshot,
                                delta_t: float) -> float:
        """
        Calculates reverse energy consumption from the
        output being delivered to the internal source.
        """
        assert_type(snap,
                    expected_type=RechargeableBatterySnapshot)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        return snap.power_out * delta_t * self.out_to_internal_efficiency_value(snap=snap)

    def out_to_internal_efficiency_value(self, snap: RechargeableBatterySnapshot) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(snap,
                    expected_type=RechargeableBatterySnapshot)
        return self.out_to_internal_efficiency_func(snap)


@dataclass
class InToInternalEnergyConsumption():
    """
    """
    in_to_internal_efficiency_func: Callable[[RechargeableBatterySnapshot], float]

    def __post_init__(self):
        assert_callable(self.in_to_internal_efficiency_func)

    def compute_in_to_internal(self, snap: RechargeableBatterySnapshot,
                               delta_t: float) -> float:
        """
        Computes the energy consumption
        from the input to internal storage.
        """
        assert_type(snap,
                    expected_type=RechargeableBatterySnapshot)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        return snap.power_in * delta_t * self.in_to_internal_efficiency_value(snap=snap)

    def in_to_internal_efficiency_value(self, snap: RechargeableBatterySnapshot) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(snap,
                    expected_type=RechargeableBatterySnapshot)
        return self.in_to_internal_efficiency_func(snap)


@dataclass
class InternalToInEnergyConsumption():
    """
    """
    internal_to_in_efficiency_func: Callable[[RechargeableBatterySnapshot], float]

    def __post_init__(self):
        assert_callable(self.internal_to_in_efficiency_func)

    def compute_internal_to_in(self, snap: RechargeableBatterySnapshot,
                               delta_t: float) -> float:
        """
        Computes the energy consumption from
        the internal storage to the input.
        """
        assert_type(snap,
                    expected_type=RechargeableBatterySnapshot)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        return snap.power_in * delta_t / self.internal_to_in_efficiency_value(snap=snap)

    def internal_to_in_efficiency_value(self, snap: RechargeableBatterySnapshot) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(snap,
                    expected_type=RechargeableBatterySnapshot)
        return self.internal_to_in_efficiency_func(snap)


@dataclass
class InToOutEnergyConsumption(Generic[InOutSnapshot]):
    """
    """
    in_to_out_efficiency_func: Callable[[InOutSnapshot], float]

    def __post_init__(self):
        assert_callable(self.in_to_out_efficiency_func)

    def compute_in_to_out(self, snap: InOutSnapshot,
                          delta_t: float) -> float:
        """
        Computes the energy consumption
        from the input to the output.
        """
        assert_type(snap,
                    expected_type=(ConverterSnapshot, EnergySourceSnapshot))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        if isinstance(snap, ConverterSnapshot):
            power = snap.applied_power_out
        else:
            power = snap.power_out
        return power * delta_t / self.in_to_out_efficiency_value(snap=snap)

    def in_to_out_efficiency_value(self, snap: InOutSnapshot) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(snap,
                    expected_type=(ConverterSnapshot, EnergySourceSnapshot))
        return self.in_to_out_efficiency_func(snap)


@dataclass
class OutToInEnergyConsumption(Generic[InOutSnapshot]):
    """
    """
    out_to_in_efficiency_func: Callable[[InOutSnapshot], float]

    def __post_init__(self):
        assert_callable(self.out_to_in_efficiency_func)

    def compute_out_to_in(self, snap: InOutSnapshot,
                          delta_t: float) -> float:
        """
        Computes the energy consumption
        from the output to the input.
        """
        assert_type(snap,
                    expected_type=(ConverterSnapshot, EnergySourceSnapshot))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        return snap.power_in * delta_t / self.out_to_in_efficiency_value(snap=snap)

    def out_to_in_efficiency_value(self, snap: InOutSnapshot) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(snap,
                    expected_type=(ConverterSnapshot, EnergySourceSnapshot))
        return self.out_to_in_efficiency_func(snap)


@dataclass
class InternalToOutFuelConsumption(Generic[FuelTankSnapshot]):
    """
    """
    internal_to_out_fuel_consumption_func: Callable[[FuelTankSnapshot], float]

    def __post_init__(self):
        assert_callable(self.internal_to_out_fuel_consumption_func)

    def compute_internal_to_out(self, snap: FuelTankSnapshot,
                                delta_t: float):
        """
        Calculates the fuel transfered from
        internal storage to the output.
        """
        assert_type(snap,
                    expected_type=(LiquidFuelTankSnapshot, GaseousFuelTankSnapshot))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        return self.internal_to_out_fuel_consumption_value(snap) * delta_t

    def internal_to_out_fuel_consumption_value(self, snap: FuelTankSnapshot) -> float:
        """
        Returns the marginal fuel consumption at a given state.
        """
        assert_type(snap,
                    expected_type=(LiquidFuelTankSnapshot, GaseousFuelTankSnapshot))
        return self.internal_to_out_fuel_consumption_func(snap)


@dataclass
class InToOutFuelConsumption(Generic[InFuelSnapshot]):
    """
    """
    in_to_out_fuel_consumption_func: Callable[[InFuelSnapshot], float]

    def __post_init__(self):
        assert_callable(self.in_to_out_fuel_consumption_func)

    def compute_in_to_out(self, snap: InFuelSnapshot,
                          delta_t: float):
        """
        Calculates the fuel consumed
        from input to generate an output.
        """
        assert_type(snap,
                    expected_type=(LiquidCombustionEngineSnapshot,
                                   GaseousCombustionEngineSnapshot,
                                   FuelCellSnapshot))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        return self.in_to_out_fuel_consumption_value(snap) * delta_t

    def in_to_out_fuel_consumption_value(self, snap: InFuelSnapshot) -> float:
        """
        Returns the marginal fuel consumption at a given state.
        """
        assert_type(snap,
                    expected_type=(LiquidCombustionEngineSnapshot,
                                   GaseousCombustionEngineSnapshot,
                                   FuelCellSnapshot))
        return self.in_to_out_fuel_consumption_func(snap)


# ================
# TAILORED CLASSES
# ================


@dataclass
class EnergySourceConsumption():
    """
    Placeholder for energy sources' tailored consumption classes.
    """


@dataclass
class ConverterConsumption():
    """
    Placeholder for converters' tailored consumption classes.
    """


@dataclass
class BaseBattery(EnergySourceConsumption):
    """
    Base class for battery consumption types.
    """


@dataclass
class RechargeableBatteryConsumption(BaseBattery,
                                     InternalToOutEnergyConsumption["RechargeableBatterySnapshot"],
                                     OutToInternalEnergyConsumption,
                                     InternalToInEnergyConsumption,
                                     InToInternalEnergyConsumption):
    """
    Models energy consumption in a rechargeable battery.
    """


@dataclass
class NonRechargeableBatteryConsumption(BaseBattery,
                                        InternalToOutEnergyConsumption["NonRechargeableBatterySnapshot"]):
    """
    Models energy consumption in a non rechargeable battery.
    """


@dataclass
class ElectricMotorConsumption(ConverterConsumption,
                               InToOutEnergyConsumption["ElectricMotorSnapshot"],
                               OutToInEnergyConsumption["ElectricMotorSnapshot"]):
    """
    Models energy consumption in a reversible electric motor.
    """


@dataclass
class ElectricGeneratorConsumption(ConverterConsumption,
                                   InToOutEnergyConsumption["ElectricGeneratorSnapshot"]):
    """
    Models energy consumption in an irreversible electric generator.
    """


@dataclass
class LiquidCombustionEngineConsumption(ConverterConsumption,
                                        InToOutFuelConsumption["LiquidCombustionEngineSnapshot"]):
    """
    Models fuel consumption in a liquid combustion engine.
    """


@dataclass
class GaseousCombustionEngineConsumption(ConverterConsumption,
                                         InToOutFuelConsumption["GaseousCombustionEngineSnapshot"]):
    """
    Models fuel consumption in a gaseous combustion engine.
    """


@dataclass
class FuelCellConsumption(ConverterConsumption,
                          InToOutFuelConsumption["FuelCellSnapshot"]):
    """
    Models consumption in a fuel cell.
    """


@dataclass
class GearBoxConsumption(ConverterConsumption,
                         InToOutEnergyConsumption["GearBoxSnapshot"],
                         OutToInEnergyConsumption["GearBoxSnapshot"]):
    """
    Models consumption in a reversible
    mechanical-to-mechanical component
    (gears, etc).
    """


@dataclass
class ElectricInverterConsumption(ConverterConsumption,
                                  InToOutEnergyConsumption["ElectricInverterSnapshot"]):
    """
    Models consumption in an
    irreversible electric inverter.
    """


@dataclass
class ElectricRectifierConsumption(ConverterConsumption,
                                   InToOutEnergyConsumption["ElectricRectifierSnapshot"]):
    """
    Models consumption in an
    irreversible electric rectifier.
    """


@dataclass
class LiquidFuelTankConsumption(EnergySourceConsumption,
                                InternalToOutFuelConsumption["LiquidFuelTankSnapshot"]):
    """
    Models the fuel consumption in a fuel tank.
    """


@dataclass
class GaseousFuelTankConsumption(EnergySourceConsumption,
                                 InternalToOutFuelConsumption["GaseousFuelTankSnapshot"]):
    """
    Models the fuel consumption in a fuel tank.
    """


# ========
# CREATORS
# ========

def return_rechargeable_battery_consumption(
        discharge_efficiency_func: Callable[
            [RechargeableBatterySnapshot], float],
        recharge_efficiency_func: Callable[
            [RechargeableBatterySnapshot], float]
        ) -> RechargeableBatteryConsumption:
    return RechargeableBatteryConsumption(
        in_to_internal_efficiency_func=recharge_efficiency_func,
        internal_to_in_efficiency_func=discharge_efficiency_func,
        out_to_internal_efficiency_func=recharge_efficiency_func,
        internal_to_out_efficiency_func=discharge_efficiency_func
    )

def return_non_rechargeable_battery_consumption(
        discharge_efficiency_func: Callable[
            [NonRechargeableBatterySnapshot], float],
        ) -> NonRechargeableBatteryConsumption:
    return NonRechargeableBatteryConsumption(
        internal_to_out_efficiency_func=discharge_efficiency_func
    )

def return_electric_motor_consumption(
        motor_efficiency_func: Callable[[ElectricMotorSnapshot], float],
        generator_efficiency_func: Callable[[ElectricMotorSnapshot], float]
        ) -> ElectricMotorConsumption:
    return ElectricMotorConsumption(
        in_to_out_efficiency_func=motor_efficiency_func,
        out_to_in_efficiency_func=generator_efficiency_func,
    )

def return_electric_generator_consumption(
        generator_efficiency_func: Callable[[ElectricGeneratorSnapshot], float]
        ) -> ElectricGeneratorConsumption:
    return ElectricGeneratorConsumption(
        in_to_out_efficiency_func=generator_efficiency_func
    )

def return_liquid_combustion_engine_consumption(
        fuel_consumption_func: Callable[[LiquidCombustionEngineSnapshot], float]
        ) -> LiquidCombustionEngineConsumption:
    return LiquidCombustionEngineConsumption(
        in_to_out_fuel_consumption_func=fuel_consumption_func
    )

def return_gaseous_combustion_engine_consumption(
        fuel_consumption_func: Callable[[GaseousCombustionEngineSnapshot], float]
        ) -> GaseousCombustionEngineConsumption:
    return GaseousCombustionEngineConsumption(
        in_to_out_fuel_consumption_func=fuel_consumption_func
    )

def return_fuel_cell_consumption(
        fuel_consumption_func: Callable[[FuelCellSnapshot], float]
        ) -> FuelCellConsumption:
    return FuelCellConsumption(
        in_to_out_fuel_consumption_func=fuel_consumption_func
    )

def return_gearbox_consumption(
        efficiency_func: Callable[[GearBoxSnapshot], float],
        reverse_efficiency_func: Callable[[GearBoxSnapshot], float]
        ) -> GearBoxConsumption:
    return GearBoxConsumption(
        in_to_out_efficiency_func=efficiency_func,
        out_to_in_efficiency_func=reverse_efficiency_func
    )

def return_electric_inverter_consumption(
    efficiency_func: Callable[[ElectricInverterSnapshot], float]
    ) -> ElectricInverterConsumption:
    return ElectricInverterConsumption(
        in_to_out_efficiency_func=efficiency_func
    )

def return_electric_rectifier_consumption(
    efficiency_func: Callable[[ElectricRectifierSnapshot], float]
    ) -> ElectricRectifierConsumption:
    return ElectricRectifierConsumption(
        in_to_out_efficiency_func=efficiency_func
    )

def return_liquid_fuel_tank_consumption(
    fuel_consumption_func: Callable[[LiquidFuelTankSnapshot], float]
    ) -> LiquidFuelTankConsumption:
    return LiquidFuelTankConsumption(
        internal_to_out_fuel_consumption_func=fuel_consumption_func
    )

def return_gaseous_fuel_tank_consumption(
    fuel_consumption_func: Callable[[GaseousFuelTankSnapshot], float]
    ) -> GaseousFuelTankConsumption:
    return GaseousFuelTankConsumption(
        internal_to_out_fuel_consumption_func=fuel_consumption_func
    )
