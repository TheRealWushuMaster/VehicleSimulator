"""This module contains test routines for the full state classes."""

from components.state import FullStateNoInput, \
        FullStateWithInput, \
        FullStateElectricEnergyStorageNoInput, \
        FullStateElectricEnergyStorageWithInput, \
        FullStateFuelStorageNoInput
from components.fuel_type import Gasoline
from tests.state.test_state import create_liquid_fuel_io_state, test_create_dc_electric_io_state, \
    test_create_electric_energy_storage_state, create_liquid_fuel_storage_state

def test_create_full_state_no_input() -> None:
    state = FullStateNoInput(output=create_liquid_fuel_io_state(fuel=Gasoline()),
                             internal=None)
    assert isinstance(state, FullStateNoInput)

def test_create_full_state_with_input() -> None:
    state = FullStateWithInput(input=test_create_dc_electric_io_state(),
                               output=test_create_dc_electric_io_state(),
                               internal=None)
    assert isinstance(state, FullStateWithInput)

def test_create_full_state_electric_storage_no_input() -> None:
    state = FullStateElectricEnergyStorageNoInput(output=test_create_dc_electric_io_state(),
                                                  internal=None,
                                                  electric_energy_storage=test_create_electric_energy_storage_state())
    assert isinstance(state, FullStateElectricEnergyStorageNoInput)

def test_create_full_state_electric_storage_with_input() -> None:
    state = FullStateElectricEnergyStorageWithInput(input=test_create_dc_electric_io_state(),
                                                    output=test_create_dc_electric_io_state(),
                                                    internal=None,
                                                    electric_energy_storage=test_create_electric_energy_storage_state())
    assert isinstance(state, FullStateElectricEnergyStorageWithInput)

def test_create_full_state_fuel_storage_no_input() -> None:
    state = FullStateFuelStorageNoInput(output=create_liquid_fuel_io_state(fuel=Gasoline()),
                                        internal=None,
                                        fuel_storage=create_liquid_fuel_storage_state(fuel=Gasoline()))
    assert isinstance(state, FullStateFuelStorageNoInput)
