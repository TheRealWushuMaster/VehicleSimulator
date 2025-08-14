"""This module contains several dynamic response curves for different components."""

from dataclasses import dataclass
from typing import Callable
from components.limitation import ElectricGeneratorLimits, \
    ElectricMotorLimits, LiquidCombustionEngineLimits, GaseousCombustionEngineLimits
from components.state import ElectricIOState, RotatingIOState, \
    PureMechanicalState, ElectricMotorState, ElectricGeneratorState, \
    return_electric_motor_state
from helpers.functions import assert_type, assert_type_and_range, \
    ang_vel_to_rpm
from helpers.types import ElectricSignalType


class MechanicalToMechanical():
    """
    Contains generator methods for purely mechanical components.
    """
    @staticmethod
    def forward_gearbox_ideal_response(gear_ratio: float, efficiency: float=1.0
                                       ) -> Callable[[PureMechanicalState, float, float],
                                                     PureMechanicalState]:
        """
        Generates a forward response for a stateless pure
        mechanical component.
        Receives an input `torque` and `rpm` and outputs `rpm`
        affected by `gear_ratio`, `torque`, and `efficiency`.
        """
        assert_type_and_range(gear_ratio,
                              more_than=0.0)
        assert_type_and_range(efficiency,
                              more_than=0.0,
                              less_than=1.0,
                              include_more=False)
        def response(state: PureMechanicalState,
                     delta_t: float,
                     control_signal: float) -> PureMechanicalState:
            assert isinstance(state, PureMechanicalState)
            output = RotatingIOState(torque=state.input.torque * gear_ratio * efficiency,
                                     rpm=state.input.rpm / gear_ratio)
            return PureMechanicalState(input=state.input,
                                       output=output,
                                       internal=state.internal)
        return response

    @staticmethod
    def reverse_gearbox_ideal_response(gear_ratio: float, efficiency: float=1.0
                                       ) -> Callable[[PureMechanicalState, float, float],
                                                     PureMechanicalState]:
        """
        Generates a reverse response for a stateless pure
        mechanical component.
        Receives an input `torque` and `rpm` and outputs `rpm`
        affected by `gear_ratio`, `torque`, and `efficiency`.
        """
        assert_type_and_range(gear_ratio,
                              more_than=0.0)
        assert_type_and_range(efficiency,
                              more_than=0.0,
                              less_than=1.0,
                              include_more=False)
        def response(state: PureMechanicalState,
                     delta_t: float,
                     control_signal: float) -> PureMechanicalState:
            assert isinstance(state, PureMechanicalState)
            inp = RotatingIOState(torque=state.output.torque / gear_ratio * efficiency,
                                  rpm=state.output.rpm * gear_ratio)
            return PureMechanicalState(input=inp,
                                       output=state.output,
                                       internal=state.internal)
        return response


class ElectricToMechanical():
    """
    Contains generator methods for electric motors.
    """
    @staticmethod
    def forward_driven_first_order(signal_type: ElectricSignalType
                                   ) -> Callable[[ElectricMotorState, float,
                                                  float, float, float, float],
                                                 ElectricMotorState]:
        """
        """
        def response(state: ElectricMotorState,
                     load_torque: float,
                     downstream_inertia: float,
                     delta_t: float,
                     control_signal: float,
                     efficiency: float) -> ElectricMotorState:
            assert_type(state,
                        expected_type=ElectricMotorState)
            
        return response
    
    
    @staticmethod
    def voltage_controlled_first_order(motor_params: DCElectricMotorParams,
                                       signal_type: ElectricSignalType
                                       ) -> Callable[[ElectricMotorState, float,
                                                      float, float], ElectricMotorState]:
        """
        Returns a dynamic response for a voltage-controlled electric motor.
        """
        def response(state: ElectricMotorState,
                     counter_torque: float,
                     downstream_inertia: float,
                     delta_t: float) -> ElectricMotorState:
            assert_type_and_range(counter_torque, downstream_inertia, delta_t,
                                  more_than=0.0)
            assert isinstance(state.input, ElectricIOState)
            assert isinstance(state.output, RotatingIOState)
            j = motor_params.j + downstream_inertia
            v = state.input.voltage
            v_m = state.output.ang_vel * motor_params.ke
            i = (v - v_m) / motor_params.r
            t = motor_params.kt * i
            w_dot = (t - counter_torque) / j
            rpm = state.output.rpm + ang_vel_to_rpm(ang_vel=w_dot * delta_t)
            new_state = ElectricMotorState(input=ElectricIOState(signal_type=signal_type,
                                                                 electric_power=i),
                                           output=RotatingIOState(torque=t,
                                                                  rpm=rpm),
                                           internal=state.internal)
            new_state.input.set_delivering()
            new_state.output.set_receiving()
            return new_state
        return response


class MechanicalToElectric():
    """
    Contains generator methods for electric generators or reversed motors.
    """
    @staticmethod
    def voltage_controlled_first_order(motor_params: DCElectricMotorParams,
                                       signal_type: ElectricSignalType
                                       ) -> Callable[[ElectricGeneratorState|ElectricMotorState,
                                                      float, float, float],
                                                     ElectricGeneratorState|ElectricMotorState]:
        def response(state: ElectricGeneratorState|ElectricMotorState,
                     counter_torque: float,
                     downstream_inertia: float,
                     delta_t: float) -> ElectricGeneratorState|ElectricMotorState:
            assert_type_and_range(counter_torque, downstream_inertia, delta_t,
                                  more_than=0.0)
            assert_type(state,
                        expected_type=(ElectricGeneratorState, ElectricMotorState))
            if isinstance(state, ElectricGeneratorState):
                mech_state = state.input
            else:
                mech_state = state.output
            j = motor_params.j + downstream_inertia
            i = mech_state.torque / motor_params.kt
            v_m = mech_state.ang_vel * motor_params.ke
            v = v_m + motor_params.r * i
            w_dot = (mech_state.torque - counter_torque) / j
            rpm = mech_state.rpm + ang_vel_to_rpm(ang_vel=w_dot * delta_t)
            new_mech_state = RotatingIOState(torque=mech_state.torque,
                                             rpm=rpm)
            new_elec_state = ElectricIOState(signal_type=signal_type,
                                             voltage=v,
                                             current=i)
            if isinstance(state, ElectricGeneratorState):
                gen_state = ElectricGeneratorState(input=new_mech_state,
                                                   output=new_elec_state,
                                                   internal=state.internal)
                gen_state.input.set_delivering()
                gen_state.output.set_receiving()
                return gen_state
            mot_state = ElectricMotorState(input=new_elec_state,
                                           output=new_mech_state,
                                           internal=state.internal)
            mot_state.input.set_receiving()
            mot_state.output.set_delivering()
            return mot_state
        return response
