"""This module contains classes for representing
the dynamic responses of components."""

from abc import ABC
from dataclasses import dataclass
from typing import Callable
from components.state import State, IOState
from helpers.functions import assert_type


@dataclass
class DynamicResponse(ABC):
    """
    Base class for dynamic responses.
    Includes methods that must be overridden if applicable.
    """
    forward_response: Callable[[State, float], IOState]

    def __post_init__(self):
        assert_type(self.forward_response,
                    expected_type=Callable)  # type: ignore[arg-type]

    def compute_forward(self, state: State,
                        delta_t: float) -> IOState:
        return self.forward_response(state, delta_t)

    def compute_reverse(self, state: State,
                        delta_t: float) -> IOState:
        raise NotImplementedError

    @property
    def reversible(self) -> bool:
        raise NotImplementedError


@dataclass
class ForwardDynamicResponse(DynamicResponse):
    """
    Creates a non-reversible dynamic response.
    """
    @property
    def reversible(self) -> bool:
        return False


@dataclass
class BidirectionalDynamicResponse(DynamicResponse):
    """
    Creates a reversible dynamic response.
    """
    reverse_response: Callable[[State, float], IOState]

    def __post_init__(self):
        super().__post_init__()
        assert_type(self.reverse_response,
                    expected_type=Callable)  # type: ignore[arg-type]

    def compute_reverse(self, state: State,
                        delta_t: float) -> IOState:
        return self.reverse_response(state, delta_t)

    @property
    def reversible(self) -> bool:
        return True
