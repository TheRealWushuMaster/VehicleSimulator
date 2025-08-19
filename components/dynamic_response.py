"""This module contains classes for representing
the dynamic responses of components."""

from dataclasses import dataclass
from typing import Callable
from components.consumption import ElectricMotorConsumption, \
    ElectricGeneratorConsumption, CombustionEngineConsumption, \
    FuelCellConsumption
from components.limitation import ElectricMotorLimits, \
    ElectricGeneratorLimits, \
    LiquidCombustionEngineLimits, GaseousCombustionEngineLimits, \
    FuelCellLimits
from components.state import \
    ElectricMotorState, ElectricGeneratorState, \
    LiquidCombustionEngineState, GaseousCombustionEngineState, \
    PureElectricState, PureMechanicalState, FuelCellState
from helpers.functions import assert_callable, assert_type, assert_type_and_range

class BaseDynamicResponse():
    """
    Base class for categorizing dynamic responses.
    """


@dataclass
class ElectricMotorDynamicResponse(BaseDynamicResponse):
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
        new_state = self.forward_response(state,
                                          load_torque,
                                          downstream_inertia,
                                          delta_t,
                                          control_signal,
                                          efficiency,
                                          limits)
        new_state.input.set_delivering()
        new_state.output.set_receiving()
        return new_state

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
        new_state = self.reverse_response(state,
                                          efficiency,
                                          limits)
        new_state.input.set_receiving()
        new_state.output.set_delivering()
        return new_state

    @property
    def reversible(self) -> bool:
        return True


@dataclass
class ElectricGeneratorDynamicResponse(BaseDynamicResponse):
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
        new_state = self.forward_response(state,
                                          efficiency,
                                          limits)
        new_state.input.set_delivering()
        new_state.output.set_receiving()
        return new_state

    @property
    def reversible(self) -> bool:
        return False


@dataclass
class LiquidCombustionDynamicResponse(BaseDynamicResponse):
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
        new_state = self.forward_response(state,
                                          load_torque,
                                          downstream_inertia,
                                          delta_t,
                                          control_signal,
                                          fuel_consumption,
                                          limits)
        new_state.input.set_delivering()
        new_state.output.set_receiving()
        return new_state

    @property
    def reversible(self) -> bool:
        return False


@dataclass
class GaseousCombustionDynamicResponse(BaseDynamicResponse):
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
        new_state = self.forward_response(state,
                                          load_torque,
                                          downstream_inertia,
                                          delta_t,
                                          control_signal,
                                          fuel_consumption,
                                          limits)
        new_state.input.set_delivering()
        new_state.output.set_receiving()
        return new_state

    @property
    def reversible(self) -> bool:
        return False


@dataclass
class PureMechanicalDynamicResponse(BaseDynamicResponse):
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
        new_state = self.forward_response(state)
        new_state.input.set_delivering()
        new_state.output.set_receiving()
        return new_state

    def compute_reverse(self, state: PureMechanicalState
                        ) -> PureMechanicalState:
        """
        Computes the input of the
        pure mechanical component.
        """
        assert_type(state,
                    expected_type=PureMechanicalState)
        new_state = self.reverse_response(state)
        new_state.input.set_receiving()
        new_state.output.set_delivering()
        return new_state

    @property
    def reversible(self) -> bool:
        return True


@dataclass
class FuelCellDynamicResponse(BaseDynamicResponse):
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
        new_state = self.forward_response(state,
                                          delta_t,
                                          control_signal,
                                          fuel_consumption,
                                          limits)
        new_state.input.set_delivering()
        new_state.output.set_receiving()
        return new_state

    @property
    def reversible(self) -> bool:
        return False


@dataclass
class RectifierDynamicResponse(BaseDynamicResponse):
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
        new_state = self.forward_response(state)
        new_state.input.set_delivering()
        new_state.output.set_receiving()
        return new_state

    @property
    def reversible(self) -> bool:
        return False


@dataclass
class InverterDynamicResponse(RectifierDynamicResponse):
    """
    Creates the dynamic response
    of an electric inverter.
    """
