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


@dataclass
class DCElectricMotorParams():
    """
    Parameters that describe a first-order DC electric motor.
    """
    r: float    # Armature resistance, in Ohms
    kt: float   # Torque constant, in N.m/A
    ke: float   # Back EMF constant, in V.s/rad
    j: float    # Rotor inertia, in kg.m²
    limit: ElectricMotorLimits  # Maximum power at a defined state

    def __post_init__(self):
        assert_type_and_range(self.j, self.kt,
                              self.ke, self.r,
                              more_than=0.0)
        assert_type(self.limit,
                    expected_type=ElectricMotorLimits)


class MechanicalToMechanical():
    """
    Contains generator methods for purely mechanical components.
    """
    @staticmethod
    def gearbox_ideal_response(gear_ratio: float, efficiency: float=1.0
                               ) -> Callable[[PureMechanicalState],
                                             PureMechanicalState]:
        """
        Generates a response for a stateless mechanical component.
        Receives an input `torque` and `rpm` (in a `State` object)
        and outputs `rpm` affected by `gear_ratio` and `torque` 
        affected by `efficiency` (also in a `State` object).
        """
        assert_type_and_range(gear_ratio,
                              more_than=0.0)
        assert_type_and_range(efficiency,
                              more_than=0.0,
                              less_than=1.0,
                              include_more=False)
        def response(state: PureMechanicalState,
                     forward: bool=True) -> PureMechanicalState:
            assert isinstance(state, PureMechanicalState)
            inp = state.input if forward else state.output
            output = RotatingIOState(torque=inp.torque * gear_ratio * efficiency,
                                     rpm=inp.rpm / gear_ratio)
            return PureMechanicalState(input=inp if forward else output,
                                       output=output if forward else inp,
                                       internal=state.internal)
        return response


class ElectricToMechanical():
    """
    Contains generator methods for electric motors.
    """
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
                                                                    voltage=state.input.voltage,
                                                                    current=i),
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
