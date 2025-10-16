"""This module contains test routines for the dynamic response classes."""

from components.component_snapshot import return_electric_motor_snapshot, \
    return_electric_generator_snapshot, return_liquid_ice_snapshot, return_gaseous_ice_snapshot, \
    return_fuel_cell_snapshot, return_gearbox_snapshot, \
    return_electric_inverter_snapshot, return_electric_rectifier_snapshot, \
    return_drivetrain_snapshot
from components.consumption import ElectricMotorConsumption, \
    ElectricGeneratorConsumption, \
    LiquidCombustionEngineConsumption, GaseousCombustionEngineConsumption, \
    FuelCellConsumption, GearBoxConsumption, \
    ElectricInverterConsumption, ElectricRectifierConsumption
from components.drive_train import DriveTrain, Axle, Differential, \
    GearBox, Wheel, WheelDrive
from components.dynamic_response import ElectricMotorDynamicResponse, \
    ElectricGeneratorDynamicResponse, LiquidCombustionDynamicResponse, \
    GaseousCombustionDynamicResponse, PureMechanicalDynamicResponse, \
    RectifierDynamicResponse, InverterDynamicResponse, FuelCellDynamicResponse
from components.dynamic_response_curves import MechanicalToMechanical, \
    ElectricToElectric, ElectricToMechanical, MechanicalToElectric, \
    FuelToMechanical, FuelToElectric
from components.fuel_type import LIQUID_FUELS, GASEOUS_FUELS
from components.limitation import return_electric_motor_limits, \
    return_electric_generator_limits, return_liquid_combustion_engine_limits, \
    return_gaseous_combustion_engine_limits, return_mechanical_to_mechanical_limits, \
    return_electric_to_electric_limits, return_fuel_cell_limits
from helpers.functions import ang_vel_to_rpm, torque_to_power

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
efficiency2: float = 0.93
gear_ratio: float = 2.3
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
abs_max_fuel_mass_in: float = 0.36
abs_min_fuel_mass_in: float = 0.0
wheel_radius: float = 0.35
wheel_drive: WheelDrive = WheelDrive.FRONT_DRIVE
wheel_width: float = 0.21
wheel_mass: float = 10.0
wheel_pressure: float = 2.5
axle_mass: float = 5.0
num_wheels: int = 2
diff_mass: float = 5.0
diff_gear_ratio: float = 1.5
diff_inertia: float = 0.3
gearbox_mass: float = 4.8
gearbox_inertia: float = 0.2
def rel_max_temp(s): return abs_max_temp
def rel_min_temp(s): return abs_min_temp
def rel_max_power_in(s): return abs_max_power_in
def rel_min_power_in(s): return abs_min_power_in
def rel_max_power_out(s): return abs_max_power_out
def rel_min_power_out(s): return abs_min_power_out
def rel_max_torque_in(s): return abs_max_torque_in
def rel_max_torque_out(s): return abs_max_torque_out
def rel_min_torque_in(s): return abs_min_torque_in
def rel_min_torque_out(s): return abs_min_torque_out
def rel_max_rpm_in(s): return abs_max_rpm_in
def rel_min_rpm_in(s): return abs_min_rpm_in
def rel_max_rpm_out(s): return abs_max_rpm_out
def rel_min_rpm_out(s): return abs_min_rpm_out
def rel_max_fuel_liters_in(s): return abs_max_fuel_liters_in
def rel_min_fuel_liters_in(s): return abs_min_fuel_liters_in
def rel_max_fuel_mass_in(s): return abs_max_fuel_mass_in
def rel_min_fuel_mass_in(s): return abs_min_fuel_mass_in

def create_electric_motor_response() -> ElectricMotorDynamicResponse:
    response = ElectricMotorDynamicResponse(forward_response=ElectricToMechanical.forward_driven_first_order(),
                                            reverse_response=MechanicalToElectric.reversed_motor())
    assert isinstance(response, ElectricMotorDynamicResponse)
    return response

def create_electric_generator_response() -> ElectricGeneratorDynamicResponse:
    response = ElectricGeneratorDynamicResponse(forward_response=MechanicalToElectric.forward_generator())
    assert isinstance(response, ElectricGeneratorDynamicResponse)
    return response

