"""This module contains routines for managing
energy and fuel consumption for all components."""

from abc import ABC
from typing import Callable, Optional
from dataclasses import dataclass
from components.state import State, IOState, ElectricIOState
from helpers.functions import assert_type, assert_type_and_range


@dataclass
class BaseConsumptionModel(ABC):
    """
    Base class for consumption objects.
    """
    def compute(self, state: State,
                source_state,
                delta_t: float) -> float:
        raise NotImplementedError


@dataclass
class ElectricEnergyConsumption(BaseConsumptionModel):
    """
    Models the electric energy consumption of a component.
    """
    efficiency_func: Callable[[State], float]

    def compute(self, state: State,
                source_state: ElectricIOState,
                delta_t: float) -> float:
        """
        Calculates electric energy consumption.
        Arguments:
            - `state` (State): the full state variable
                of the component
            - `source_state` (ElectricIOState): the state
                originating the consumption
        
        The `source_state` acts as the "output", generating
        an input that consumes the electric energy being calculated.
        """
        assert_type(state,
                    expected_type=State)
        assert_type(source_state,
                    expected_type=ElectricIOState)
        assert_type_and_range(delta_t,
                              more_than=0.0)
        return source_state.power * delta_t / self.efficiency_func(state)

    @property
    def efficiency_value(self, state: State) -> float:
        return self.efficiency_func(state)


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

    def compute_forward(self, state: State) -> IOState:
        """
        Computes the forward consumption.
        """
        
        raise NotImplementedError

    def compute_reverse(self, state: State) -> IOState:
        """
        Computes the reverse consumption, if applicable.
        """
        if not self.reversible:
            raise ValueError("Consumption is not reversible.")
        raise NotImplementedError

    @property
    def reversible(self) -> bool:
        return self.reverse is not None