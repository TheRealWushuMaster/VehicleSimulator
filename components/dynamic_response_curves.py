"""This module contains several dynamic response curves for different components."""

from dataclasses import dataclass
from typing import Callable
from components.state import State, ElectricIOState, RotatingIOState
from helpers.functions import assert_type, assert_type_and_range, \
    ang_vel_to_rpm
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
    max_power: Callable[[State], float]  # Maximum power at a defined state

    def __post_init__(self):
        assert_type_and_range(self.j, self.kt,
                              self.ke, self.r,
                              more_than=0.0)
        assert_type(self.max_power,
                    expected_type=Callable)  # type: ignore[arg-type]


class MechanicalToMechanical():
    """
    Contains generator methods for purely mechanical components.
    """
    @staticmethod
    def gearbox_ideal_response(gear_ratio: float, efficiency: float=1.0
                               ) -> Callable[[State, bool], State]:
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
        def response(state: State,
                     forward: bool=True) -> State:
            assert isinstance(state.input, RotatingIOState)
            assert isinstance(state.output, RotatingIOState)
            inp = state.input if forward else state.output
            output = RotatingIOState(torque=inp.torque * gear_ratio * efficiency,
                                     rpm=inp.rpm / gear_ratio)
            return State(input=inp if forward else output,
                         output=output if forward else inp,
                         internal=state.internal,
                         electric_energy_storage=state.electric_energy_storage,
                         fuel_storage=state.fuel_storage)
        return response

class ElectricToMechanical():
    """
    Contains generator methods for electric motors.
    """
    @staticmethod
    def instant_conversion(rotor_inertia: float) -> Callable[[State, float, bool], State]:
        """
        Returns a response that reacts instantly.
        """
        assert_type_and_range(rotor_inertia,
                              more_than=0.0,
                              include_more=False)
        def response(state: State,
                     downstream_inertia: float,
                     forward: bool=True) -> State:
            assert isinstance(state.input, ElectricIOState)
            assert isinstance(state.output, RotatingIOState)
            assert isinstance(forward, bool)
            assert_type_and_range(downstream_inertia,
                                  more_than=0.0,
                                  include_more=False)
        return response


    @staticmethod
    def first_order_voltage_controlled(motor_params: DCElectricMotorParams
                                       ) -> Callable[[State, float, float, float, bool], State]:
        def response(state: State,
                     counter_torque: float,
                     downstream_inertia: float,
                     delta_t: float,
                     forward: bool=True) -> State:
            assert_type_and_range(counter_torque, downstream_inertia, delta_t,
                                  more_than=0.0)
            assert isinstance(state.input, ElectricIOState)
            assert isinstance(state.output, RotatingIOState)
            j = motor_params.j + downstream_inertia
            if forward:
                v = state.input.voltage
                v_m = state.output.ang_vel * motor_params.ke
                i = (v - v_m) / motor_params.r
                t = motor_params.kt * i
                w_dot = (t - counter_torque) / j
                rpm = state.output.rpm + ang_vel_to_rpm(ang_vel=w_dot * delta_t)
                inp = ElectricIOState(voltage=state.input.voltage,
                                      current=i)
                inp.set_delivering()
                outp = RotatingIOState(torque=t,
                                       rpm=rpm)
                outp.set_receiving()
                return State(input=inp,
                             output=outp)
            i = state.output.torque / motor_params.kt
            v_m = state.output.ang_vel * motor_params.ke
            v = v_m + motor_params.r * i
            w_dot = (state.output.torque - counter_torque) / j
            rpm = state.output.rpm + ang_vel_to_rpm(ang_vel=w_dot * delta_t)
            inp = ElectricIOState(voltage=v,
                                  current=i)
            inp.set_receiving()
            outp = RotatingIOState(torque=state.output.torque,
                                   rpm=rpm)
            outp.set_delivering()
            return State(input=inp,
                         output=outp)
        return response


class MechanicalToElectric():
    """
    Contains generator methods for electric generators or reversed motors.
    """
    @staticmethod
    def instant_conversion() -> Callable[[State], State]:
        raise NotImplementedError

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
