"""This module contains routines for managing
energy and fuel consumption for all components."""

from typing import Callable, TypeVar, Generic
from dataclasses import dataclass
from components.state import FullStateNoInput, FullStateWithInput, \
    RechargeableBatteryState, NonRechargeableBatteryState, \
    ElectricMotorState, ElectricGeneratorState, \
    LiquidCombustionEngineState, GaseousCombustionEngineState, \
    LiquidFuelTankState, GaseousFuelTankState, FuelCellState, \
    PureElectricState, PureMechanicalState
from helpers.functions import assert_type, assert_type_and_range, assert_callable


# ============
# BASE CLASSES
# ============

InternalToOutState = TypeVar("InternalToOutState",
                             bound=RechargeableBatteryState|NonRechargeableBatteryState)
InOutState = TypeVar("InOutState",
                     bound=FullStateWithInput)
FuelTankState = TypeVar("FuelTankState",
                        bound=LiquidFuelTankState|GaseousFuelTankState)
InFuelState = TypeVar("InFuelState",
                      bound=LiquidCombustionEngineState|
                            GaseousCombustionEngineState|
                            FuelCellState)


@dataclass
class InternalToOutEnergyConsumption(Generic[InternalToOutState]):
    """
    Base class for modeling internal energy
    consumption of a component.
    Applies to components that store their
    own energy (batteries and others).
    """
    internal_to_out_efficiency_func: Callable[[InternalToOutState], float]

    def __post_init__(self):
        assert_callable(self.internal_to_out_efficiency_func)

    def compute_internal_to_out(self, state: InternalToOutState,
                                delta_t: float) -> float:
        """
        Calculates energy consumption from internal
        source being delivered to the output.
        """
        assert_type(state,
                    expected_type=(RechargeableBatteryState, NonRechargeableBatteryState))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.output.set_receiving()
        return state.output.power * delta_t / self.internal_to_out_efficiency_value(state=state)

    def internal_to_out_efficiency_value(self, state: InternalToOutState) -> float:
        """
        Returns the efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=(FullStateNoInput, FullStateWithInput))
        return self.internal_to_out_efficiency_func(state)


@dataclass
class OutToInternalEnergyConsumption():
    """
    Base class for modeling internal reversible
    energy consumption from a component.
    Applies to components that store their
    own energy (batteries and others).
    """
    out_to_internal_efficiency_func: Callable[[RechargeableBatteryState], float]

    def __post_init__(self):
        assert_callable(self.out_to_internal_efficiency_func)

    def compute_out_to_internal(self, state: RechargeableBatteryState,
                                delta_t: float) -> float:
        """
        Calculates reverse energy consumption from the
        output being delivered to the internal source.
        """
        assert_type(state,
                    expected_type=RechargeableBatteryState)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.output.set_delivering()
        return state.output.power * delta_t * self.out_to_internal_efficiency_value(state=state)

    def out_to_internal_efficiency_value(self, state: RechargeableBatteryState) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=RechargeableBatteryState)
        return self.out_to_internal_efficiency_func(state)


@dataclass
class InToInternalEnergyConsumption():
    """
    """
    in_to_internal_efficiency_func: Callable[[RechargeableBatteryState], float]

    def __post_init__(self):
        assert_callable(self.in_to_internal_efficiency_func)

    def compute_in_to_internal(self, state: RechargeableBatteryState,
                               delta_t: float) -> float:
        """
        Computes the energy consumption
        from the input to internal storage.
        """
        assert_type(state,
                    expected_type=RechargeableBatteryState)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.input.set_delivering()
        return state.input.power * delta_t * self.in_to_internal_efficiency_value(state=state)

    def in_to_internal_efficiency_value(self, state: RechargeableBatteryState) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=RechargeableBatteryState)
        return self.in_to_internal_efficiency_func(state)


@dataclass
class InternalToInEnergyConsumption():
    """
    """
    internal_to_in_efficiency_func: Callable[[RechargeableBatteryState], float]

    def __post_init__(self):
        assert_callable(self.internal_to_in_efficiency_func)

    def compute_internal_to_in(self, state: RechargeableBatteryState,
                               delta_t: float) -> float:
        """
        Computes the energy consumption from
        the internal storage to the input.
        """
        assert_type(state,
                    expected_type=RechargeableBatteryState)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.input.set_receiving()
        return state.input.power * delta_t / self.internal_to_in_efficiency_value(state=state)

    def internal_to_in_efficiency_value(self, state: RechargeableBatteryState) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=RechargeableBatteryState)
        return self.internal_to_in_efficiency_func(state)


@dataclass
class InToOutEnergyConsumption(Generic[InOutState]):
    """
    """
    in_to_out_efficiency_func: Callable[[InOutState], float]

    def __post_init__(self):
        assert_callable(self.in_to_out_efficiency_func)

    def compute_in_to_out(self, state: InOutState,
                          delta_t: float) -> float:
        """
        Computes the energy consumption
        from the input to the output.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.input.set_delivering()
        state.output.set_receiving()
        return state.output.power * delta_t / self.in_to_out_efficiency_value(state=state)

    def in_to_out_efficiency_value(self, state: InOutState) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        return self.in_to_out_efficiency_func(state)


