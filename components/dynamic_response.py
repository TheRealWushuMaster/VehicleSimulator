"""This module contains classes for representing
the dynamic responses of components."""

from dataclasses import dataclass
from typing import Callable
from components.consumption import ElectricMotorConsumption, \
    ElectricGeneratorConsumption, LiquidCombustionEngineConsumption, \
    GaseousCombustionEngineConsumption, FuelCellConsumption
from components.limitation import ElectricMotorLimits, \
    ElectricGeneratorLimits, \
    LiquidCombustionEngineLimits, GaseousCombustionEngineLimits, \
    FuelCellLimits
from components.component_snapshot import ElectricMotorSnapshot, ElectricGeneratorSnapshot, \
    LiquidCombustionEngineSnapshot, GaseousCombustionEngineSnapshot, \
    GearBoxSnapshot, FuelCellSnapshot, ElectricInverterSnapshot, ElectricRectifierSnapshot
from components.component_state import ElectricMotorState, ElectricGeneratorState, \
    InternalCombustionEngineState, FuelCellState, PureElectricState, PureMechanicalState
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
    forward_response: Callable[[ElectricMotorSnapshot,
                                float, float, float,
                                ElectricMotorConsumption,
                                ElectricMotorLimits],
                               tuple[ElectricMotorSnapshot,
                                     ElectricMotorState]]
    reverse_response: Callable[[ElectricMotorSnapshot,
                                ElectricMotorConsumption,
                                ElectricMotorLimits],
                               tuple[ElectricMotorSnapshot,
                                     ElectricMotorState]]

    def __post_init__(self):
        assert_callable(self.forward_response,
                        self.reverse_response)

    def compute_forward(self, snap: ElectricMotorSnapshot,
                        downstream_inertia: float,
                        delta_t: float,
                        throttle_signal: float,
                        efficiency: ElectricMotorConsumption,
                        limits: ElectricMotorLimits
                        ) -> tuple[ElectricMotorSnapshot,
                                   ElectricMotorState]:
        """
        Computes the output of the motor
        for a given electric input.
        """
        assert_type(snap,
                    expected_type=ElectricMotorSnapshot)
        assert_type(efficiency,
                    expected_type=ElectricMotorConsumption)
        assert_type(limits,
                    expected_type=ElectricMotorLimits)
        assert_type_and_range(throttle_signal,
                              more_than=0.0)
        assert_type_and_range(downstream_inertia, delta_t,
                              more_than=0.0,
                              include_more=False)
        new_snap, new_state = self.forward_response(snap,
                                                    downstream_inertia,
                                                    delta_t,
                                                    throttle_signal,
                                                    efficiency,
                                                    limits)
        return new_snap, new_state

    def compute_reverse(self, snap: ElectricMotorSnapshot,
                        efficiency: ElectricMotorConsumption,
                        limits: ElectricMotorLimits
                        ) -> tuple[ElectricMotorSnapshot,
                                   ElectricMotorState]:
        """
        Computes the input of the motor
        when acting as a generator.
        """
        assert_type(snap,
                    expected_type=ElectricMotorSnapshot)
        assert_type(efficiency,
                    expected_type=ElectricMotorConsumption)
        assert_type(limits,
                    expected_type=ElectricMotorLimits)
        new_snap, new_state = self.reverse_response(snap,
                                                    efficiency,
                                                    limits)
        return new_snap, new_state

    @property
    def reversible(self) -> bool:
        """
        States that the component is reversible.
        """
        return True


