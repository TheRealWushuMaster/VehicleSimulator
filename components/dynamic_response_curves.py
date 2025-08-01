"""This module contains several dynamic response curves for different components."""

from typing import Callable
from components.state import State, ElectricIOState, FuelIOState, \
    RotatingIOState, InternalState
from helpers.functions import assert_type_and_range


class MechanicalToMechanical():
    """
    Contains generator methods for purely mechanical components.
    """
    @staticmethod
    def gearbox_ideal_response(gear_ratio: float, efficiency: float=1.0
                               ) -> Callable[[RotatingIOState, InternalState], RotatingIOState]:
        assert_type_and_range(gear_ratio,
                              more_than=0.0)
        assert_type_and_range(efficiency,
                              more_than=0.0,
                              less_than=1.0,
                              include_more=False)
        def response(input_state: RotatingIOState,
                     internal_state: InternalState) -> RotatingIOState:
            return RotatingIOState(torque=input_state.torque * gear_ratio * efficiency,
                                   rpm=input_state.rpm / gear_ratio)
        return response
