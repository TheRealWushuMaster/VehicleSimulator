"""This module generates sample power vs RPM and efficiency vs power & RPM curves."""

from dataclasses import dataclass
from math import exp, sqrt
from typing import Callable
from components.state import State, RotatingIOState, ElectricIOState, FuelIOState, \
    IOState
from helpers.functions import assert_type, assert_range, assert_type_and_range, \
    assert_numeric, ang_vel_to_rpm
from helpers.types import MotorOperationPoint, MotorEfficiencyPoint


@dataclass
class DCElectricMotorParams():
    """
    Collection of parameters that describe a DC electric motor.
    """
    r: float    # Armature resistance, in Ohms
    l: float    # Armature inductance, in H
    km: float   # Armature constant, in N.m/A
    kb: float   # Back EMF constant, in V.s/rad
    j: float    # Rotor inertia, in kg.m²
    kf: float    # Viscous friction coefficient, in N.m.s/rad
    max_power: Callable[[State], float] # Maximum power at a defined state

    def __post_init__(self):
        assert_type_and_range(self.l, self.j, self.kb,
                              self.kf, self.km, self.r,
                              more_than=0.0)
        assert_type(self.max_power,
                    expected_type=Callable) # type: ignore[arg-type]


@dataclass
class CombustionEngineParams():
    """
    Collection of parameters that describe an internal combustion engine.
    """
    j: float    # Rotor inertia, in kg.m²
    kf: float    # Viscous friction coefficient, in N.m.s/rad
    tau_delay: float    # Combustion delay, in sec
    idle_rpm: float     # Idle rpms
    max_power: Callable[[State], float] # Maximum power at a defined state

    def __post_init__(self):
        assert_type_and_range(self.j, self.kf, self.tau_delay, self.idle_rpm,
                              more_than=0.0)
        assert_type(self.max_power,
                    expected_type=Callable) # type: ignore[arg-type]


#===========================================


class MechanicalMaxPowerVsRPMCurves():
    """
    Generates maximum power vs RPM curves.
    Only applies to mechanical components.
    """
    @staticmethod
    def constant(max_power: float,
                 max_rpm: float,
                 min_rpm: float) -> Callable[[RotatingIOState], float]:
        """
        Generates a constant maximum power from min_rpm to max_rpm.
        """
        assert_type(max_power, max_rpm, min_rpm,
                    expected_type=float)
        assert_range(max_power, max_rpm, min_rpm,
                     more_than=0.0)
        assert_range(max_rpm,
                     more_than=min_rpm)
        def power_func(state: RotatingIOState) -> float:
            return max_power if min_rpm<=state.rpm<=max_rpm else 0.0
        return power_func

    @staticmethod
    def linear(min_rpm: MotorOperationPoint,
               max_rpm: MotorOperationPoint) -> Callable[[RotatingIOState], float]:
        """Generates a linear maximum power curve from min_rpm to max_rpm."""
        assert_numeric(min_rpm.rpm, max_rpm.rpm, min_rpm.power, max_rpm.power)
        assert_range(min_rpm.rpm, min_rpm.power, max_rpm.power,
                     more_than=0.0)
        assert_range(max_rpm.rpm,
                     more_than=min_rpm.rpm)
        def power_func(state: RotatingIOState) -> float:
            if not min_rpm.rpm <= state.rpm <= max_rpm.rpm:
                return 0.0
            return (max_rpm.power - min_rpm.power) * (state.rpm - min_rpm.rpm) / (max_rpm.rpm - min_rpm.rpm) + min_rpm.power
        return power_func

    @staticmethod
    def ice(min_rpm: MotorOperationPoint,
            max_rpm: MotorOperationPoint,
            peak_rpm: MotorOperationPoint) -> Callable[[RotatingIOState], float]:
        """
        Generates a sample maximum power vs RPM curve for an internal
        combustion engine.
        It is simulated with two Gaussian curves.
        """
        assert_range(peak_rpm.rpm,
                     more_than=min_rpm.rpm,
                     less_than=max_rpm.rpm)
        assert_range(min_rpm.power, max_rpm.power,
                     less_than=peak_rpm.power)
        alpha_1 = 1 / 2 / (peak_rpm.rpm - min_rpm.rpm)**2
        k2 = (min_rpm.power - peak_rpm.power) / (exp(-0.5) - 1)
        k1 = peak_rpm.power - k2
        alpha_2 = 1 / 2 / (peak_rpm.rpm - max_rpm.rpm)**2
        k4 = (max_rpm.power - peak_rpm.power) / (exp(-0.5) - 1)
        k3 = peak_rpm.power - k4
        def power_func(state: RotatingIOState) -> float:
            if not min_rpm.rpm <= state.rpm <= max_rpm.rpm:
                return 0.0
            alpha, a, b = (alpha_1, k1, k2) if state.rpm <= peak_rpm.rpm else (alpha_2, k3, k4)
            return a + b * exp(-alpha * (state.rpm - peak_rpm.rpm)**2)
        return power_func

    @staticmethod
    def em(base_rpm: float,
           max_rpm: float,
           max_power: float) -> Callable[[RotatingIOState], float]:
        """
        Generates a sample power vs RPM curve for an electric motor.
        Maximum power increases linearly up to base_rpm, then remains constant.
        """
        assert_type_and_range(base_rpm, max_power,
                              more_than=0.0)
        assert_type_and_range (max_rpm,
                               more_than=base_rpm)
        def power_func(state: RotatingIOState) -> float:
            if not 0.0 <= state.rpm <= max_rpm:
                return 0.0
            if state.rpm <= base_rpm:
                return max_power * state.rpm / base_rpm
            return max_power
        return power_func


