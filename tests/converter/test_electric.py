"""This module contains test routines
for electric to electric converters."""

from components.electric_converters import Inverter, Rectifier
from components.consumption import return_electric_inverter_consumption, \
    return_electric_rectifier_consumption
from components.dynamic_response import InverterDynamicResponse, \
    RectifierDynamicResponse
from components.dynamic_response_curves import \
    ElectricToElectric
from components.limitation import return_electric_to_electric_limits

mass: float = 50.0
max_power: float = 1_000.0
nominal_voltage_in: float = 400.0
nominal_voltage_out: float = 360.0
efficiency: float = 0.94
voltage_gain: float = 2.0
abs_max_temp: float = 300.0
abs_min_temp: float = 200.0
abs_max_power_in: float = 3_000.0
abs_min_power_in: float = 0.0
abs_max_power_out: float = 2_500.0
abs_min_power_out: float = 0.0
def rel_max_temp(s): return abs_max_temp
def rel_min_temp(s): return abs_min_temp
def rel_max_power_in(s): return abs_max_power_in
def rel_min_power_in(s): return abs_min_power_in
def rel_max_power_out(s): return abs_max_power_out
def rel_min_power_out(s): return abs_min_power_out
limits = return_electric_to_electric_limits(
    abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
    abs_max_power_in=abs_max_power_in, abs_min_power_in=abs_min_power_in,
    abs_max_power_out=abs_max_power_out, abs_min_power_out=abs_min_power_out,
    rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
    rel_max_power_in=rel_max_power_in, rel_min_power_in=rel_min_power_in,
    rel_max_power_out=rel_max_power_out, rel_min_power_out=rel_min_power_out,
    )
inverter_eff_func = return_electric_inverter_consumption(
    efficiency_func=lambda s: efficiency
)
rectifier_eff_func = return_electric_rectifier_consumption(
    efficiency_func=lambda s: efficiency
)

def test_create_inverter() -> None:
    dynamic_response = InverterDynamicResponse(
        forward_response=ElectricToElectric.inverter_response(
            efficiency=efficiency
        )
    )
    inv = Inverter(name="Test Inverter",
                   mass=mass,
                   max_power=max_power,
                   limits=limits,
                   eff_func=inverter_eff_func,
                   dynamic_response=dynamic_response,
                   nominal_voltage_in=nominal_voltage_in,
                   nominal_voltage_out=nominal_voltage_out)
    assert isinstance(inv, Inverter)

def test_create_rectifier() -> None:
    dynamic_response = RectifierDynamicResponse(
        forward_response=ElectricToElectric.rectifier_response(
            efficiency=efficiency
        )
    )
    inv = Rectifier(name="Test Inverter",
                    mass=mass,
                    max_power=max_power,
                    limits=limits,
                    eff_func=rectifier_eff_func,
                    dynamic_response=dynamic_response,
                    nominal_voltage_in=nominal_voltage_in,
                    nominal_voltage_out=nominal_voltage_out)
    assert isinstance(inv, Rectifier)