def create_liquid_combustion_response() -> LiquidCombustionDynamicResponse:
    response = LiquidCombustionDynamicResponse(forward_response=FuelToMechanical.liquid_combustion_to_mechanical())
    assert isinstance(response, LiquidCombustionDynamicResponse)
    return response

def create_gaseous_combustion_response() -> GaseousCombustionDynamicResponse:
    response = GaseousCombustionDynamicResponse(forward_response=FuelToMechanical.gaseous_combustion_to_mechanical())
    assert isinstance(response, GaseousCombustionDynamicResponse)
    return response

def create_fuel_cell_response() -> FuelCellDynamicResponse:
    response = FuelCellDynamicResponse(forward_response=FuelToElectric.gaseous_fuel_to_electric())
    assert isinstance(response, FuelCellDynamicResponse)
    return response

def create_pure_mechanical_response() -> PureMechanicalDynamicResponse:
    response = PureMechanicalDynamicResponse(forward_response=MechanicalToMechanical.forward_gearbox(gear_ratio=gear_ratio,
                                                                                                     efficiency=efficiency),
                                             reverse_response=MechanicalToMechanical.reverse_gearbox(gear_ratio=gear_ratio,
                                                                                                     efficiency=efficiency2))
    assert isinstance(response, PureMechanicalDynamicResponse)
    return response

def create_rectifier_response() -> RectifierDynamicResponse:
    response = RectifierDynamicResponse(forward_response=ElectricToElectric.rectifier_response(efficiency=efficiency))
    assert isinstance(response, RectifierDynamicResponse)
    return response

def create_inverter_response() -> InverterDynamicResponse:
    response = InverterDynamicResponse(forward_response=ElectricToElectric.inverter_response(efficiency=efficiency))
    assert isinstance(response, InverterDynamicResponse)
    return response

def create_drivetrain() -> DriveTrain:
    mm_limits = return_mechanical_to_mechanical_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                       abs_max_torque_in=abs_max_torque_in, abs_min_torque_in=abs_min_torque_in,
                                                       abs_max_rpm_in=abs_max_rpm_in, abs_min_rpm_in=abs_min_rpm_in,
                                                       abs_max_torque_out=abs_max_torque_out, abs_min_torque_out=abs_min_torque_out,
                                                       abs_max_rpm_out=abs_max_rpm_out, abs_min_rpm_out=abs_min_rpm_out,
                                                       rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                       rel_max_torque_in=rel_max_torque_in, rel_min_torque_in=rel_min_torque_in,
                                                       rel_max_rpm_in=rel_max_rpm_in, rel_min_rpm_in=rel_min_rpm_in,
                                                       rel_max_torque_out=rel_max_torque_out, rel_min_torque_out=rel_min_torque_out,
                                                       rel_max_rpm_out=rel_max_rpm_out, rel_min_rpm_out=rel_min_rpm_out)
    wheel = Wheel(radius=wheel_radius,
                  width=wheel_width,
                  mass=wheel_mass,
                  air_pressure=wheel_pressure)
    axle = Axle(_inertia=inertia,
                _mass=axle_mass,
                _num_wheels=num_wheels,
                wheel=wheel)
    differential = Differential(name="Differential",
                                mass=diff_mass,
                                limits=mm_limits,
                                gear_ratio=diff_gear_ratio,
                                efficiency=efficiency,
                                inertia=diff_inertia)
    gearbox = GearBox(name="Gearbox",
                      mass=gearbox_mass,
                      limits=mm_limits,
                      gear_ratio=gear_ratio,
                      efficiency=efficiency2,
                      inertia=gearbox_inertia)
    return DriveTrain(front_axle=axle,
                      rear_axle=axle,
                      wheel_drive=wheel_drive,
                      differential=differential,
                      gearbox=gearbox)

# =============================

