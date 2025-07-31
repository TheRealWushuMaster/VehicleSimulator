"""This module contains routines for managing
energy and fuel consumption for all components."""

from abc import ABC
from typing import Callable, Optional, Literal, Type
from dataclasses import dataclass
from components.state import State, ElectricIOState, RotatingIOState
from helpers.functions import assert_type, assert_type_and_range


@dataclass
class BaseConsumptionModel(ABC):
    """
    Base class for consumption objects.
    """
    def compute(self, state: State,
                which: Literal["input", "output"],
                delta_t: float) -> float:
        """
        Calculates the base consumption.
        """
        raise NotImplementedError


@dataclass
class EnergyConsumption(BaseConsumptionModel):
    """
    Base class for modeling energy
    consumption from a component.
    Applies to electric and mechanical components.
    """
    efficiency_func: Callable[[State], float]
    energy_type: Type[ElectricIOState]|Type[RotatingIOState]

    def __post_init__(self):
        assert_type(self.efficiency_func,
                    expected_type=Callable)  # type: ignore[arg-type]
        assert_type(self.energy_type,
                    expected_type=(ElectricIOState, RotatingIOState))

    def compute(self, state: State,
                which: Literal["input", "output"],
                delta_t: float) -> float:
        """
        Calculates energy consumption.
        Arguments:
            - `state` (State): the full state variable
                of the component
            - `which` ("input" or "output"): the state
                originating the consumption
        
        The `which` IOState acts as the "output", generating
        an input that consumes the energy being calculated.
        """
        assert_type(state,
                    expected_type=State)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        assert which in ("input", "output")
        if which == "input":
            source_state = state.output
        else:
            assert state.input is not None
            source_state = state.input
        assert isinstance(source_state, self.energy_type)
        return source_state.power * delta_t / self.efficiency_func(state)  # type: ignore[attr-defined]

    def efficiency_value(self, state: State) -> float:
        """
        Returns the efficiency value at a given state.
        """
        assert_type(state,
                    expected_type=State)
        return self.efficiency_func(state)


@dataclass
class ElectricEnergyConsumption(EnergyConsumption):
    """
    Models the electric energy consumption of a component.
    """
    def __init__(self, efficiency_func: Callable[[State], float]):
        super().__init__(efficiency_func=efficiency_func,
                         energy_type=ElectricIOState)


@dataclass
class MechanicalEnergyConsumption(EnergyConsumption):
    """
    Models the mechanical energy consumption of a component.
    """
    def __init__(self, efficiency_func: Callable[[State], float]):
        super().__init__(efficiency_func=efficiency_func,
                         energy_type=RotatingIOState)


@dataclass
class FuelConsumption(BaseConsumptionModel):
    """
    Models the fuel consumption of components.
    """
    fuel_consumption_func: Callable[[State], float]

    def __post_init__(self):
        assert_type(self.fuel_consumption_func,
                    expected_type=Callable)  # type: ignore[arg-type]

    def compute(self, state: State,
                which: Literal["input", "output"],
                delta_t: float) -> float:
        assert_type(state,
                    expected_type=State)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        return self.fuel_consumption_func(state)


@dataclass
class Consumption():
    """
    Class containing forward and (optional) reverse consumption objects.
    """
    forward: BaseConsumptionModel
    reverse: Optional[BaseConsumptionModel]=None

    def __post_init__(self):
        assert_type(self.forward,
                    expected_type=BaseConsumptionModel)
        assert_type(self.reverse,
                    expected_type=BaseConsumptionModel,
                    allow_none=True)

    def compute_forward(self, state: State,
                        delta_t: float) -> float:
        """
        Computes the forward consumption.
        """
        assert_type(state,
                    expected_type=State)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        return self.forward.compute(state=state,
                                    which="output",
                                    delta_t=delta_t)

    def compute_reverse(self, state: State,
                        delta_t: float) -> float:
        """
        Computes the reverse consumption, if applicable.
        """
        if not self.reversible:
            raise ValueError("Consumption is not reversible.")
        assert_type(state,
                    expected_type=State)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        assert self.reverse is not None
        return self.reverse.compute(state=state,
                                    which="input",
                                    delta_t=delta_t)

    @property
    def reversible(self) -> bool:
        """
        Returns whether the consumption is reversible.
        """
        return self.reverse is not None