@dataclass
class ElectricGeneratorDynamicResponse(BaseDynamicResponse):
    """
    Creates the dynamic response
    of an electric generator.
    """
    forward_response: Callable[[ElectricGeneratorSnapshot,
                                ElectricGeneratorConsumption,
                                ElectricGeneratorLimits],
                               tuple[ElectricGeneratorSnapshot,
                                     ElectricGeneratorState]]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, snap: ElectricGeneratorSnapshot,
                        efficiency: ElectricGeneratorConsumption,
                        limits: ElectricGeneratorLimits
                        ) -> tuple[ElectricGeneratorSnapshot,
                                   ElectricGeneratorState]:
        """
        Computes the output of the motor
        for a given electric input.
        """
        assert_type(snap,
                    expected_type=ElectricGeneratorSnapshot)
        assert_type(efficiency,
                    expected_type=ElectricGeneratorConsumption)
        assert_type(limits,
                    expected_type=ElectricGeneratorLimits)
        new_snap, new_state = self.forward_response(snap,
                                                    efficiency,
                                                    limits)
        return new_snap, new_state

    @property
    def reversible(self) -> bool:
        """
        States that the component is irreversible.
        """
        return False


@dataclass
class LiquidCombustionDynamicResponse(BaseDynamicResponse):
    """
    Creates the dynamic response
    of a liquid combustion engine.
    """
    forward_response: Callable[[LiquidCombustionEngineSnapshot, float,
                                float, float, float,
                                LiquidCombustionEngineConsumption,
                                LiquidCombustionEngineLimits],
                               tuple[LiquidCombustionEngineSnapshot,
                                     InternalCombustionEngineState]]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, snap: LiquidCombustionEngineSnapshot,
                        load_torque: float,
                        downstream_inertia: float,
                        delta_t: float,
                        throttle_signal: float,
                        fuel_consumption: LiquidCombustionEngineConsumption,
                        limits: LiquidCombustionEngineLimits
                        ) -> tuple[LiquidCombustionEngineSnapshot,
                                   InternalCombustionEngineState]:
        """
        Computes the output of the
        engine for a given fuel input.
        """
        assert_type(snap,
                    expected_type=LiquidCombustionEngineSnapshot)
        assert_type(fuel_consumption,
                    expected_type=LiquidCombustionEngineConsumption)
        assert_type(limits,
                    expected_type=LiquidCombustionEngineLimits)
        assert_type_and_range(load_torque, throttle_signal,
                              more_than=0.0)
        assert_type_and_range(downstream_inertia, delta_t,
                              more_than=0.0,
                              include_more=False)
        new_snap, new_state = self.forward_response(snap,
                                                    load_torque,
                                                    downstream_inertia,
                                                    delta_t,
                                                    throttle_signal,
                                                    fuel_consumption,
                                                    limits)
        return new_snap, new_state

    @property
    def reversible(self) -> bool:
        """
        States that the component is irreversible.
        """
        return False


@dataclass
class GaseousCombustionDynamicResponse(BaseDynamicResponse):
    """
    Creates the dynamic response
    of a gaseous combustion engine.
    """
    forward_response: Callable[[GaseousCombustionEngineSnapshot, float,
                                float, float, float,
                                GaseousCombustionEngineConsumption,
                                GaseousCombustionEngineLimits],
                               tuple[GaseousCombustionEngineSnapshot,
                                     InternalCombustionEngineState]]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, snap: GaseousCombustionEngineSnapshot,
                        load_torque: float,
                        downstream_inertia: float,
                        delta_t: float,
                        throttle_signal: float,
                        fuel_consumption: GaseousCombustionEngineConsumption,
                        limits: GaseousCombustionEngineLimits
                        ) -> tuple[GaseousCombustionEngineSnapshot,
                                   InternalCombustionEngineState]:
        """
        Computes the output of the
        engine for a given fuel input.
        """
        assert_type(snap,
                    expected_type=GaseousCombustionEngineSnapshot)
        assert_type(fuel_consumption,
                    expected_type=GaseousCombustionEngineConsumption)
        assert_type(limits,
                    expected_type=GaseousCombustionEngineLimits)
        assert_type_and_range(load_torque, throttle_signal,
                              more_than=0.0)
        assert_type_and_range(downstream_inertia, delta_t,
                              more_than=0.0,
                              include_more=False)
        new_snap, new_state = self.forward_response(snap,
                                                    load_torque,
                                                    downstream_inertia,
                                                    delta_t,
                                                    throttle_signal,
                                                    fuel_consumption,
                                                    limits)
        return new_snap, new_state

    @property
    def reversible(self) -> bool:
        """
        States that the component is irreversible.
        """
        return False