def test_create_electric_motor_response() -> None:
    response = create_electric_motor_response()
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
    initial_snap = return_electric_motor_snapshot(electric_power_in=power_in,
                                                  torque_out=torque_out,
                                                  rpm_out=rpm_out)
    # Testing forward conversion
    fc_snap, fc_new_state = response.compute_forward(snap=initial_snap,
                                                     load_torque=load_torque,
                                                     downstream_inertia=inertia,
                                                     delta_t=delta_t,
                                                     control_signal=control_signal,
                                                     efficiency=em_consumption,
                                                     limits=em_limits)
    assert fc_snap.io.output_port.torque == (rel_max_torque_out(initial_snap) - rel_min_torque_out(initial_snap)) * control_signal
    w_dot = (fc_snap.io.output_port.torque - load_torque) / inertia
    delta_rpm = ang_vel_to_rpm(ang_vel=w_dot*delta_t)
    assert fc_new_state.output_port.rpm == rpm_out + delta_rpm
    assert fc_snap.power_in * em_consumption.in_to_out_efficiency_value(snap=initial_snap) == fc_snap.power_out
    # Testing reverse conversion
    rc_snap, rc_new_state = response.compute_reverse(snap=initial_snap,
                                                     efficiency=em_consumption,
                                                     limits=em_limits)
    assert rc_snap.power_in == rc_snap.power_out * em_consumption.out_to_in_efficiency_value(snap=initial_snap)

def test_create_electric_generator_response() -> ElectricGeneratorDynamicResponse:
    response = create_electric_generator_response()
    eg_consumption = ElectricGeneratorConsumption(in_to_out_efficiency_func=lambda s: efficiency)
    eg_limits = return_electric_generator_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                 abs_max_torque_in=abs_max_torque_out, abs_min_torque_in=abs_min_torque_out,
                                                 abs_max_rpm_in=abs_max_rpm_out, abs_min_rpm_in=abs_min_rpm_out,
                                                 abs_max_power_out=abs_max_power_out, abs_min_power_out=abs_min_power_out,
                                                 rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                 rel_max_torque_in=rel_max_torque_in, rel_min_torque_in=rel_min_torque_in,
                                                 rel_max_rpm_in=rel_max_rpm_in, rel_min_rpm_in=rel_min_rpm_in,
                                                 rel_max_power_out=rel_max_power_out, rel_min_power_out=rel_min_power_out)
    initial_snap = return_electric_generator_snapshot(torque_in=torque_in,
                                                      rpm_in=rpm_in,
                                                      electric_power_out=power_out)
    fc_snap, fc_new_state = response.compute_forward(snap=initial_snap,
                                                     efficiency=eg_consumption,
                                                     limits=eg_limits)
    result = torque_to_power(torque=torque_in,
                             rpm=rpm_in) * efficiency
    assert fc_snap.power_out == result
    return response

def test_create_liquid_combustion_response() -> None:
    for fuel in LIQUID_FUELS:
        response = create_liquid_combustion_response()
        lc_consumption = LiquidCombustionEngineConsumption(in_to_out_fuel_consumption_func=lambda s: fuel_liters_in)
        lc_limits = return_liquid_combustion_engine_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                           abs_max_fuel_liters_in=abs_max_fuel_liters_in, abs_min_fuel_liters_in=abs_min_fuel_liters_in,
                                                           abs_max_torque_out=abs_max_torque_out, abs_min_torque_out=abs_min_torque_out,
                                                           abs_max_rpm_out=abs_max_rpm_out, abs_min_rpm_out=abs_min_rpm_out,
                                                           rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                           rel_max_fuel_liters_in=rel_max_fuel_liters_in, rel_min_fuel_liters_in=rel_min_fuel_liters_in,
                                                           rel_max_torque_out=rel_max_torque_out, rel_min_torque_out=rel_min_torque_out,
                                                           rel_max_rpm_out=rel_max_rpm_out, rel_min_rpm_out=rel_min_rpm_out)
        initial_snap = return_liquid_ice_snapshot(fuel_in=fuel,
                                                  liters_flow_in=fuel_liters_in,
                                                  torque_out=torque_out,
                                                  rpm_out=rpm_out)
        fc_snap, fc_new_state = response.compute_forward(snap=initial_snap,
                                                         load_torque=load_torque,
                                                         downstream_inertia=inertia,
                                                         delta_t=delta_t,
                                                         control_signal=control_signal,
                                                         fuel_consumption=lc_consumption,
                                                         limits=lc_limits)
        result = fuel_liters_in * delta_t
        assert fc_snap.io.input_port.liters_flow == result

