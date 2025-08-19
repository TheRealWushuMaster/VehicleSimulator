"""This module contains routines for testing ICE creation."""

from typing import TypedDict
from components.consumption import return_combustion_engine_consumption
from components.dynamic_response import LiquidCombustionDynamicResponse, \
    GaseousCombustionDynamicResponse
from components.dynamic_response_curves import FuelToMechanical
from components.fuel_type import LiquidFuel, GaseousFuel, \
    LIQUID_FUELS, GASEOUS_FUELS
from components.limitation import return_liquid_combustion_engine_limits, \
    return_gaseous_combustion_engine_limits
from components.motor import LiquidInternalCombustionEngine, \
    GaseousInternalCombustionEngine
from components.state import FullStateWithInput, \
    LiquidCombustionEngineState, GaseousCombustionEngineState, \
    return_liquid_combustion_engine_state


class TestICEParams(TypedDict):
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

def t_func(s: FullStateWithInput, t: float) -> FullStateWithInput:
    return return_liquid_combustion_engine_state(fuel=LIQUID_FUELS[0])

def l_test_func(s: LiquidCombustionEngineState) -> float:
    return 2.0

def g_test_func(s: GaseousCombustionEngineState) -> float:
    return 2.0

ice_defaults: TestICEParams = {"mass": 50.0,
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

def create_liquid_combustion_engine(fuel: LiquidFuel) -> LiquidInternalCombustionEngine:
    limits = return_liquid_combustion_engine_limits(
        abs_max_temp=2.0, abs_min_temp=1.0,
        abs_max_fuel_liters_in=2.0, abs_min_fuel_liters_in=1.0,
        abs_max_torque_out=2.0, abs_min_torque_out=1.0,
        abs_max_rpm_out=2.0, abs_min_rpm_out=1.0,
        rel_max_temp=l_test_func, rel_min_temp=l_test_func,
        rel_max_fuel_liters_in=l_test_func, rel_min_fuel_liters_in=l_test_func,
        rel_max_torque_out=l_test_func, rel_min_torque_out=l_test_func,
        rel_max_rpm_out=l_test_func, rel_min_rpm_out=l_test_func
    )
    consumption = return_combustion_engine_consumption(
        fuel_consumption_func=lambda s: 1.0
    )
    dynamic_response = LiquidCombustionDynamicResponse(
        forward_response=FuelToMechanical.liquid_combustion_to_mechanical())
    return LiquidInternalCombustionEngine(
        name="Test Liquid Combustion Engine",
        mass=ice_defaults["mass"],
        limits=limits,
        consumption=consumption,
        dynamic_response=dynamic_response,
        inertia=ice_defaults["inertia"],
        fuel=fuel
    )

def create_gaseous_combustion_engine(fuel: GaseousFuel) -> GaseousInternalCombustionEngine:
    limits = return_gaseous_combustion_engine_limits(
        abs_max_temp=2.0, abs_min_temp=1.0,
        abs_max_fuel_mass_in=2.0, abs_min_fuel_mass_in=1.0,
        abs_max_torque_out=2.0, abs_min_torque_out=1.0,
        abs_max_rpm_out=2.0, abs_min_rpm_out=1.0,
        rel_max_temp=g_test_func, rel_min_temp=g_test_func,
        rel_max_fuel_mass_in=g_test_func, rel_min_fuel_mass_in=g_test_func,
        rel_max_torque_out=g_test_func, rel_min_torque_out=g_test_func,
        rel_max_rpm_out=g_test_func, rel_min_rpm_out=g_test_func
    )
    consumption = return_combustion_engine_consumption(
        fuel_consumption_func=lambda s: 1
    )
    dynamic_response = GaseousCombustionDynamicResponse(
        forward_response=FuelToMechanical.gaseous_combustion_to_mechanical()
    )
    return GaseousInternalCombustionEngine(
        name="Test Gaseous Combustion Engine",
        mass=ice_defaults["mass"],
        limits=limits,
        consumption=consumption,
        dynamic_response=dynamic_response,
        inertia=ice_defaults["inertia"],
        fuel=fuel
    )

#============================

def test_create_liquid_combustion_engine() -> None:
    for fuel in LIQUID_FUELS:
        liquid_ice = create_liquid_combustion_engine(fuel=fuel)
        assert isinstance(liquid_ice, LiquidInternalCombustionEngine)

def test_create_gaseous_combustion_engine() -> None:
    for fuel in GASEOUS_FUELS:
        gaseous_ice = create_gaseous_combustion_engine(fuel=fuel)
        assert isinstance(gaseous_ice, GaseousInternalCombustionEngine)
