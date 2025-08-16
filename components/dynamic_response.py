"""This module contains classes for representing
the dynamic responses of components."""

from abc import ABC
from dataclasses import dataclass
from typing import Callable
from components.consumption import ElectricMotorConsumption, \
    ElectricGeneratorConsumption, CombustionEngineConsumption, \
    FuelCellConsumption
from components.limitation import ElectricMotorLimits, \
    ElectricGeneratorLimits, \
    LiquidCombustionEngineLimits, GaseousCombustionEngineLimits, \
    FuelCellLimits
from components.state import FullStateWithInput, \
    ElectricMotorState, ElectricGeneratorState, \
    LiquidCombustionEngineState, GaseousCombustionEngineState, \
    PureElectricState, PureMechanicalState, FuelCellState
from helpers.functions import assert_callable, assert_type, assert_type_and_range


@dataclass
class DynamicResponse(ABC):
    """
    Base class for dynamic responses.
    Includes methods that must be overridden if applicable.
    """
    forward_response: Callable[[FullStateWithInput, float, float], FullStateWithInput]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, state: FullStateWithInput,
                        delta_t: float,
                        control_signal: float=0.0) -> FullStateWithInput:
        """
        Computes the forward response of the component.
        """
        return self.forward_response(state, delta_t, control_signal)

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
    reverse_response: Callable[[FullStateWithInput, float, float], FullStateWithInput]
    
    def __post_init__(self):
        super().__post_init__()
        assert_callable(self.reverse_response)

    def compute_reverse(self, state: FullStateWithInput,
                        delta_t: float,
                        control_signal: float=0.0) -> FullStateWithInput:
        return self.reverse_response(state, delta_t, control_signal)

    @property
    def reversible(self) -> bool:
        return True





@dataclass
class ElectricMotorDynamicResponse():
    """
    Creates the dynamic response of
    a reversible electric motor.
    """
    forward_response: Callable[[ElectricMotorState, float,
                                float, float, float,
                                ElectricMotorConsumption,
                                ElectricMotorLimits],
                               ElectricMotorState]
    reverse_response: Callable[[ElectricMotorState,
                                ElectricMotorConsumption,
                                ElectricMotorLimits],
                               ElectricMotorState]

    def __post_init__(self):
        assert_callable(self.forward_response,
                        self.reverse_response)

    def compute_forward(self, state: ElectricMotorState,
                        load_torque: float,
                        downstream_inertia: float,
                        delta_t: float,
                        control_signal: float,
                        efficiency: ElectricMotorConsumption,
                        limits: ElectricMotorLimits
                        ) -> ElectricMotorState:
        """
        Computes the output of the motor
        for a given electric input.
        """
        assert_type(state,
                    expected_type=ElectricMotorState)
        assert_type(efficiency,
                    expected_type=ElectricMotorConsumption)
        assert_type(limits,
                    expected_type=ElectricMotorLimits)
        assert_type_and_range(load_torque, control_signal,
                              more_than=0.0)
        assert_type_and_range(downstream_inertia, delta_t,
                              more_than=0.0,
                              include_more=False)
        return self.forward_response(state,
                                     load_torque,
                                     downstream_inertia,
                                     delta_t,
                                     control_signal,
                                     efficiency,
                                     limits)

    def compute_reverse(self, state: ElectricMotorState,
                        efficiency: ElectricMotorConsumption,
                        limits: ElectricMotorLimits
                        ) -> ElectricMotorState:
        """
        Computes the input of the motor
        when acting as a generator.
        """
        assert_type(state,
                    expected_type=ElectricMotorState)
        assert_type(efficiency,
                    expected_type=ElectricMotorConsumption)
        assert_type(limits,
                    expected_type=ElectricMotorLimits)
        return self.reverse_response(state,
                                     efficiency,
                                     limits)

    @property
    def reversible(self) -> bool:
        return True


@dataclass
class ElectricGeneratorDynamicResponse():
    """
    Creates the dynamic response
    of an electric generator.
    """
    forward_response: Callable[[ElectricGeneratorState,
                                ElectricGeneratorConsumption,
                                ElectricGeneratorLimits],
                               ElectricGeneratorState]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, state: ElectricGeneratorState,
                        efficiency: ElectricGeneratorConsumption,
                        limits: ElectricGeneratorLimits
                        ) -> ElectricGeneratorState:
        """
        Computes the output of the motor
        for a given electric input.
        """
        assert_type(state,
                    expected_type=ElectricGeneratorState)
        assert_type(efficiency,
                    expected_type=ElectricGeneratorConsumption)
        assert_type(limits,
                    expected_type=ElectricGeneratorLimits)
        return self.forward_response(state,
                                     efficiency,
                                     limits)

    @property
    def reversible(self) -> bool:
        return False