class MechanicalPowerEfficiencyCurves():
    """
    Generates efficiency vs power & RPM curves.
    Only applies to mechanical components.
    """
    @staticmethod
    def constant(efficiency: float,
                 max_rpm: float,
                 min_rpm: float,
                 max_power_vs_rpm: Callable[[RotatingIOState], float]
                 ) -> Callable[[RotatingIOState], float]:
        """
        Generates a constant maximum efficiency from min_rpm to max_rpm.
        """
        assert_numeric(efficiency, max_rpm, min_rpm)
        assert_type(max_power_vs_rpm,
                    expected_type=Callable) # type: ignore[arg-type]
        assert_range(min_rpm,
                     more_than=0.0)
        assert_range(max_rpm,
                     more_than=min_rpm)
        assert_range(efficiency,
                     more_than=0.0,
                     less_than=1.0)
        def efficiency_func(state: RotatingIOState) -> float:
            if not min_rpm <= state.rpm <= max_rpm:
                return 0.0
            if not 0.0 <= state.power <= max_power_vs_rpm(state):
                return 0.0
            return efficiency
        return efficiency_func

    @staticmethod
    def linear(max_efficiency: float,
               min_efficiency: float,
               max_rpm: float,
               min_rpm: float,
               max_power_vs_rpm: Callable[[float], float],
               power_max_eff: float,
               rpm_max_eff: float,
               power_falloff_rate: float,
               rpm_falloff_rate: float) -> Callable[[RotatingIOState], float]:
        """Generates a linear maximum efficiency from min_rpm to max_rpm."""
        assert_type(max_efficiency, min_efficiency, max_rpm, min_rpm,
                    power_max_eff, rpm_max_eff,
                    power_falloff_rate, rpm_falloff_rate,
                    expected_type=float)
        assert_type(max_power_vs_rpm,
                    expected_type=Callable) # type: ignore[arg-type]
        assert_range(min_rpm,
                     more_than=0.0)
        assert_range(max_rpm,
                     more_than=min_rpm)
        assert_range(rpm_max_eff,
                     more_than=min_rpm,
                     less_than=max_rpm)
        assert_range(max_efficiency,
                     more_than=0.0,
                     less_than=1.0)
        assert_range(min_efficiency,
                     more_than=0.0,
                     less_than=max_efficiency)
        def efficiency_func(state: RotatingIOState) -> float:
            if not min_rpm <= state.rpm <= max_rpm:
                return 0.0
            if not 0.0 <= state.power <= max_power_vs_rpm(state.rpm):
                return 0.0
            power_range = max_power_vs_rpm(rpm_max_eff)
            rpm_range = max_rpm - min_rpm
            power_distance = abs(state.power - power_max_eff) / power_range
            rpm_distance = abs(state.rpm - rpm_max_eff) / rpm_range
            elliptical_distance = sqrt((power_distance*power_falloff_rate)**2 + (rpm_distance*rpm_falloff_rate)**2)
            return max(max_efficiency * max(0.0, 1.0 - elliptical_distance), min_efficiency)
        return efficiency_func

    @staticmethod
    def gaussian(max_eff: MotorEfficiencyPoint,
                 min_eff: float,
                 falloff_rpm: float,
                 falloff_power: float,
                 max_power_vs_rpm: Callable[[RotatingIOState], float],
                 min_rpm: float,
                 max_rpm: float) -> Callable[[RotatingIOState], float]:
        """
        Generates a sample efficiency vs power & rpm for internal
        combustion engines and electric motors.
        It is simulated using a bivariate Gaussian curve.
        The values of `falloff_rpm` and `falloff_power` should be much
        smaller for electric motors than for ICEs.
        """
        assert_type(falloff_rpm, falloff_power, min_rpm, max_rpm,
                    expected_type=float)
        assert_type(max_power_vs_rpm,
                    expected_type=Callable) # type: ignore[arg-type]
        assert_range(falloff_rpm, falloff_power,
                     more_than=0.0)
        assert_range(min_eff,
                     more_than=0.0,
                     less_than=max_eff.efficiency)
        def efficiency_func(state: RotatingIOState) -> float:
            if not min_rpm <= state.rpm <= max_rpm or \
               not 0.0 <= state.power <= max_power_vs_rpm(state):
                return 0.0
            return max(max_eff.efficiency * exp(-falloff_rpm*(state.rpm-max_eff.rpm)**2 - falloff_power*(state.power-max_eff.power)**2), min_eff)
        return efficiency_func


