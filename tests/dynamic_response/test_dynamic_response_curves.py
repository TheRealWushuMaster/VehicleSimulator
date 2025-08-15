"""This module contains test routines for dynamic response curves."""

from components.dynamic_response_curves import MechanicalToMechanical, \
    ElectricToElectric, ElectricToMechanical, MechanicalToElectric, \
    FuelToMechanical
from components.fuel_type import LiquidFuel, GaseousFuel, \
    LIQUID_FUELS, GASEOUS_FUELS
from components.state import LiquidCombustionEngineState, GaseousCombustionEngineState, \
    return_liquid_combustion_engine_state, return_gaseous_combustion_engine_state

fuel_liters_in: float = 0.35
fuel_mass_in: float = 0.48
torque_out: float = 2.3
rpm_out: float = 325.8

def create_liquid_combustion_engine_response(fuel: LiquidFuel) -> FuelToMechanical:
    state = return_liquid_combustion_engine_state(fuel=fuel,
                                                  fuel_liters_in=fuel_liters_in,
                                                  torque_out=torque_out,
                                                  rpm_out=rpm_out)
    response = FuelToMechanical.liquid_combustion_to_mechanical()
    coso = response()

def create_gaseous_combustion_engine_response(fuel: GaseousFuel) -> FuelToMechanical:
    pass

def test_create_forward_mechanical_to_mechanical() -> MechanicalToMechanical:
    pass

def test_create_reverse_mechanical_to_mechanical() -> MechanicalToMechanical:
    pass

def test_create_rectifier_response() -> ElectricToElectric:
    pass

def test_create_inverter_response() -> ElectricToElectric:
    pass

def test_create_forward_electric_motor_response() -> ElectricToMechanical:
    pass

def test_create_reverse_electric_motor_response() -> MechanicalToElectric:
    pass

def test_create_electric_generator_response() -> MechanicalToElectric:
    pass

def test_create_liquid_combustion_engine_response() -> None:
    for fuel in LIQUID_FUELS:
        response = create_liquid_combustion_engine_response(fuel=fuel)
        assert isinstance(response, FuelToMechanical)

def test_create_gaseous_combustion_engine_response() -> None:
    for fuel in GASEOUS_FUELS:
        response = create_gaseous_combustion_engine_response(fuel=fuel)
        assert isinstance(response, FuelToMechanical)
