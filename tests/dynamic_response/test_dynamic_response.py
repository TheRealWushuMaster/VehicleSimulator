"""This module contains test routines for the dynamic response classes."""

from components.consumption import ElectricMotorConsumption, \
    ElectricGeneratorConsumption, CombustionEngineConsumption
from components.dynamic_response import ElectricMotorDynamicResponse, \
    ElectricGeneratorDynamicResponse, LiquidCombustionDynamicResponse, \
    GaseousCombustionDynamicResponse, PureMechanicalDynamicResponse, \
    RectifierDynamicResponse, InverterDynamicResponse
from components.dynamic_response_curves import MechanicalToMechanical, \
    ElectricToElectric, ElectricToMechanical, MechanicalToElectric, \
    FuelToMechanical
from components.fuel_type import LIQUID_FUELS, GASEOUS_FUELS
from components.limitation import return_electric_motor_limits, \
    return_electric_generator_limits, return_liquid_combustion_engine_limits
from components.state import return_electric_motor_state, \
    return_electric_generator_state, return_liquid_combustion_engine_state
from helpers.functions import ang_vel_to_rpm, torque_to_power
from helpers.types import ElectricSignalType

nominal_voltage: float = 300.0
power_in: float = 2_000.0
power_out: float = 2_000.0
torque_in: float = 5.0
torque_out: float = 5.0
rpm_in: float = 2_500.0
rpm_out: float = 2_500.0
delta_t: float = 0.1
voltage_gain: float = 2.0
efficiency: float = 0.92
gear_ratio: float = 2.32
load_torque: float = 4.03
inertia: float = 6.2
control_signal: float = 0.68
fuel_liters_in: float = 0.23
fuel_mass_in: float = 0.17
abs_max_temp: float = 400.0
abs_min_temp: float = 200.0
abs_max_power_in: float = 10_000.0
abs_min_power_in: float = 0.0
abs_max_power_out: float = 10_000.0
abs_min_power_out: float = 0.0
abs_max_torque_in: float = 10.0
abs_min_torque_in: float = 0.0
abs_max_torque_out: float = 10.0
abs_min_torque_out: float = 0.0
abs_max_rpm_in: float = 6_000.0
abs_min_rpm_in: float = 0.0
abs_max_rpm_out: float = 6_000.0
abs_min_rpm_out: float = 0.0
abs_max_fuel_liters_in: float = 0.45
abs_min_fuel_liters_in: float = 0.0
rel_max_temp = lambda s: abs_max_temp
rel_min_temp = lambda s: abs_min_temp
rel_max_power_in = lambda s: abs_max_power_in
rel_min_power_in = lambda s: abs_min_power_in
rel_max_power_out = lambda s: abs_max_power_out
rel_min_power_out = lambda s: abs_min_power_out
rel_max_torque_in = lambda s: abs_max_torque_in
rel_min_torque_in = lambda s: abs_min_torque_in
rel_max_torque_out = lambda s: abs_max_torque_out
rel_min_torque_out = lambda s: abs_min_torque_out
rel_max_rpm_in = lambda s: abs_max_rpm_in
rel_min_rpm_in = lambda s: abs_min_rpm_in
rel_max_rpm_out = lambda s: abs_max_rpm_out
rel_min_rpm_out = lambda s: abs_min_rpm_out
rel_max_fuel_liters_in = lambda s: abs_max_fuel_liters_in
rel_min_fuel_liters_in = lambda s: abs_min_fuel_liters_in

def test_create_electric_motor_response() -> None:
    response = ElectricMotorDynamicResponse(forward_response=ElectricToMechanical.forward_driven_first_order(),
                                            reverse_response=MechanicalToElectric.reversed_motor())
    assert isinstance(response, ElectricMotorDynamicResponse)
    em_consumption = ElectricMotorConsumption(in_to_out_efficiency_func=lambda s: efficiency,
                                              out_to_in_efficiency_func=lambda s: efficiency)
    em_limits = return_electric_motor_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                             abs_max_power_in=abs_max_power_in, abs_min_power_in=abs_min_power_in,
                                             abs_max_torque_out=abs_max_torque_out, abs_min_torque_out=abs_min_torque_out,
                                             abs_max_rpm_out=abs_max_rpm_out, abs_min_rpm_out=abs_min_rpm_out,
                                             rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                             rel_max_power_in=rel_max_power_in, rel_min_power_in=rel_min_power_in,
                                             rel_max_torque_out=rel_max_torque_out, rel_min_torque_out=rel_min_torque_out,
                                             rel_max_rpm_out=rel_max_rpm_out, rel_min_rpm_out=rel_min_rpm_out)
    initial_state = return_electric_motor_state(signal_type=ElectricSignalType.AC,
                                                nominal_voltage=nominal_voltage,
                                                power_in=power_in,
                                                torque_out=torque_out,
                                                rpm_out=rpm_out)
    forward_conversion_state = response.compute_forward(state=initial_state,
                                                        load_torque=load_torque,
                                                        downstream_inertia=inertia,
                                                        delta_t=delta_t,
                                                        control_signal=control_signal,
                                                        efficiency=em_consumption,
                                                        limits=em_limits)
    assert forward_conversion_state.output.torque == (rel_max_torque_out(initial_state) - rel_min_torque_out(initial_state)) * control_signal
    w_dot = (forward_conversion_state.output.torque - load_torque) / inertia
    delta_rpm = ang_vel_to_rpm(ang_vel=w_dot*delta_t)
    assert forward_conversion_state.output.rpm == rpm_out + delta_rpm
    assert forward_conversion_state.input.power == forward_conversion_state.output.power / em_consumption.in_to_out_efficiency_value(state=initial_state)
    reverse_conversion_state = response.compute_reverse(state=initial_state,
                                                        efficiency=em_consumption,
                                                        limits=em_limits)
    assert reverse_conversion_state.input.electric_power == initial_state.output.power / em_consumption.out_to_in_efficiency_value(state=initial_state)

