"""This module contains routines for testing ICE creation."""

from typing import TypedDict
from components.fuel_type import Biodiesel, Diesel, Ethanol, Gasoline, \
    HydrogenGas, HydrogenLiquid, Methane, Methanol, Fuel
from components.motor import InternalCombustionEngine
from components.motor_curves import MechanicalMaxPowerVsRPMCurves, \
    MechanicalPowerEfficiencyCurves
from components.state import MechanicalState, zero_mechanical_state


class TestICEParams(TypedDict):
    mass: float
    max_power: float
    min_rpm: float
    max_rpm: float
    efficiency: float
    state: MechanicalState


ice_defaults: TestICEParams = {"mass": 50.0,
                               "max_power": 50_000.0,
                               "min_rpm": 800.0,
                               "max_rpm": 5_000.0,
                               "efficiency": 0.35,
                               "state": zero_mechanical_state()}

def create_ice(fuel: Fuel,
               mass: float=ice_defaults["mass"],
               max_power: float=ice_defaults["max_power"],
               state: MechanicalState=ice_defaults["state"]) -> InternalCombustionEngine:
    power_func = MechanicalMaxPowerVsRPMCurves.constant(max_power=max_power,
                                                        max_rpm=ice_defaults["max_rpm"],
                                                        min_rpm=ice_defaults["min_rpm"])
    eff_func = MechanicalPowerEfficiencyCurves.constant(efficiency=ice_defaults["efficiency"],
                                                        max_rpm=ice_defaults["max_rpm"],
                                                        min_rpm=ice_defaults["min_rpm"],
                                                        max_power_vs_rpm=power_func)
    ice = InternalCombustionEngine(name="Test ICE",
                                   mass=mass,
                                   max_power=max_power,
                                   eff_func=eff_func,
                                   state=state,
                                   power_func=power_func,
                                   fuel=fuel)
    return ice

#============================

def test_create_biodiesel_engine() -> None:
    ice = create_ice(fuel=Biodiesel())
    assert isinstance(ice, InternalCombustionEngine)

def test_create_diesel_engine() -> None:
    ice = create_ice(fuel=Diesel())
    assert isinstance(ice, InternalCombustionEngine)

def test_create_ethanol_engine() -> None:
    ice = create_ice(fuel=Ethanol())
    assert isinstance(ice, InternalCombustionEngine)

def test_create_gasoline_engine() -> None:
    ice = create_ice(fuel=Gasoline())
    assert isinstance(ice, InternalCombustionEngine)

def test_create_hydrogen_gas_engine() -> None:
    ice = create_ice(fuel=HydrogenGas())
    assert isinstance(ice, InternalCombustionEngine)

def test_create_hydrogen_liquid_engine() -> None:
    ice = create_ice(fuel=HydrogenLiquid())
    assert isinstance(ice, InternalCombustionEngine)

def test_create_methane_engine() -> None:
    ice = create_ice(fuel=Methane())
    assert isinstance(ice, InternalCombustionEngine)

def test_create_methanol_engine() -> None:
    ice = create_ice(fuel=Methanol())
    assert isinstance(ice, InternalCombustionEngine)
