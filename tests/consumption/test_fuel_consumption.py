"""This module contains test routines for the FuelConsumption class."""

from typing import Literal
from components.consumption import Consumption, FuelConsumption
from components.state import State, FuelIOState, LiquidFuelIOState, \
    GaseousFuelIOState, zero_internal_state, RotatingIOState
from components.fuel_type import Biodiesel, Diesel, Ethanol, HydrogenGas, \
    HydrogenLiquid, Gasoline, Methane, Methanol

cons_per_sec: float = 0.1
delta_t: float = 1.0
torque: float = 5.0
rpm: float = 100.0

liquid_fuels = [Biodiesel, Diesel, Ethanol, HydrogenLiquid, Gasoline, Methanol]
gaseous_fuels = [HydrogenGas, Methane]

def fuel_cons_func(state: State) -> float:
    assert isinstance(state.output, RotatingIOState)
    return state.output.torque * state.output.rpm * cons_per_sec

def create_fuel_consumption() -> FuelConsumption:
    return FuelConsumption(fuel_consumption_func=fuel_cons_func)

def test_create_fuel_consumption() -> None:
    fc = create_fuel_consumption()
    assert isinstance(fc, FuelConsumption)

def test_create_forward_fuel_consumption() -> Consumption:
    cons = Consumption(forward=create_fuel_consumption())
    assert isinstance(cons, Consumption)
    return cons

def test_create_bidirectional_fuel_consumption() -> Consumption:
    fc1 = create_fuel_consumption()
    fc2 = create_fuel_consumption()
    cons = Consumption(forward=fc1,
                       reverse=fc2)
    assert isinstance(cons, Consumption)
    return cons

def forward_consumption(cons: Consumption,
                        receiving_state: RotatingIOState,
                        delivering_state: LiquidFuelIOState|GaseousFuelIOState) -> float:
    assert isinstance(delivering_state, (LiquidFuelIOState, GaseousFuelIOState))
    state = State(input=delivering_state,
                  output=receiving_state,
                  internal=zero_internal_state(),
                  electric_energy_storage=None,
                  fuel_storage=None)
    return cons.compute_forward(state=state,
                                delta_t=delta_t)

def reverse_consumption(cons: Consumption,
                        receiving_state: RotatingIOState,
                        delivering_state: FuelIOState) -> float:
    state = State(input=delivering_state,
                  output=receiving_state,
                  internal=zero_internal_state(),
                  electric_energy_storage=None,
                  fuel_storage=None)
    return cons.compute_reverse(state=state,
                                delta_t=delta_t)

def execute_consumption(which: Literal["f", "r"]) -> None:
    receiving_state = RotatingIOState(torque=torque,
                                      rpm=rpm)
    if which == "f":
        cons = Consumption(forward=create_fuel_consumption())
        consumption = forward_consumption
    else:
        cons = Consumption(forward=create_fuel_consumption(),
                           reverse=create_fuel_consumption())
        consumption = reverse_consumption
    for fuel in liquid_fuels:
        delivering_state = LiquidFuelIOState(fuel=fuel(),
                                             fuel_liters=0.0)
        result = consumption(cons=cons,
                             receiving_state=receiving_state,
                             delivering_state=delivering_state)
        assert result == torque * rpm * cons_per_sec * delta_t
    for fuel in gaseous_fuels:
        delivering_state = GaseousFuelIOState(fuel=fuel(),
                                              fuel_mass=0.0)
        result = consumption(cons=cons,
                             receiving_state=receiving_state,
                             delivering_state=delivering_state)
        assert result == torque * rpm * cons_per_sec * delta_t

def test_forward_consumption() -> None:
    execute_consumption(which="f")

def test_reverse_consumption() -> None:
    execute_consumption(which="r")