def test_create_electric_generator_response() -> None:
    response = ElectricGeneratorDynamicResponse(forward_response=MechanicalToElectric.forward_generator())
    assert isinstance(response, ElectricGeneratorDynamicResponse)
    eg_consumption = ElectricGeneratorConsumption(in_to_out_efficiency_func=lambda s: efficiency)
    eg_limits = return_electric_generator_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                 abs_max_torque_in=abs_max_torque_out, abs_min_torque_in=abs_min_torque_out,
                                                 abs_max_rpm_in=abs_max_rpm_out, abs_min_rpm_in=abs_min_rpm_out,
                                                 abs_max_power_out=abs_max_power_out, abs_min_power_out=abs_min_power_out,
                                                 rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                 rel_max_torque_in=rel_max_torque_in, rel_min_torque_in=rel_min_torque_in,
                                                 rel_max_rpm_in=rel_max_rpm_in, rel_min_rpm_in=rel_min_rpm_in,
                                                 rel_max_power_out=rel_max_power_out, rel_min_power_out=rel_min_power_out)
    initial_state = return_electric_generator_state(nominal_voltage=nominal_voltage,
                                                    torque_in=torque_in,
                                                    rpm_in=rpm_in,
                                                    power_out=power_out)
    forward_conversion_state = response.compute_forward(state=initial_state,
                                                        efficiency=eg_consumption,
                                                        limits=eg_limits)
    result = torque_to_power(torque=torque_in,
                             rpm=rpm_in) / efficiency
    assert forward_conversion_state.output.power == result

def test_create_liquid_combustion_response() -> None:
    for fuel in LIQUID_FUELS:
        response = LiquidCombustionDynamicResponse(forward_response=FuelToMechanical.liquid_combustion_to_mechanical())
        assert isinstance(response, LiquidCombustionDynamicResponse)
        lc_consumption = CombustionEngineConsumption(in_to_out_fuel_consumption_func=lambda s: fuel_liters_in)
        lc_limits = return_liquid_combustion_engine_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                           abs_max_fuel_liters_in=abs_max_fuel_liters_in, abs_min_fuel_liters_in=abs_min_fuel_liters_in,
                                                           abs_max_torque_out=abs_max_torque_out, abs_min_torque_out=abs_min_torque_out,
                                                           abs_max_rpm_out=abs_max_rpm_out, abs_min_rpm_out=abs_min_rpm_out,
                                                           rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                           rel_max_fuel_liters_in=rel_max_fuel_liters_in, rel_min_fuel_liters_in=rel_min_fuel_liters_in,
                                                           rel_max_torque_out=rel_max_torque_out, rel_min_torque_out=rel_min_torque_out,
                                                           rel_max_rpm_out=rel_max_rpm_out, rel_min_rpm_out=rel_min_rpm_out)
        initial_state = return_liquid_combustion_engine_state(fuel=fuel,
                                                              fuel_liters_in=fuel_liters_in,
                                                              torque_out=torque_out,
                                                              rpm_out=rpm_out)
        forward_conversion_state = response.compute_forward(state=initial_state,
                                                            load_torque=load_torque,
                                                            downstream_inertia=inertia,
                                                            delta_t=delta_t,
                                                            control_signal=control_signal,
                                                            fuel_consumption=lc_consumption,
                                                            limits=lc_limits)
        result = fuel_liters_in * delta_t
        assert forward_conversion_state.input.fuel_liters == result

def test_create_gaseous_combustion_response() -> None:
    response = GaseousCombustionDynamicResponse(forward_response=FuelToMechanical.gaseous_combustion_to_mechanical())
    assert isinstance(response, GaseousCombustionDynamicResponse)

def test_create_mechanical_to_mechanical_response() -> None:
    response = PureMechanicalDynamicResponse(forward_response=MechanicalToMechanical.forward_gearbox(gear_ratio=gear_ratio,
                                                                                                     efficiency=efficiency),
                                             reverse_response=MechanicalToMechanical.reverse_gearbox(gear_ratio=gear_ratio,
                                                                                                     efficiency=efficiency))
    assert isinstance(response, PureMechanicalDynamicResponse)

def test_create_rectifier_response() -> None:
    response = RectifierDynamicResponse(forward_response=ElectricToElectric.rectifier_response(voltage_gain=voltage_gain,
                                                                                               efficiency=efficiency))
    assert isinstance(response, RectifierDynamicResponse)

def test_create_inverter_response() -> None:
    response = InverterDynamicResponse(forward_response=ElectricToElectric.inverter_response(voltage_gain=voltage_gain,
                                                                                             efficiency=efficiency))
    assert isinstance(response, InverterDynamicResponse)