def test_create_gaseous_combustion_response() -> None:
    for fuel in GASEOUS_FUELS:
        response = create_gaseous_combustion_response()
        gc_consumption = GaseousCombustionEngineConsumption(in_to_out_fuel_consumption_func=lambda s: fuel_mass_in)
        gc_limits = return_gaseous_combustion_engine_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                            abs_max_fuel_mass_in=abs_max_fuel_mass_in, abs_min_fuel_mass_in=abs_min_fuel_mass_in,
                                                            abs_max_torque_out=abs_max_torque_out, abs_min_torque_out=abs_min_torque_out,
                                                            abs_max_rpm_out=abs_max_rpm_out, abs_min_rpm_out=abs_min_rpm_out,
                                                            rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                            rel_max_fuel_mass_in=rel_max_fuel_mass_in, rel_min_fuel_mass_in=rel_min_fuel_mass_in,
                                                            rel_max_torque_out=rel_max_torque_out, rel_min_torque_out=rel_min_torque_out,
                                                            rel_max_rpm_out=rel_max_rpm_out, rel_min_rpm_out=rel_min_rpm_out)
        initial_snap = return_gaseous_ice_snapshot(fuel_in=fuel,
                                                   mass_flow_in=fuel_mass_in,
                                                   torque_out=torque_out,
                                                   rpm_out=rpm_out)
        fc_snap, fc_new_state = response.compute_forward(snap=initial_snap,
                                                         load_torque=load_torque,
                                                         downstream_inertia=inertia,
                                                         delta_t=delta_t,
                                                         control_signal=control_signal,
                                                         fuel_consumption=gc_consumption,
                                                         limits=gc_limits)
        result = fuel_mass_in * delta_t
        assert fc_snap.io.input_port.mass_flow == result

def test_create_fuel_cell_response() -> None:
    for fuel in GASEOUS_FUELS:
        response = create_fuel_cell_response()
        fc_consumption = FuelCellConsumption(in_to_out_fuel_consumption_func=lambda s: fuel_mass_in)
        fc_limits = return_fuel_cell_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                            abs_max_fuel_mass_in=abs_max_fuel_mass_in, abs_min_fuel_mass_in=abs_min_fuel_mass_in,
                                            abs_max_power_out=abs_max_power_out, abs_min_power_out=abs_min_power_out,
                                            rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                            rel_max_fuel_mass_in=rel_max_fuel_mass_in, rel_min_fuel_mass_in=rel_min_fuel_mass_in,
                                            rel_max_power_out=rel_max_power_out, rel_min_power_out=rel_min_power_out,)
        initial_snap = return_fuel_cell_snapshot(fuel_in=fuel,
                                                 mass_flow_in=fuel_mass_in,
                                                 electric_power_out=power_out)
        fc_snap, fc_new_state = response.compute_forward(snap=initial_snap,
                                                         delta_t=delta_t,
                                                         control_signal=control_signal,
                                                         fuel_consumption=fc_consumption,
                                                         limits=fc_limits)
        result = fuel_mass_in * delta_t
        assert fc_snap.io.input_port.mass_flow == result

