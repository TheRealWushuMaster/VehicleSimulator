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
class InternalNonReversibleEnergyConsumption():
    """
    Base class for modeling internal energy
    consumption of a component.
    Applies to components that store their
    own energy (batteries and others).
    """
    efficiency_func: Callable[[FullStateNoInput|FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.efficiency_func)

    def compute(self, state: FullStateNoInput|FullStateWithInput,
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
        return state.output.power * delta_t / self.efficiency_value(state=state)

    def efficiency_value(self, state: FullStateNoInput|FullStateWithInput) -> float:
        """
        Returns the efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=(FullStateNoInput, FullStateWithInput))
        return self.efficiency_func(state)


@dataclass
class InternalReversibleEnergyConsumption(InternalNonReversibleEnergyConsumption):
    """
    Base class for modeling internal reversible
    energy consumption from a component.
    Applies to components that store their
    own energy (batteries and others).
    """
    reverse_efficiency_func: Callable[[FullStateNoInput|FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.reverse_efficiency_func)

    def reverse_compute(self, state: FullStateNoInput|FullStateWithInput,
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
        return state.output.power * delta_t / self.reverse_efficiency_value(state=state)

    def reverse_efficiency_value(self, state: FullStateNoInput|FullStateWithInput) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=(FullStateNoInput, FullStateWithInput))
        return self.reverse_efficiency_func(state)


@dataclass
class ExternalNonReversibleEnergyConsumption():
    """
    Base class for modeling non reversible
    external energy consumption of a component.
    Applies to components that request energy
    from elsewhere (mainly converters).
    """
    efficiency_func: Callable[[FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.efficiency_func)

    def compute(self, state: FullStateWithInput,
                delta_t: float) -> float:
        """
        Calculates energy consumption from the
        input being delivered to the output.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.output.set_receiving()
        state.input.set_delivering()
        return state.output.power * delta_t / self.efficiency_value(state=state)

    def efficiency_value(self, state: FullStateWithInput) -> float:
        """
        Returns the efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        return self.efficiency_func(state)


@dataclass
class ExternalReversibleEnergyConsumption(ExternalNonReversibleEnergyConsumption):
    """
    Base class for modeling reversible external
    energy consumption of a component.
    Applies to components that request energy
    from elsewhere (mainly converters).
    """
    reverse_efficiency_func: Callable[[FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.reverse_efficiency_func)

    def reverse_compute(self, state: FullStateWithInput,
                        delta_t: float) -> float:
        """
        Calculates reverse energy consumption from the
        output being delivered to the input.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.output.set_delivering()
        state.input.set_receiving()
        return state.output.power * delta_t / self.reverse_efficiency_value(state=state)

    def reverse_efficiency_value(self, state: FullStateWithInput) -> float:
        """
        Returns the reverse efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        return self.reverse_efficiency_func(state)


@dataclass
class ExternalNonReversibleFuelConsumption():
    """
    Base class for modeling non reversible
    fuel consumption from the input.
    Applies to components that consume
    fuel (combustion engines).
    """
    fuel_consumption_func: Callable[[FullStateWithInput], float]

    def __post_init__(self):
        assert_callable(self.fuel_consumption_func)

    def compute(self, state: FullStateWithInput,
                delta_t: float):
        """
        Calculates the fuel consumed from the input.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        state.input.set_delivering()
        state.output.set_receiving()
        return self.fuel_consumption(state) * delta_t

    def fuel_consumption(self, state: FullStateWithInput) -> float:
        """
        Returns the marginal fuel consumption at a given state.
        """
        assert_type(state,
                    expected_type=FullStateWithInput)
        return self.fuel_consumption_func(state)


# ================
# TAILORES CLASSES
# ================


@dataclass
class RechargeableBatteryConsumption():
    """
    Models energy consumption in a rechargeable battery.
    """
    internal: InternalReversibleEnergyConsumption

    def __post_init__(self):
        assert_type(self.internal,
        expected_type=InternalReversibleEnergyConsumption)


@dataclass
class NonRechargeableBatteryConsumption():
    """
    Models energy consumption in a non rechargeable battery.
    """
    internal: InternalNonReversibleEnergyConsumption

    def __post_init__(self):
        assert_type(self.internal,
                    expected_type=InternalNonReversibleEnergyConsumption)


@dataclass
class ElectricMotorConsumption():
    """
    Models consumption in a non rechargeable battery.
    """
    external: ExternalReversibleEnergyConsumption

    def __post_init__(self):
        assert_type(self.external,
                    expected_type=ExternalReversibleEnergyConsumption)


@dataclass
class ElectricGeneratorConsumption():
    """
    Models consumption in an irreversible electric generator.
    """
    external: ExternalNonReversibleEnergyConsumption

    def __post_init__(self):
        assert_type(self.external,
                    expected_type=ExternalNonReversibleEnergyConsumption)


@dataclass
class CombustionEngineConsumption():
    """
    Models consumption in a combustion engine.
    """
    external: ExternalNonReversibleFuelConsumption

    def __post_init__(self):
        assert_type(self.external,
                    expected_type=ExternalNonReversibleFuelConsumption)


@dataclass
class FuelCellConsumption(CombustionEngineConsumption):
    """
    Models consumption in a fuel cell.
    """


@dataclass
class PureMechanicalConsumption():
    """
    Models consumption in a reversible
    mechanical-to-mechanical component
    (gears, etc).
    """
    external: ExternalReversibleEnergyConsumption

    def __post_init__(self):
        assert_type(self.external,
                    expected_type=ExternalReversibleEnergyConsumption)


@dataclass
class PureElectricConsumption():
    """
    Models consumption in a non reversible 
    electric-to-electric component (rectifiers,
    inverters, etc).
    """
    external: ExternalNonReversibleEnergyConsumption

    def __post_init__(self):
        assert_type(self.external,
                    expected_type=ExternalNonReversibleEnergyConsumption)


# ========
# CREATORS
# ========

def return_rechargeable_battery_consumption(
        efficiency_func: Callable[
            [FullStateNoInput|FullStateWithInput], float],
        reverse_efficiency_func: Callable[
            [FullStateNoInput|FullStateWithInput], float]
        ) -> RechargeableBatteryConsumption:
    return RechargeableBatteryConsumption(
        internal=InternalReversibleEnergyConsumption(
            efficiency_func=efficiency_func,
            reverse_efficiency_func=reverse_efficiency_func
            )
        )

def return_non_rechargeable_battery_consumption(
        efficiency_func: Callable[
            [FullStateNoInput|FullStateWithInput], float]
        ) -> NonRechargeableBatteryConsumption:
    return NonRechargeableBatteryConsumption(
        internal=InternalNonReversibleEnergyConsumption(
            efficiency_func=efficiency_func
        )
    )

def return_electric_motor_consumption(
        efficiency_func: Callable[[FullStateWithInput], float],
        reverse_efficiency_func: Callable[[FullStateWithInput], float]
        ) -> ElectricMotorConsumption:
    return ElectricMotorConsumption(
        external=ExternalReversibleEnergyConsumption(
            efficiency_func=efficiency_func,
            reverse_efficiency_func=reverse_efficiency_func
        )
    )

def return_electric_generator_consumption(
        efficiency_func: Callable[[FullStateWithInput], float]
        ) -> ElectricGeneratorConsumption:
    return ElectricGeneratorConsumption(
        external=ExternalNonReversibleEnergyConsumption(
            efficiency_func=efficiency_func
        )
    )

def return_combustion_engine_consumption(
        fuel_consumption_func: Callable[[FullStateWithInput], float]
        ) -> CombustionEngineConsumption:
    return CombustionEngineConsumption(
        external=ExternalNonReversibleFuelConsumption(
            fuel_consumption_func=fuel_consumption_func
        )
    )

def return_fuel_cell_consumption(
        fuel_consumption_func: Callable[[FullStateWithInput], float]
        ) -> FuelCellConsumption:
    return FuelCellConsumption(
        external=ExternalNonReversibleFuelConsumption(
            fuel_consumption_func=fuel_consumption_func
        )
    )

def return_pure_mechanical_consumption(
        efficiency_func: Callable[[FullStateWithInput], float],
        reverse_efficiency_func: Callable[[FullStateWithInput], float]
        ) -> PureMechanicalConsumption:
    return PureMechanicalConsumption(
        external=ExternalReversibleEnergyConsumption(
            efficiency_func=efficiency_func,
            reverse_efficiency_func=reverse_efficiency_func
        )
    )

def return_pure_electric_consumption(
    efficiency_func: Callable[[FullStateWithInput], float]
    ) -> PureElectricConsumption:
    return PureElectricConsumption(
        external=ExternalNonReversibleEnergyConsumption(
            efficiency_func=efficiency_func
        )
    )
