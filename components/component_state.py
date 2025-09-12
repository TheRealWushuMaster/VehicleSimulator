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
class BatteryInternalState(BaseInternalState):
    """
    Defines a battery state variable.
    """
    electric_energy_stored: float=0.0


@dataclass
class LiquidFuelTankInternalState(BaseInternalState):
    """
    Defines a liquid fuel tank state variable.
    """
    liters_stored: float=0.0


@dataclass
class GaseousFuelTankInternalState(BaseInternalState):
    """
    Defines a gaseous fuel tank state variable.
    """
    mass_stored: float=0.0


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
class FuelCellState(ConverterState):
    """
    Defines the state variable of a fuel cell.
    """
    internal: BaseInternalState


@dataclass
class ElectricGeneratorState(ConverterState):
    """
    Defines the state variable of an electric generator.
    """
    input_port: RotatingState
    internal: BaseInternalState


@dataclass
class PureMechanicalState(ConverterState):
    """
    Defines the state variable of a pure mechanical component.
    """
    input_port: RotatingState
    internal: BaseInternalState
    output_port: RotatingState


@dataclass
class PureElectricState(ConverterState):
    """
    Defines the state variable of a pure electric component.
    """
    internal: BaseInternalState


@dataclass
class BatteryState():
    """
    Defines a battery's state variable.
    """
    internal: BatteryInternalState


@dataclass
class LiquidFuelTankState():
    """
    Defines a liquid fuel tank's state variable.
    """
    internal: LiquidFuelTankInternalState


@dataclass
class GaseousFuelTankState():
    """
    Defines a gaseous fuel tank's state variable.
    """
    internal: GaseousFuelTankInternalState


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
