"""This module contains test routines for the fuel cell class."""

from components.fuel_cell import FUEL_CELL_TYPES
from components.limitation import return_fuel_cell_limits

nominal_voltage: float = 200.0
max_power: float = 20_000.0
abs_max_temp: float = 400.0
abs_min_temp: float = 200.0
abs_max_fuel_mass_in: float = 1.0
abs_min_fuel_mass_in: float = 0.0
abs_max_power_out: float = 20_000.0
abs_min_power_out: float = 0.0
def rel_max_temp(s):
    return abs_max_temp
def rel_min_temp(s):
    return abs_min_temp
def rel_max_fuel_mass_in(s):
    return abs_max_fuel_mass_in
def rel_min_fuel_mass_in(s):
    return abs_min_fuel_mass_in
def rel_max_power_out(s):
    return abs_max_power_out
def rel_min_power_out(s):
    return abs_min_power_out

limits = return_fuel_cell_limits(
    abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
    abs_max_fuel_mass_in=abs_max_fuel_mass_in, abs_min_fuel_mass_in=abs_min_fuel_mass_in,
    abs_max_power_out=abs_max_power_out, abs_min_power_out=abs_min_power_out,
    rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
    rel_max_fuel_mass_in=rel_max_fuel_mass_in, rel_min_fuel_mass_in=rel_min_fuel_mass_in,
    rel_max_power_out=rel_max_power_out, rel_min_power_out=rel_min_power_out
)

def test_create_fuel_cells() -> None:
    for fc_type in FUEL_CELL_TYPES:
        fc = fc_type(name="Test fuel cell",
                     nominal_voltage=nominal_voltage,
                     limits=limits,
                     max_power=max_power)
        assert isinstance(fc, fc_type)
