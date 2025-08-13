"""This module contains classes for representing
the dynamic responses of components."""

from abc import ABC
from dataclasses import dataclass
from typing import Callable
from components.state import FullStateWithInput
from helpers.functions import assert_callable


@dataclass
class DynamicResponse(ABC):
    """
    Base class for dynamic responses.
    Includes methods that must be overridden if applicable.
    """
    forward_response: Callable[[FullStateWithInput, float], FullStateWithInput]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, state: FullStateWithInput,
                        delta_t: float) -> FullStateWithInput:
        return self.forward_response(state, delta_t)

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
    reverse_response: Callable[[FullStateWithInput, float], FullStateWithInput]
    
    def __post_init__(self):
        super().__post_init__()
        assert_callable(self.reverse_response)

    def compute_reverse(self, state: FullStateWithInput,
                        delta_t: float) -> FullStateWithInput:
        return self.reverse_response(state, delta_t)

    @property
    def reversible(self) -> bool:
        return True
