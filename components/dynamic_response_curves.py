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
import matplotlib.pyplot as plt


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
                                       ) -> Callable[[ElectricGeneratorState, float,
                                                      float, float], ElectricMotorState]:
        def response(state: ElectricMotorState,
                     counter_torque: float,
                     downstream_inertia: float,
                     delta_t: float) -> ElectricMotorState:
            assert_type_and_range(counter_torque, downstream_inertia, delta_t,
                                  more_than=0.0)
            assert isinstance(state.input, ElectricIOState)
            assert isinstance(state.output, RotatingIOState)
            j = motor_params.j + downstream_inertia
            i = state.output.torque / motor_params.kt
            v_m = state.output.ang_vel * motor_params.ke
            v = v_m + motor_params.r * i
            w_dot = (state.output.torque - counter_torque) / j
            rpm = state.output.rpm + ang_vel_to_rpm(ang_vel=w_dot * delta_t)
            new_state = ElectricMotorState(input=ElectricIOState(signal_type=signal_type,
                                                                 voltage=v,
                                                                 current=i),
                                           output=RotatingIOState(torque=state.output.torque,
                                                                  rpm=rpm),
                                           internal=state.internal)
            new_state.input.set_receiving()
            new_state.output.set_delivering()
            return new_state
        return response

params = DCElectricMotorParams(r=0.1,
                               kt=0.02,
                               ke=0.02,
                               j=0.02,
                               max_power=lambda s: 1.0)
resp = ElectricToMechanical.first_order_voltage_controlled(motor_params=params)
st = State(input=ElectricIOState(voltage=0.0,
                                 current=0.0),
           output=RotatingIOState(torque=1.0,
                                  rpm=0.0))
results: list[float] = []
for _ in range(50):
    st = resp(state=st,
              counter_torque=0.5,
              downstream_inertia=0.0,
              delta_t=1.0,
              forward=False)
    assert isinstance(st, State)
    assert isinstance(st.input, ElectricIOState)
    assert isinstance(st.output, RotatingIOState)
    results.append(st.efficiency)
plt.plot(results)
plt.show()
