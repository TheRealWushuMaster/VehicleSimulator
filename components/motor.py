"""
This module contains definitions for motors and engines.
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional
from components.fuel_type import Fuel
from components.converter import MechanicalConverter
from components.port import PortInput, PortOutput, PortBidirectional
from components.state import MechanicalState, zero_mechanical_state
from helpers.functions import assert_type_and_range
from helpers.types import PowerType

@dataclass
class ElectricMotor(MechanicalConverter):
    """Models a simple, reversible electric motor."""
    def __init__(self,
                 name: str,
                 mass: float,
                 max_power: float,
                 eff_func: Callable[[MechanicalState], float],
                 reverse_efficiency: float,
                 state: Optional[MechanicalState],
                 power_func: Callable[[MechanicalState], float],
                 inertia: float):
        if state is None:
            state = zero_mechanical_state()
        input_port = PortBidirectional(exchange=PowerType.ELECTRIC)
        output_port = PortBidirectional(exchange=PowerType.MECHANICAL)
        super().__init__(name=name,
                         mass=mass,
                         input=input_port,
                         output=output_port,
                         control_signal=0.0,
                         state=state,
                         max_power=max_power,
                         power_func=power_func, # type: ignore[arg-type]
                         efficiency_func=eff_func, # type: ignore[arg-type]
                         reverse_efficiency=reverse_efficiency,
                         inertia=inertia)


@dataclass
class InternalCombustionEngine(MechanicalConverter):
    """Models a simple internal combustion engine."""
    def __init__(self,
                 name: str,
                 mass: float,
                 max_power: float,
                 eff_func: Callable[[MechanicalState], float],
                 state: Optional[MechanicalState],
                 power_func: Callable[[MechanicalState], float],
                 fuel: Fuel,
                 inertia: float):
        if state is None:
            state = zero_mechanical_state()
        input_port = PortInput(exchange=fuel)
        output_port = PortOutput(exchange=PowerType.MECHANICAL)
        super().__init__(name=name,
                         mass=mass,
                         input=input_port,
                         output=output_port,
                         control_signal=0.0,
                         state=state,
                         max_power=max_power,
                         power_func=power_func, # type: ignore[arg-type]
                         efficiency_func=eff_func, # type: ignore[arg-type]
                         reverse_efficiency=None,
                         inertia=inertia)


@dataclass
class ElectricGenerator(MechanicalConverter):
    """Models a simple, non reversible electric generator."""
    def __init__(self,
                 name: str,
                 mass: float,
                 max_power: float,
                 eff_func: Callable[[MechanicalState], float],
                 state: Optional[MechanicalState],
                 power_func: Callable[[MechanicalState], float],
                 inertia: float):
        if state is None:
            state = zero_mechanical_state()
        input_port = PortInput(exchange=PowerType.MECHANICAL)
        output_port = PortOutput(exchange=PowerType.ELECTRIC)
        super().__init__(name=name,
                         mass=mass,
                         input=input_port,
                         output=output_port,
                         control_signal=None,
                         state=state,
                         max_power=max_power,
                         power_func=power_func, # type: ignore[arg-type]
                         efficiency_func=eff_func, # type: ignore[arg-type]
                         reverse_efficiency=None,
                         inertia=inertia)
