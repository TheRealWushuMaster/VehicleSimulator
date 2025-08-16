"""This module contains test routines for the state classes."""

from components.state import ElectricIOState, ElectricEnergyStorageState, \
    RotatingIOState, \
    LiquidFuelIOState, GaseousFuelIOState, \
    LiquidFuelStorageState, GaseousFuelStorageState
from components.fuel_type import LiquidFuel, GaseousFuel, \
    LIQUID_FUELS, GASEOUS_FUELS
    
from helpers.types import ElectricSignalType


voltage: float = 10.0
current: float = 3.0
power: float = 30.0
torque: float = 10.0
rpm: float = 200.0
electric_energy: float = 10.0
fuel_mass: float = 5.0
fuel_liters: float = 8.0

# =====================
# ENERGY IO STATES TEST
# =====================

def test_create_ac_electric_io_state() -> ElectricIOState:
    state = ElectricIOState(signal_type=ElectricSignalType.AC,
                            electric_power=power)
    assert isinstance(state, ElectricIOState)
    return state

def test_create_dc_electric_io_state() -> ElectricIOState:
    state = ElectricIOState(signal_type=ElectricSignalType.DC,
                            electric_power=power)
    assert isinstance(state, ElectricIOState)
    return state

def test_create_rotating_io_state() -> RotatingIOState:
    state = RotatingIOState(torque=torque,
                            rpm=rpm)
    assert isinstance(state, RotatingIOState)
    return state

# =========================
# FUEL EXCHANGE STATES TEST
# =========================

def create_liquid_fuel_io_state(fuel: LiquidFuel) -> LiquidFuelIOState:
    state = LiquidFuelIOState(fuel=fuel,
                              fuel_liters=fuel_liters)
    return state

def create_gaseous_fuel_io_state(fuel: GaseousFuel) -> GaseousFuelIOState:
    state = GaseousFuelIOState(fuel=fuel,
                               fuel_mass=fuel_mass)
    return state

def test_create_liquid_fuel_io_state() -> None:
    for fuel in LIQUID_FUELS:
        state = create_liquid_fuel_io_state(fuel=fuel)
        assert isinstance(state, LiquidFuelIOState)

def test_create_gaseous_fuel_io_state() -> None:
    for fuel in GASEOUS_FUELS:
        state = create_gaseous_fuel_io_state(fuel=fuel)
        assert isinstance(state, GaseousFuelIOState)

# ===================
# STORAGE STATES TEST
# ===================

def test_create_electric_energy_storage_state() -> ElectricEnergyStorageState:
    state = ElectricEnergyStorageState(energy=10.0)
    assert isinstance(state, ElectricEnergyStorageState)
    return state

def create_liquid_fuel_storage_state(fuel: LiquidFuel) -> LiquidFuelStorageState:
    state = LiquidFuelStorageState(fuel=fuel,
                                   fuel_liters=fuel_liters)
    return state

def create_gaseous_fuel_storage_state(fuel: GaseousFuel) -> GaseousFuelStorageState:
    state = GaseousFuelStorageState(fuel=fuel,
                                    fuel_mass=fuel_mass)
    return state

def test_create_liquid_fuel_storage_state() -> None:
    for fuel in LIQUID_FUELS:
        state = create_liquid_fuel_storage_state(fuel=fuel)
        assert isinstance(state, LiquidFuelStorageState)

def test_create_gaseous_fuel_storage_state() -> None:
    for fuel in GASEOUS_FUELS:
        state = create_gaseous_fuel_storage_state(fuel=fuel)
        assert isinstance(state, GaseousFuelStorageState)
