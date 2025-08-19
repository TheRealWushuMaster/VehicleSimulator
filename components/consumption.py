"""This module contains routines for managing
energy and fuel consumption for all components."""

from typing import Callable
from dataclasses import dataclass
from components.state import FullStateNoInput, FullStateWithInput
from helpers.functions import assert_type, assert_type_and_range, assert_callable


# ============
# BASE CLASSES
# ============


@dataclass
class InternalToOutEnergyConsumption():
    """
    Base class for modeling internal energy
    consumption of a component.
    Applies to components that store their
    own energy (batteries and others).
    """
    internal_to_out_efficiency_func: Callable[[FullStateNoInput|FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.internal_to_out_efficiency_func)

    def compute_internal_to_out(self, state: FullStateNoInput|FullStateWithInput,
                                delta_t: float) -> float:
        """
        Calculates energy consumption from internal
        source being delivered to the output.
        """
        assert_type(state,
                    expected_type=(FullStateNoInput, FullStateWithInput))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.output.set_receiving()
        return state.output.power * delta_t / self.internal_to_out_efficiency_value(state=state)

    def internal_to_out_efficiency_value(self, state: FullStateNoInput|FullStateWithInput) -> float:
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
    out_to_internal_efficiency_func: Callable[[FullStateNoInput|FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.out_to_internal_efficiency_func)

    def compute_out_to_internal(self, state: FullStateNoInput|FullStateWithInput,
                                delta_t: float) -> float:
        """
        Calculates reverse energy consumption from the
        output being delivered to the internal source.
        """
        assert_type(state,
                    expected_type=(FullStateNoInput, FullStateWithInput))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.output.set_delivering()
        return state.output.power * delta_t * self.out_to_internal_efficiency_value(state=state)

    def out_to_internal_efficiency_value(self, state: FullStateNoInput|FullStateWithInput) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=(FullStateNoInput, FullStateWithInput))
        return self.out_to_internal_efficiency_func(state)


@dataclass
class InToInternalEnergyConsumption():
    """
    """
    in_to_internal_efficiency_func: Callable[[FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.in_to_internal_efficiency_func)

    def compute_in_to_internal(self, state: FullStateWithInput,
                               delta_t: float) -> float:
        """
        Computes the energy consumption
        from the input to internal storage.
        """
        assert_type(state,
                    expected_type=(FullStateWithInput))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.input.set_delivering()
        return state.input.power * delta_t * self.in_to_internal_efficiency_value(state=state)

    def in_to_internal_efficiency_value(self, state: FullStateWithInput) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=(FullStateNoInput, FullStateWithInput))
        return self.in_to_internal_efficiency_func(state)


@dataclass
class InternalToInEnergyConsumption():
    """
    """
    internal_to_in_efficiency_func: Callable[[FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.internal_to_in_efficiency_func)

    def compute_internal_to_in(self, state: FullStateWithInput,
                               delta_t: float) -> float:
        """
        Computes the energy consumption from
        the internal storage to the input.
        """
        assert_type(state,
                    expected_type=(FullStateWithInput))
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.input.set_receiving()
        return state.input.power * delta_t / self.internal_to_in_efficiency_value(state=state)

    def internal_to_in_efficiency_value(self, state: FullStateWithInput) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=(FullStateNoInput, FullStateWithInput))
        return self.internal_to_in_efficiency_func(state)


@dataclass
class InToOutEnergyConsumption():
    """
    """
    in_to_out_efficiency_func: Callable[[FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.in_to_out_efficiency_func)

    def compute_in_to_out(self, state: FullStateWithInput,
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

    def in_to_out_efficiency_value(self, state: FullStateWithInput) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        return self.in_to_out_efficiency_func(state)


@dataclass
class OutToInEnergyConsumption():
    """
    """
    out_to_in_efficiency_func: Callable[[FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.out_to_in_efficiency_func)

    def compute_out_to_in(self, state: FullStateWithInput,
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

    def out_to_in_efficiency_value(self, state: FullStateWithInput) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        return self.out_to_in_efficiency_func(state)


@dataclass
class InternalToOutFuelConsumption():
    """
    """
    internal_to_out_fuel_consumption_func: Callable[[FullStateNoInput], float]

    def __post_init__(self):
        assert_callable(self.internal_to_out_fuel_consumption_func)

    def compute_internal_to_out(self, state: FullStateNoInput,
                                delta_t: float):
        """
        Calculates the fuel transfered from
        internal storage to the output.
        """
        assert_type(state,
                    expected_type=FullStateNoInput)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.output.set_receiving()
        return self.internal_to_out_fuel_consumption_value(state) * delta_t

    def internal_to_out_fuel_consumption_value(self, state: FullStateNoInput) -> float:
        """
        Returns the marginal fuel consumption at a given state.
        """
        assert_type(state,
                    expected_type=FullStateNoInput)
        return self.internal_to_out_fuel_consumption_func(state)


@dataclass
class InToOutFuelConsumption():
    """
    """
    in_to_out_fuel_consumption_func: Callable[[FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.in_to_out_fuel_consumption_func)

    def compute_in_to_out(self, state: FullStateWithInput,
                          delta_t: float):
        """
        Calculates the fuel consumed
        from input to generate an output.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.output.set_receiving()
        return self.in_to_out_fuel_consumption_value(state) * delta_t

    def in_to_out_fuel_consumption_value(self, state: FullStateWithInput) -> float:
        """
        Returns the marginal fuel consumption at a given state.
        """
        assert_type(state,
                    expected_type=FullStateNoInput)
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
class BaseBattery():
    """
    """
    

@dataclass
class RechargeableBatteryConsumption(EnergySourceConsumption, InternalToOutEnergyConsumption, OutToInternalEnergyConsumption,
                                     InternalToInEnergyConsumption, InToInternalEnergyConsumption):
    """
    Models energy consumption in a rechargeable battery.
    """


@dataclass
class NonRechargeableBatteryConsumption(EnergySourceConsumption, InternalToOutEnergyConsumption):
    """
    Models energy consumption in a non rechargeable battery.
    """


@dataclass
class ElectricMotorConsumption(ConverterConsumption, InToOutEnergyConsumption, OutToInEnergyConsumption):
    """
    Models energy consumption in a reversible electric motor.
    """


@dataclass
class ElectricGeneratorConsumption(ConverterConsumption, InToOutEnergyConsumption):
    """
    Models energy consumption in an irreversible electric generator.
    """


@dataclass
class CombustionEngineConsumption(ConverterConsumption, InToOutFuelConsumption):
    """
    Models fuel consumption in a combustion engine.
    """


@dataclass
class FuelCellConsumption(CombustionEngineConsumption):
    """
    Models consumption in a fuel cell.
    """


@dataclass
class PureMechanicalConsumption(ConverterConsumption, InToOutEnergyConsumption, OutToInEnergyConsumption):
    """
    Models consumption in a reversible
    mechanical-to-mechanical component
    (gears, etc).
    """


@dataclass
class PureElectricConsumption(ConverterConsumption, InToOutEnergyConsumption):
    """
    Models consumption in a non reversible 
    electric-to-electric component (rectifiers,
    inverters, etc).
    """


@dataclass
class FuelTankConsumption(EnergySourceConsumption, InternalToOutFuelConsumption):
    """
    Models the fuel consumption in a fuel tank.
    """


# ========
# CREATORS
# ========

def return_rechargeable_battery_consumption(
        discharge_efficiency_func: Callable[
            [FullStateNoInput|FullStateWithInput], float],
        recharge_efficiency_func: Callable[
            [FullStateNoInput|FullStateWithInput], float]
        ) -> RechargeableBatteryConsumption:
    return RechargeableBatteryConsumption(
        in_to_internal_efficiency_func=recharge_efficiency_func,
        internal_to_in_efficiency_func=discharge_efficiency_func,
        out_to_internal_efficiency_func=recharge_efficiency_func,
        internal_to_out_efficiency_func=discharge_efficiency_func
    )

def return_non_rechargeable_battery_consumption(
        discharge_efficiency_func: Callable[
            [FullStateNoInput], float],
        ) -> NonRechargeableBatteryConsumption:
    return NonRechargeableBatteryConsumption(
        internal_to_out_efficiency_func=discharge_efficiency_func
    )

def return_electric_motor_consumption(
        motor_efficiency_func: Callable[[FullStateWithInput], float],
        generator_efficiency_func: Callable[[FullStateWithInput], float]
        ) -> ElectricMotorConsumption:
    return ElectricMotorConsumption(
        in_to_out_efficiency_func=motor_efficiency_func,
        out_to_in_efficiency_func=generator_efficiency_func,
    )

def return_electric_generator_consumption(
        generator_efficiency_func: Callable[[FullStateWithInput], float]
        ) -> ElectricGeneratorConsumption:
    return ElectricGeneratorConsumption(
        in_to_out_efficiency_func=generator_efficiency_func
    )

def return_combustion_engine_consumption(
        fuel_consumption_func: Callable[[FullStateWithInput], float]
        ) -> CombustionEngineConsumption:
    return CombustionEngineConsumption(
        in_to_out_fuel_consumption_func=fuel_consumption_func
    )

def return_fuel_cell_consumption(
        fuel_consumption_func: Callable[[FullStateWithInput], float]
        ) -> FuelCellConsumption:
    return FuelCellConsumption(
        in_to_out_fuel_consumption_func=fuel_consumption_func
    )

def return_pure_mechanical_consumption(
        efficiency_func: Callable[[FullStateWithInput], float],
        reverse_efficiency_func: Callable[[FullStateWithInput], float]
        ) -> PureMechanicalConsumption:
    return PureMechanicalConsumption(
        in_to_out_efficiency_func=efficiency_func,
        out_to_in_efficiency_func=reverse_efficiency_func
    )

def return_pure_electric_consumption(
    efficiency_func: Callable[[FullStateWithInput], float]
    ) -> PureElectricConsumption:
    return PureElectricConsumption(
        in_to_out_efficiency_func=efficiency_func
    )

def return_fuel_tank_consumption(
    fuel_consumption_func: Callable[[FullStateNoInput], float]
    ) -> FuelTankConsumption:
    return FuelTankConsumption(
        internal_to_out_fuel_consumption_func=fuel_consumption_func
    )