def test_create_gearbox_response() -> None:
    response = create_pure_mechanical_response()
    mm_consumption = GearBoxConsumption(in_to_out_efficiency_func=lambda s: efficiency,
                                        out_to_in_efficiency_func=lambda s: efficiency2)
    mm_limits = return_mechanical_to_mechanical_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                       abs_max_torque_in=abs_max_torque_in, abs_min_torque_in=abs_min_torque_in,
                                                       abs_max_rpm_in=abs_max_rpm_in, abs_min_rpm_in=abs_min_rpm_in,
                                                       abs_max_torque_out=abs_max_torque_out, abs_min_torque_out=abs_min_torque_out,
                                                       abs_max_rpm_out=abs_max_rpm_out, abs_min_rpm_out=abs_min_rpm_out,
                                                       rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                       rel_max_torque_in=rel_max_torque_in, rel_min_torque_in=rel_min_torque_in,
                                                       rel_max_rpm_in=rel_max_rpm_in, rel_min_rpm_in=rel_min_rpm_in,
                                                       rel_max_torque_out=rel_max_torque_out, rel_min_torque_out=rel_min_torque_out,
                                                       rel_max_rpm_out=rel_max_rpm_out, rel_min_rpm_out=rel_min_rpm_out)
    initial_snap = return_gearbox_snapshot(torque_in=torque_in,
                                           rpm_in=rpm_in,
                                           torque_out=torque_out,
                                           rpm_out=rpm_in/gear_ratio)
    # Testing forward conversion
    fc_snap, fc_new_state = response.compute_forward(snap=initial_snap)
    assert fc_snap.io.output_port.torque == initial_snap.io.input_port.torque * \
        gear_ratio * mm_consumption.in_to_out_efficiency_value(snap=fc_snap)
    assert fc_snap.state.output_port.rpm == fc_snap.state.input_port.rpm / gear_ratio
    assert round(fc_snap.power_out, 8) == round(fc_snap.power_in * mm_consumption.in_to_out_efficiency_value(snap=fc_snap), 8)
    # Testing reverse conversion
    rc_snap, rc_new_state = response.compute_reverse(snap=initial_snap)
    assert round(rc_snap.state.input_port.rpm, 8) == round(rc_snap.state.output_port.rpm * gear_ratio, 8)
    assert round(rc_snap.io.output_port.torque, 8) == round(rc_snap.io.input_port.torque * \
        gear_ratio / mm_consumption.out_to_in_efficiency_value(snap=rc_snap), 8)
    assert round(rc_snap.power_out, 8) == round(rc_snap.power_in / mm_consumption.out_to_in_efficiency_value(snap=rc_snap), 8)

def test_create_rectifier_response() -> None:
    response = create_rectifier_response()
    er_consumption = ElectricRectifierConsumption(in_to_out_efficiency_func=lambda s: efficiency)
    er_limits = return_electric_to_electric_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                   abs_max_power_in=abs_max_power_in, abs_min_power_in=abs_min_power_in,
                                                   abs_max_power_out=abs_max_power_in, abs_min_power_out=abs_min_power_in,
                                                   rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                   rel_max_power_in=rel_max_power_in, rel_min_power_in=rel_min_power_in,
                                                   rel_max_power_out=rel_max_power_in, rel_min_power_out=rel_min_power_in)
    initial_snap = return_electric_rectifier_snapshot(electric_power_in=power_in,
                                                      electric_power_out=power_out)
    fc_snap, fc_new_state = response.compute_forward(snap=initial_snap)
    assert fc_snap.power_out == fc_snap.power_in * \
        er_consumption.in_to_out_efficiency_value(snap=fc_snap)

def test_create_inverter_response() -> None:
    response = create_inverter_response()
    ir_consumption = ElectricInverterConsumption(in_to_out_efficiency_func=lambda s: efficiency)
    ir_limits = return_electric_to_electric_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                   abs_max_power_in=abs_max_power_in, abs_min_power_in=abs_min_power_in,
                                                   abs_max_power_out=abs_max_power_in, abs_min_power_out=abs_min_power_in,
                                                   rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                   rel_max_power_in=rel_max_power_in, rel_min_power_in=rel_min_power_in,
                                                   rel_max_power_out=rel_max_power_in, rel_min_power_out=rel_min_power_in)
    initial_snap = return_electric_inverter_snapshot(electric_power_in=power_in,
                                                     electric_power_out=power_out)
    fc_snap, fc_new_state = response.compute_forward(snap=initial_snap)
    assert fc_snap.power_out == fc_snap.power_in * \
        ir_consumption.in_to_out_efficiency_value(snap=fc_snap)

def test_create_drivetrain_response() -> None:
    dt = create_drivetrain()
    initial_snap = return_drivetrain_snapshot(torque_in=torque_in,
                                              rpm_in=rpm_in,
                                              torque_out=torque_out,
                                              rpm_out=rpm_in/gear_ratio/diff_gear_ratio)
    # Testing forward conversion
    dt_snap, dt_new_state = dt.process_drive(snap=initial_snap)
    # Testing reverse conversion
    dt_snap, dt_new_state = dt.process_recover(snap=initial_snap)