@dataclass
class LiquidCombustionDynamicResponse():
    """
    Creates the dynamic response
    of a liquid combustion engine.
    """
    forward_response: Callable[[LiquidCombustionEngineState, float,
                                float, float, float,
                                CombustionEngineConsumption,
                                LiquidCombustionEngineLimits],
                               LiquidCombustionEngineState]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, state: LiquidCombustionEngineState,
                        load_torque: float,
                        downstream_inertia: float,
                        delta_t: float,
                        control_signal: float,
                        fuel_consumption: CombustionEngineConsumption,
                        limits: LiquidCombustionEngineLimits
                        ) -> LiquidCombustionEngineState:
        """
        Computes the output of the
        engine for a given fuel input.
        """
        assert_type(state,
                    expected_type=LiquidCombustionEngineState)
        assert_type(fuel_consumption,
                    expected_type=CombustionEngineConsumption)
        assert_type(limits,
                    expected_type=LiquidCombustionEngineLimits)
        assert_type_and_range(load_torque, control_signal,
                              more_than=0.0)
        assert_type_and_range(downstream_inertia, delta_t,
                              more_than=0.0,
                              include_more=False)
        return self.forward_response(state,
                                     load_torque,
                                     downstream_inertia,
                                     delta_t,
                                     control_signal,
                                     fuel_consumption,
                                     limits)

    @property
    def reversible(self) -> bool:
        return False


@dataclass
class GaseousCombustionDynamicResponse():
    """
    Creates the dynamic response
    of a gaseous combustion engine.
    """
    forward_response: Callable[[GaseousCombustionEngineState, float,
                                float, float, float,
                                CombustionEngineConsumption,
                                GaseousCombustionEngineLimits],
                               GaseousCombustionEngineState]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, state: GaseousCombustionEngineState,
                        load_torque: float,
                        downstream_inertia: float,
                        delta_t: float,
                        control_signal: float,
                        fuel_consumption: CombustionEngineConsumption,
                        limits: GaseousCombustionEngineLimits
                        ) -> GaseousCombustionEngineState:
        """
        Computes the output of the
        engine for a given fuel input.
        """
        assert_type(state,
                    expected_type=GaseousCombustionEngineState)
        assert_type(fuel_consumption,
                    expected_type=CombustionEngineConsumption)
        assert_type(limits,
                    expected_type=GaseousCombustionEngineLimits)
        assert_type_and_range(load_torque, control_signal,
                              more_than=0.0)
        assert_type_and_range(downstream_inertia, delta_t,
                              more_than=0.0,
                              include_more=False)
        return self.forward_response(state,
                                     load_torque,
                                     downstream_inertia,
                                     delta_t,
                                     control_signal,
                                     fuel_consumption,
                                     limits)

    @property
    def reversible(self) -> bool:
        return False


@dataclass
class PureMechanicalDynamicResponse():
    """
    Creates the dynamic response of a reversible
    mechanical to mechanical component.
    """
    forward_response: Callable[[PureMechanicalState],
                               PureMechanicalState]
    reverse_response: Callable[[PureMechanicalState],
                               PureMechanicalState]

    def __post_init__(self):
        assert_callable(self.forward_response,
                        self.reverse_response)

    def compute_forward(self, state: PureMechanicalState
                        ) -> PureMechanicalState:
        """
        Computes the output of the
        pure mechanical component.
        """
        assert_type(state,
                    expected_type=PureMechanicalState)
        return self.forward_response(state)

    def compute_reverse(self, state: PureMechanicalState
                        ) -> PureMechanicalState:
        """
        Computes the input of the
        pure mechanical component.
        """
        assert_type(state,
                    expected_type=PureMechanicalState)
        return self.reverse_response(state)

    @property
    def reversible(self) -> bool:
        return True


@dataclass
class FuelCellDynamicResponse():
    """
    Creates the dynamic response
    of a gaseous fuel cell.
    """
    forward_response: Callable[[FuelCellState, float, float,
                                FuelCellConsumption, FuelCellLimits],
                               FuelCellState]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, state: FuelCellState,
                        delta_t: float,
                        control_signal: float,
                        fuel_consumption: FuelCellConsumption,
                        limits: FuelCellLimits
                        ) -> FuelCellState:
        """
        Computes the output of the fuel cell.
        """
        assert isinstance(state, FuelCellState)
        return self.forward_response(state,
                                     delta_t,
                                     control_signal,
                                     fuel_consumption,
                                     limits)

    @property
    def reversible(self) -> bool:
        return False


@dataclass
class RectifierDynamicResponse():
    """
    Creates the dynamic response
    of an electric rectifier.
    """
    forward_response: Callable[[PureElectricState],
                               PureElectricState]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, state: PureElectricState
                        ) -> PureElectricState:
        """
        Computes the output of the
        pure mechanical component.
        """
        assert_type(state,
                    expected_type=PureElectricState)
        return self.forward_response(state)

    @property
    def reversible(self) -> bool:
        return False


@dataclass
class InverterDynamicResponse(RectifierDynamicResponse):
    """
    Creates the dynamic response
    of an electric inverter.
    """