class MechanicalDynamicResponse():
    """
    Generates a dynamic response model for motors and engines
    for use when updating states in the simulation.
    """
    @staticmethod
    def ice(ice_params: CombustionEngineParams) -> Callable[[State, float, float], State]:
        """
        Returns a dynamic model for a combustion engine.
        """
        raise NotImplementedError

    @staticmethod
    def dc_em(em_params: DCElectricMotorParams
              ) -> Callable[[State, float, float, float], IOState]:
        """
        Returns a dynamic model for a DC electric motor
        when it's acting as a motor.
        """
        #i_dot = (-(em_params.r * i + em_params.kb * w) + v) / em_params.l
        def dc_em_dynamic_response(state: State,
                                   control: float,
                                   delta_t: float,
                                   downstream_inertia: float) -> IOState:
            assert isinstance(state.input, ElectricIOState)
            assert isinstance(state.output, RotatingIOState)
            j = em_params.j + downstream_inertia
            w_dot = (em_params.km * state.input.current - em_params.kf * state.output.ang_vel) / j
            new_w = state.output.ang_vel + w_dot * delta_t
            return RotatingIOState(power=0.0,
                                   rpm=ang_vel_to_rpm(ang_vel=new_w))
        return dc_em_dynamic_response

    @staticmethod
    def dc_em_reverse(em_params: DCElectricMotorParams
                      ) -> Callable[[State, float, float, float,
                                     float, float], IOState]:
        """
        Returns a dynamic model for a DC electric motor
        when it's acting as a generator.
        """
        def dc_em_dynamic_response(state: State,
                                   control: float,
                                   delta_t: float,
                                   w_dot: float,
                                   w_dot_dot: float,
                                   upstream_inertia: float) -> IOState:
            assert isinstance(state.input, ElectricIOState)
            assert isinstance(state.output, RotatingIOState)
            j = em_params.j + upstream_inertia
            i = (j * w_dot + em_params.kf * state.output.ang_vel) / em_params.km
            i_dot = (j * w_dot_dot + em_params.kf * w_dot) / em_params.km
            v = em_params.kb * state.output.ang_vel + em_params.r * i + em_params.l * i_dot
            return ElectricIOState(delivering=True,
                                   receiving=False,
                                   power=v*i,
                                   current=i)
        return dc_em_dynamic_response
