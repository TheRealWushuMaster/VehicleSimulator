"""This module contains definitions for state variables for all components."""

from dataclasses import dataclass
from simulation.constants import DEFAULT_TEMPERATURE


@dataclass
class RotatingState():
    """
    Defines a rotating mechanical state variable.
    """
    rpm: float=0.0


@dataclass
class BaseInternalState():
    """
    Defines the internal state of any component.
    """
    temperature: float=DEFAULT_TEMPERATURE


@dataclass
class MotorInternalState(BaseInternalState):
    """
    Defines the internal state of a motor or engine.
    """
    on: bool=True


@dataclass
class ConverterState():
    """
    Base class for a converter's state.
    """


@dataclass
class ElectricMotorState(ConverterState):
    """
    Defines the state variable of an electric motor.
    """
    internal: MotorInternalState
    output_port: RotatingState


@dataclass
class InternalCombustionEngineState(ConverterState):
    """
    Defines the state variable of an internal combustion engine.
    """
    internal: MotorInternalState
    output_port: RotatingState


@dataclass
class ElectricGeneratorState(ConverterState):
    """
    Defines the state variable of an electric generator.
    """
    input_port: RotatingState
    internal: BaseInternalState


def return_electric_motor_state(temperature: float=DEFAULT_TEMPERATURE,
                                on: bool=True,
                                rpm: float=0.0) -> ElectricMotorState:
    """
    Returns an instance of `ElectricMotorState`.
    """
    return ElectricMotorState(internal=MotorInternalState(temperature=temperature,
                                                          on=on),
                              output_port=RotatingState(rpm=rpm))

def return_internal_combustion_engine_state(temperature: float=DEFAULT_TEMPERATURE,
                                            on: bool=True,
                                            rpm: float=0.0) -> InternalCombustionEngineState:
    """
    Returns an instance of `InternalCombustionEngineState`.
    """
    return InternalCombustionEngineState(internal=MotorInternalState(temperature=temperature,
                                                                     on=on),
                                         output_port=RotatingState(rpm=rpm))

def return_electric_generator_state(temperature: float=DEFAULT_TEMPERATURE,
                                    rpm: float=0.0) -> ElectricGeneratorState:
    """
    Returns an instance of `ElectricGeneratorState`.
    """
    return ElectricGeneratorState(internal=BaseInternalState(temperature=temperature),
                                  input_port=RotatingState(rpm=rpm))
