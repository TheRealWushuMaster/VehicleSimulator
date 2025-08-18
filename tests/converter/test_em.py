"""This module contains routines for testing Electric Motor creation."""

from typing import TypedDict
from components.consumption import return_electric_generator_consumption, \
    return_electric_motor_consumption
from components.limitation import  \
    return_electric_generator_limits, return_electric_motor_limits
from components.motor import ElectricMotor, ElectricGenerator
from tests.dynamic_response.test_dynamic_response import create_electric_motor_response, \
    create_electric_generator_response
from helpers.types import ElectricSignalType


class TestEMParams(TypedDict):
    mass: float
    inertia: float
    motor_eff: float
    gen_eff: float
    max_temp: float
    min_temp: float
    max_voltage_in: float
    min_voltage_in: float
    max_current_in: float
    min_current_in: float
    max_torque_out: float
    min_torque_out: float
    max_rpm_out: float
    min_rpm_out: float


em_defaults: TestEMParams = {"mass": 50.0,
                             "inertia": 5.0,
                             "motor_eff": 0.95,
                             "gen_eff": 0.91,
                             "max_temp": 350.0,
                             "min_temp": 200.0,
                             "max_voltage_in": 300.0,
                             "min_voltage_in": 0.0,
                             "max_current_in": 200.0,
                             "min_current_in": 0.0,
                             "max_torque_out": 100.0,
                             "min_torque_out": 0.0,
                             "max_rpm_out": 5_000.0,
                             "min_rpm_out": 0.0}

# ============================

def create_electric_motor() -> ElectricMotor:
    limits = return_electric_motor_limits(
        abs_max_temp=em_defaults["max_temp"], abs_min_temp=em_defaults["min_temp"],
        abs_max_power_in=em_defaults["max_voltage_in"], abs_min_power_in=em_defaults["min_voltage_in"],
        abs_max_torque_out=em_defaults["max_torque_out"], abs_min_torque_out=em_defaults["min_torque_out"],
        abs_max_rpm_out=em_defaults["max_rpm_out"], abs_min_rpm_out=em_defaults["min_rpm_out"],
        rel_max_temp=lambda s: em_defaults["max_temp"], rel_min_temp=lambda s: em_defaults["min_temp"],
        rel_max_power_in=lambda s: em_defaults["max_voltage_in"], rel_min_power_in=lambda s: em_defaults["min_voltage_in"],
        rel_max_torque_out=lambda s: em_defaults["max_torque_out"], rel_min_torque_out=lambda s: em_defaults["min_torque_out"],
        rel_max_rpm_out=lambda s: em_defaults["max_rpm_out"], rel_min_rpm_out=lambda s: em_defaults["min_rpm_out"]
    )
    consumption = return_electric_motor_consumption(
        motor_efficiency_func=lambda s: em_defaults["motor_eff"],
        generator_efficiency_func=lambda s: em_defaults["gen_eff"]
    )
    dynamic_response = create_electric_motor_response()
    return ElectricMotor(name="Test Electric Motor",
                         mass=em_defaults["mass"],
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         electric_type=ElectricSignalType.AC,
                         inertia=em_defaults["inertia"])

def create_electric_generator() -> ElectricGenerator:
    limits = return_electric_generator_limits(
        abs_max_temp=em_defaults["max_temp"], abs_min_temp=em_defaults["min_temp"],
        abs_max_power_out=em_defaults["max_voltage_in"], abs_min_power_out=em_defaults["min_voltage_in"],
        abs_max_torque_in=em_defaults["max_torque_out"], abs_min_torque_in=em_defaults["min_torque_out"],
        abs_max_rpm_in=em_defaults["max_rpm_out"], abs_min_rpm_in=em_defaults["min_rpm_out"],
        rel_max_temp=lambda s: em_defaults["max_temp"], rel_min_temp=lambda s: em_defaults["min_temp"],
        rel_max_power_out=lambda s: em_defaults["max_voltage_in"], rel_min_power_out=lambda s: em_defaults["min_voltage_in"],
        rel_max_torque_in=lambda s: em_defaults["max_torque_out"], rel_min_torque_in=lambda s: em_defaults["min_torque_out"],
        rel_max_rpm_in=lambda s: em_defaults["max_rpm_out"], rel_min_rpm_in=lambda s: em_defaults["min_rpm_out"]
    )
    consumption = return_electric_generator_consumption(
        generator_efficiency_func=lambda s: em_defaults["gen_eff"]
    )
    dynamic_response = create_electric_generator_response()
    return ElectricGenerator(name="Test Electric Generator",
                             mass=em_defaults["mass"],
                             limits=limits,
                             consumption=consumption,
                             dynamic_response=dynamic_response,
                             inertia=em_defaults["inertia"])

# ============================

def test_create_electric_generator() -> None:
    eg = create_electric_generator()
    assert isinstance(eg, ElectricGenerator)

def test_create_electric_motor() -> None:
    em = create_electric_motor()
    assert isinstance(em, ElectricMotor)
