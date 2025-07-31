"""This module contains test routines for the EnergyConsumption class."""

from typing import Literal
from components.consumption import ElectricEnergyConsumption, \
    MechanicalEnergyConsumption, Consumption
from components.state import State, IOState, ElectricIOState, \
    RotatingIOState, zero_internal_state
from helpers.functions import torque_to_power

voltage: float = 10.0
current: float = 1.0
torque: float = 5.0
rpm: float = 60.0
efficiency: float = 0.96
delta_t: float = 1.0

def create_electric_energy_consumption() -> ElectricEnergyConsumption:
    return ElectricEnergyConsumption(efficiency_func=lambda s: efficiency)

def create_mechanical_energy_consumption() -> MechanicalEnergyConsumption:
    return MechanicalEnergyConsumption(efficiency_func=lambda s: efficiency)

#============================

def test_electric_energy_consumption() -> None:
    eec = create_electric_energy_consumption()
    assert isinstance(eec, ElectricEnergyConsumption)

def test_mechanical_energy_consumption() -> None:
    mec = create_mechanical_energy_consumption()
    assert isinstance(mec, MechanicalEnergyConsumption)

#============================

def test_create_forward_electric_energy_consumption() -> Consumption:
    cons = Consumption(forward=create_electric_energy_consumption(),
                       reverse=None)
    assert isinstance(cons, Consumption)
    return cons

def test_create_bidirectional_electric_energy_consumption() -> Consumption:
    eec = create_electric_energy_consumption()
    cons = Consumption(forward=eec,
                       reverse=eec)
    assert isinstance(cons, Consumption)
    return cons

#============================

def test_create_forward_mechanical_energy_consumption() -> Consumption:
    cons = Consumption(forward=create_mechanical_energy_consumption(),
                       reverse=None)
    assert isinstance(cons, Consumption)
    return cons

def test_create_bidirectional_mechanical_energy_consumption() -> Consumption:
    eec = create_mechanical_energy_consumption()
    cons = Consumption(forward=eec,
                       reverse=eec)
    assert isinstance(cons, Consumption)
    return cons

#============================

def test_create_electric_to_mechanical_consumption() -> Consumption:
    cons = Consumption(forward=create_mechanical_energy_consumption(),
                       reverse=create_electric_energy_consumption())
    assert isinstance(cons, Consumption)
    return cons

def test_create_mechanical_to_electric_consumption() -> Consumption:
    cons = Consumption(forward=create_electric_energy_consumption(),
                       reverse=create_mechanical_energy_consumption())
    assert isinstance(cons, Consumption)
    return cons

#============================

def forward_consumption(cons: Consumption,
                        receiving_state: IOState,
                        delivering_state: IOState) -> float:
    state = State(input=delivering_state,
                  output=receiving_state,
                  internal=zero_internal_state(),
                  electric_energy_storage=None,
                  fuel_storage=None)
    return cons.compute_forward(state=state,
                                delta_t=delta_t)

def reverse_consumption(cons: Consumption,
                        receiving_state: IOState,
                        delivering_state: IOState) -> float:
    state = State(input=delivering_state,
                  output=receiving_state,
                  internal=zero_internal_state(),
                  electric_energy_storage=None,
                  fuel_storage=None)
    return cons.compute_reverse(state=state,
                                delta_t=delta_t)

def execute_consumption(which: Literal["f", "r"]) -> None:
    eec = (create_electric_energy_consumption(),
           create_electric_energy_consumption(),
           ElectricIOState(voltage=voltage,
                           current=current),
           ElectricIOState(voltage=voltage,
                           current=current),
           voltage * current * delta_t / efficiency)
    mec = (create_mechanical_energy_consumption(),
           create_mechanical_energy_consumption(),
           RotatingIOState(torque=torque,
                           rpm=rpm),
           RotatingIOState(torque=torque,
                           rpm=rpm),
           torque_to_power(torque=torque,
                           rpm=rpm) * delta_t / efficiency)
    for elem in (eec, mec):
        if which == "f":
            cons = Consumption(forward=elem[0])
            result = forward_consumption(cons=cons,
                                         receiving_state=elem[2],
                                         delivering_state=elem[3])
        else:
            cons = Consumption(forward=elem[0],
                               reverse=elem[1])
            result = reverse_consumption(cons=cons,
                                         receiving_state=elem[2],
                                         delivering_state=elem[3])
        assert result == elem[4]

def test_forward_consumption() -> None:
    execute_consumption(which="f")

def test_reverse_consumption() -> None:
    execute_consumption(which="r")