@dataclass
class OutToInEnergyConsumption(Generic[InOutState]):
    """
    """
    out_to_in_efficiency_func: Callable[[InOutState], float]

    def __post_init__(self):
        assert_callable(self.out_to_in_efficiency_func)

    def compute_out_to_in(self, state: InOutState,
                          delta_t: float) -> float:
        """
        Computes the energy consumption
        from the output to the input.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.input.set_receiving()
        state.output.set_delivering()
        return state.input.power * delta_t / self.out_to_in_efficiency_value(state=state)

    def out_to_in_efficiency_value(self, state: InOutState) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        return self.out_to_in_efficiency_func(state)


@dataclass
class InternalToOutFuelConsumption(Generic[FuelTankState]):
    """
    """
    internal_to_out_fuel_consumption_func: Callable[[FuelTankState], float]

    def __post_init__(self):
        assert_callable(self.internal_to_out_fuel_consumption_func)

    def compute_internal_to_out(self, state: FuelTankState,
                                delta_t: float):
        """
        Calculates the fuel transfered from
        internal storage to the output.
        """
        assert_type(state,
                    expected_type=(LiquidFuelTankState, GaseousFuelTankState))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.output.set_receiving()
        return self.internal_to_out_fuel_consumption_value(state) * delta_t

    def internal_to_out_fuel_consumption_value(self, state: FuelTankState) -> float:
        """
        Returns the marginal fuel consumption at a given state.
        """
        assert_type(state,
                    expected_type=(LiquidFuelTankState, GaseousFuelTankState))
        return self.internal_to_out_fuel_consumption_func(state)


@dataclass
class InToOutFuelConsumption(Generic[InFuelState]):
    """
    """
    in_to_out_fuel_consumption_func: Callable[[InFuelState], float]

    def __post_init__(self):
        assert_callable(self.in_to_out_fuel_consumption_func)

    def compute_in_to_out(self, state: InFuelState,
                          delta_t: float):
        """
        Calculates the fuel consumed
        from input to generate an output.
        """
        assert_type(state,
                    expected_type=(LiquidCombustionEngineState,
                                   GaseousCombustionEngineState,
                                   FuelCellState))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.output.set_receiving()
        return self.in_to_out_fuel_consumption_value(state) * delta_t

    def in_to_out_fuel_consumption_value(self, state: InFuelState) -> float:
        """
        Returns the marginal fuel consumption at a given state.
        """
        assert_type(state,
                    expected_type=(LiquidCombustionEngineState,
                                   GaseousCombustionEngineState,
                                   FuelCellState))
        return self.in_to_out_fuel_consumption_func(state)


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
                                     InternalToOutEnergyConsumption["RechargeableBatteryState"],
                                     OutToInternalEnergyConsumption,
                                     InternalToInEnergyConsumption,
                                     InToInternalEnergyConsumption):
    """
    Models energy consumption in a rechargeable battery.
    """


@dataclass
class NonRechargeableBatteryConsumption(BaseBattery,
                                        InternalToOutEnergyConsumption["NonRechargeableBatteryState"]):
    """
    Models energy consumption in a non rechargeable battery.
    """


@dataclass
class ElectricMotorConsumption(ConverterConsumption,
                               InToOutEnergyConsumption["ElectricMotorState"],
                               OutToInEnergyConsumption["ElectricMotorState"]):
    """
    Models energy consumption in a reversible electric motor.
    """


@dataclass
class ElectricGeneratorConsumption(ConverterConsumption,
                                   InToOutEnergyConsumption["ElectricGeneratorState"]):
    """
    Models energy consumption in an irreversible electric generator.
    """


@dataclass
class LiquidCombustionEngineConsumption(ConverterConsumption,
                                        InToOutFuelConsumption["LiquidCombustionEngineState"]):
    """
    Models fuel consumption in a liquid combustion engine.
    """


@dataclass
class GaseousCombustionEngineConsumption(ConverterConsumption,
                                         InToOutFuelConsumption["GaseousCombustionEngineState"]):
    """
    Models fuel consumption in a gaseous combustion engine.
    """


@dataclass
class FuelCellConsumption(ConverterConsumption,
                          InToOutFuelConsumption["FuelCellState"]):
    """
    Models consumption in a fuel cell.
    """


@dataclass
class PureMechanicalConsumption(ConverterConsumption,
                                InToOutEnergyConsumption["PureMechanicalState"],
                                OutToInEnergyConsumption["PureMechanicalState"]):
    """
    Models consumption in a reversible
    mechanical-to-mechanical component
    (gears, etc).
    """


@dataclass
class PureElectricConsumption(ConverterConsumption,
                              InToOutEnergyConsumption["PureElectricState"]):
    """
    Models consumption in a non reversible
    electric-to-electric component (rectifiers,
    inverters, etc).
    """


@dataclass
class LiquidFuelTankConsumption(EnergySourceConsumption,
                                InternalToOutFuelConsumption["LiquidFuelTankState"]):
    """
    Models the fuel consumption in a fuel tank.
    """


@dataclass
class GaseousFuelTankConsumption(EnergySourceConsumption,
                                 InternalToOutFuelConsumption["GaseousFuelTankState"]):
    """
    Models the fuel consumption in a fuel tank.
    """


# ========
# CREATORS
# ========

def return_rechargeable_battery_consumption(
        discharge_efficiency_func: Callable[
            [RechargeableBatteryState], float],
        recharge_efficiency_func: Callable[
            [RechargeableBatteryState], float]
        ) -> RechargeableBatteryConsumption:
    return RechargeableBatteryConsumption(
        in_to_internal_efficiency_func=recharge_efficiency_func,
        internal_to_in_efficiency_func=discharge_efficiency_func,
        out_to_internal_efficiency_func=recharge_efficiency_func,
        internal_to_out_efficiency_func=discharge_efficiency_func
    )

def return_non_rechargeable_battery_consumption(
        discharge_efficiency_func: Callable[
            [NonRechargeableBatteryState], float],
        ) -> NonRechargeableBatteryConsumption:
    return NonRechargeableBatteryConsumption(
        internal_to_out_efficiency_func=discharge_efficiency_func
    )

def return_electric_motor_consumption(
        motor_efficiency_func: Callable[[ElectricMotorState], float],
        generator_efficiency_func: Callable[[ElectricMotorState], float]
        ) -> ElectricMotorConsumption:
    return ElectricMotorConsumption(
        in_to_out_efficiency_func=motor_efficiency_func,
        out_to_in_efficiency_func=generator_efficiency_func,
    )

def return_electric_generator_consumption(
        generator_efficiency_func: Callable[[ElectricGeneratorState], float]
        ) -> ElectricGeneratorConsumption:
    return ElectricGeneratorConsumption(
        in_to_out_efficiency_func=generator_efficiency_func
    )

def return_liquid_combustion_engine_consumption(
        fuel_consumption_func: Callable[[LiquidCombustionEngineState], float]
        ) -> LiquidCombustionEngineConsumption:
    return LiquidCombustionEngineConsumption(
        in_to_out_fuel_consumption_func=fuel_consumption_func
    )

def return_gaseous_combustion_engine_consumption(
        fuel_consumption_func: Callable[[GaseousCombustionEngineState], float]
        ) -> GaseousCombustionEngineConsumption:
    return GaseousCombustionEngineConsumption(
        in_to_out_fuel_consumption_func=fuel_consumption_func
    )

def return_fuel_cell_consumption(
        fuel_consumption_func: Callable[[FuelCellState], float]
        ) -> FuelCellConsumption:
    return FuelCellConsumption(
        in_to_out_fuel_consumption_func=fuel_consumption_func
    )

def return_pure_mechanical_consumption(
        efficiency_func: Callable[[PureMechanicalState], float],
        reverse_efficiency_func: Callable[[PureMechanicalState], float]
        ) -> PureMechanicalConsumption:
    return PureMechanicalConsumption(
        in_to_out_efficiency_func=efficiency_func,
        out_to_in_efficiency_func=reverse_efficiency_func
    )

def return_pure_electric_consumption(
    efficiency_func: Callable[[PureElectricState], float]
    ) -> PureElectricConsumption:
    return PureElectricConsumption(
        in_to_out_efficiency_func=efficiency_func
    )

def return_liquid_fuel_tank_consumption(
    fuel_consumption_func: Callable[[LiquidFuelTankState], float]
    ) -> LiquidFuelTankConsumption:
    return LiquidFuelTankConsumption(
        internal_to_out_fuel_consumption_func=fuel_consumption_func
    )

def return_gaseous_fuel_tank_consumption(
    fuel_consumption_func: Callable[[GaseousFuelTankState], float]
    ) -> GaseousFuelTankConsumption:
    return GaseousFuelTankConsumption(
        internal_to_out_fuel_consumption_func=fuel_consumption_func
    )