@dataclass
class PureMechanicalDynamicResponse(BaseDynamicResponse):
    """
    Creates the dynamic response of a reversible
    mechanical to mechanical component.
    """
    forward_response: Callable[[GearBoxSnapshot], tuple[GearBoxSnapshot,
                                                        PureMechanicalState]]
    reverse_response: Callable[[GearBoxSnapshot], tuple[GearBoxSnapshot,
                                                        PureMechanicalState]]

    def __post_init__(self):
        assert_callable(self.forward_response,
                        self.reverse_response)

    def compute_forward(self, snap: GearBoxSnapshot) -> tuple[GearBoxSnapshot,
                                                              PureMechanicalState]:
        """
        Computes the output of the
        pure mechanical component.
        """
        assert_type(snap,
                    expected_type=GearBoxSnapshot)
        new_snap, new_state = self.forward_response(snap)
        return new_snap, new_state

    def compute_reverse(self, snap: GearBoxSnapshot) -> tuple[GearBoxSnapshot,
                                                              PureMechanicalState]:
        """
        Computes the input of the
        pure mechanical component.
        """
        assert_type(snap,
                    expected_type=GearBoxSnapshot)
        new_snap, new_state = self.reverse_response(snap)
        return new_snap, new_state

    @property
    def reversible(self) -> bool:
        """
        States that the component is reversible.
        """
        return True


@dataclass
class FuelCellDynamicResponse(BaseDynamicResponse):
    """
    Creates the dynamic response
    of a gaseous fuel cell.
    """
    forward_response: Callable[[FuelCellSnapshot, float, float,
                                FuelCellConsumption, FuelCellLimits],
                               tuple[FuelCellSnapshot,
                                     FuelCellState]]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, snap: FuelCellSnapshot,
                        delta_t: float,
                        control_signal: float,
                        fuel_consumption: FuelCellConsumption,
                        limits: FuelCellLimits
                        ) -> tuple[FuelCellSnapshot,
                                   FuelCellState]:
        """
        Computes the output of the fuel cell.
        """
        assert isinstance(snap, FuelCellSnapshot)
        new_snap, new_state = self.forward_response(snap,
                                                    delta_t,
                                                    control_signal,
                                                    fuel_consumption,
                                                    limits)
        return new_snap, new_state

    @property
    def reversible(self) -> bool:
        """
        States that the component is irreversible.
        """
        return False


@dataclass
class RectifierDynamicResponse(BaseDynamicResponse):
    """
    Creates the dynamic response
    of an electric rectifier.
    """
    forward_response: Callable[[ElectricRectifierSnapshot],
                               tuple[ElectricRectifierSnapshot,
                                     PureElectricState]]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, snap: ElectricRectifierSnapshot
                        ) -> tuple[ElectricRectifierSnapshot,
                                   PureElectricState]:
        """
        Computes the output of the rectifier.
        """
        assert_type(snap,
                    expected_type=ElectricRectifierSnapshot)
        new_snap, new_state = self.forward_response(snap)
        return new_snap, new_state

    @property
    def reversible(self) -> bool:
        """
        States that the component is irreversible.
        """
        return False


@dataclass
class InverterDynamicResponse(BaseDynamicResponse):
    """
    Creates the dynamic response
    of an electric inverter.
    """
    forward_response: Callable[[ElectricInverterSnapshot],
                               tuple[ElectricInverterSnapshot,
                                     PureElectricState]]

    def __post_init__(self):
        assert_callable(self.forward_response)

    def compute_forward(self, snap: ElectricInverterSnapshot
                        ) -> tuple[ElectricInverterSnapshot,
                                   PureElectricState]:
        """
        Computes the output of the inverter.
        """
        assert_type(snap,
                    expected_type=ElectricInverterSnapshot)
        new_snap, new_state = self.forward_response(snap)
        return new_snap, new_state

    @property
    def reversible(self) -> bool:
        """
        States that the component is irreversible.
        """
        return False
