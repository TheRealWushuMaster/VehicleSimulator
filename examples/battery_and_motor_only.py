"""
This module contains a minimalist vehicle
representation consisting solely of a battery
and an electric motor running free.
"""

from components.vehicle import Vehicle
from components.battery import LiPoBattery
from components.consumption import return_electric_motor_consumption, \
    return_rechargeable_battery_consumption
from components.drive_train import return_axle, return_differential, \
    return_drive_train, return_gearbox, return_wheel, WheelDrive
from components.dynamic_response import ElectricMotorDynamicResponse
from components.dynamic_response_curves import ElectricToMechanical, \
    MechanicalToElectric
from components.limitation import return_electric_motor_limits, \
    return_mechanical_to_mechanical_limits
from components.link import create_link, create_drivetrain_link, PortType
from components.motor import ElectricMotor
from components.motor_curves import \
    MechanicalPowerEfficiencyCurves, MechanicalMaxTorqueVsRPMCurves
from helpers.functions import power_to_torque
from helpers.types import ElectricSignalType
from simulation.constants import BATTERY_EFFICIENCY_DEFAULT

# Battery configuration
bat_nominal_energy: float = 5_000_000.0
bat_max_power: float = 250_000.0
bat_initial_soc: float = 1.0
bat_nominal_voltage: float = 200.0
bat_soh: float = 1.0
bat_efficiency: float = BATTERY_EFFICIENCY_DEFAULT

# Electric motor configuration
em_mass: float = 150.0
em_nominal_voltage: float = bat_nominal_voltage
em_inertia: float = 2.0
em_efficiency: float = 0.91
em_max_power: float = bat_max_power * bat_efficiency * em_efficiency
em_min_rpm: float = 0.0
em_max_rpm: float = 6_000.0
em_base_rpm: float = 1_000.0
em_abs_max_temp: float = 350.0
em_abs_min_temp: float = 200.0
em_abs_max_power_in: float = em_max_power / em_efficiency
em_abs_min_power_in: float = 0.0
em_abs_max_torque_out: float = power_to_torque(power=em_max_power,
                                               rpm=em_base_rpm)
em_max_torque_vs_rpm = MechanicalMaxTorqueVsRPMCurves.em(base_rpm=em_base_rpm,
                                                         max_rpm=em_max_rpm,
                                                         max_torque=em_abs_max_torque_out)
em_abs_min_torque_out: float = 0.0

# Drivetrain configuration
wheel_radius: float = 0.3
wheel_width: float = 0.15
wheel_mass: float = 5.0
wheel_pressure: float = 2.0
axle_inertia: float = 0.5
axle_mass: float = 10.0
axle_num_wheels: int = 2
diff_mass: float = 5.0
diff_max_temp: float = 400.0
diff_min_temp: float = 200.0
diff_max_torque_in: float = 1_000.0
diff_min_torque_in: float = 0.0
diff_max_rpm_in: float = 50_000.0
diff_min_rpm_in: float = 0.0
diff_max_torque_out: float = 1_000.0
diff_min_torque_out: float = 0.0
diff_max_rpm_out: float = 50_000.0
diff_min_rpm_out: float = 0.0
diff_gear_ratio: float = 2.4
diff_efficiency: float = 0.96
diff_inertia: float = 0.8
gearbox_mass: float = 5.0
gearbox_gear_ratio: float = 3.3
gearbox_efficiency: float = 0.96
gearbox_inertia: float = 0.8
wheel_drive = WheelDrive.FRONT_DRIVE

em_limits = return_electric_motor_limits(
    abs_max_temp=em_abs_max_temp, abs_min_temp=em_abs_min_temp,
    abs_max_power_in=em_abs_max_power_in, abs_min_power_in=em_abs_min_power_in,
    abs_max_torque_out=em_abs_max_torque_out, abs_min_torque_out=em_abs_min_torque_out,
    abs_max_rpm_out=em_max_rpm, abs_min_rpm_out=em_min_rpm,
    rel_max_temp=lambda s: em_abs_max_temp, rel_min_temp=lambda s: em_abs_min_temp,
    rel_max_power_in=lambda s: em_abs_max_power_in, rel_min_power_in=lambda s: em_abs_min_power_in,
    rel_max_torque_out=em_max_torque_vs_rpm, rel_min_torque_out=lambda s: em_abs_min_torque_out,
    rel_max_rpm_out=lambda s: em_max_rpm, rel_min_rpm_out=lambda s: em_min_rpm
)
em_consumption = return_electric_motor_consumption(
    motor_efficiency_func=MechanicalPowerEfficiencyCurves.constant(efficiency=em_efficiency,
                                                                   max_rpm=em_max_rpm,
                                                                   min_rpm=em_min_rpm,
                                                                   max_torque_vs_rpm=em_max_torque_vs_rpm),  # type: ignore
    generator_efficiency_func=lambda s: em_efficiency
)
em_dyn_resp = ElectricMotorDynamicResponse(
    forward_response=ElectricToMechanical.forward_driven_first_order(),
    reverse_response=MechanicalToElectric.reversed_motor()
)
bat_consumption = return_rechargeable_battery_consumption(
    discharge_efficiency_func=lambda s: bat_efficiency,
    recharge_efficiency_func=lambda s: bat_efficiency
)
battery = LiPoBattery(name="Test LiPo battery",
                      nominal_energy=bat_nominal_energy,
                      max_power=bat_max_power,
                      energy=bat_nominal_energy*bat_initial_soc,
                      nominal_voltage=bat_nominal_voltage,
                      soh=bat_soh,
                      efficiency=bat_consumption)
electric_motor = ElectricMotor(name="Test electric motor",
                               mass=em_mass,
                               nominal_voltage=em_nominal_voltage,
                               limits=em_limits,
                               consumption=em_consumption,
                               dynamic_response=em_dyn_resp,
                               electric_type=ElectricSignalType.DC,
                               inertia=em_inertia)
bat_motor_link = create_link(component1=battery,
                             component1_port=PortType.OUTPUT_PORT,
                             component2=electric_motor,
                             component2_port=PortType.INPUT_PORT)
drivetrain_link = create_drivetrain_link(component=electric_motor)

assert bat_motor_link is not None
assert drivetrain_link is not None

diff_limits = return_mechanical_to_mechanical_limits(
    abs_max_temp=diff_max_temp, abs_min_temp=diff_min_temp,
    abs_max_torque_in=diff_max_torque_in, abs_min_torque_in=diff_min_torque_in,
    abs_max_rpm_in=diff_max_rpm_in, abs_min_rpm_in=diff_min_rpm_in,
    abs_max_torque_out=diff_max_torque_out, abs_min_torque_out=diff_min_torque_out,
    abs_max_rpm_out=diff_max_rpm_out, abs_min_rpm_out=diff_min_rpm_out,
    rel_max_temp=lambda s: diff_max_temp, rel_min_temp=lambda s: diff_min_temp,
    rel_max_torque_in=lambda s: diff_max_torque_in, rel_min_torque_in=lambda s: diff_min_torque_in,
    rel_max_rpm_in=lambda s: diff_max_rpm_in, rel_min_rpm_in=lambda s: diff_min_rpm_in,
    rel_max_torque_out=lambda s: diff_max_torque_out, rel_min_torque_out=lambda s: diff_min_torque_out,
    rel_max_rpm_out=lambda s: diff_max_rpm_out, rel_min_rpm_out=lambda s: diff_min_rpm_out
)
gearbox_limits = diff_limits
wheel = return_wheel(radius=wheel_radius,
                     width=wheel_width,
                     mass=wheel_mass,
                     pressure=wheel_pressure)
axle = return_axle(inertia=axle_inertia,
                   mass=axle_mass,
                   num_wheels=axle_num_wheels,
                   wheel=wheel)
differential = return_differential(mass=diff_mass,
                                   limits=diff_limits,
                                   gear_ratio=diff_gear_ratio,
                                   efficiency=diff_efficiency,
                                   inertia=diff_inertia)
gearbox = return_gearbox(mass=gearbox_mass,
                         limits=gearbox_limits,
                         gear_ratio=gearbox_gear_ratio,
                         efficiency=gearbox_efficiency,
                         inertia=gearbox_inertia)
drive_train = return_drive_train(front_axle=axle,
                                 rear_axle=axle,
                                 wheel_drive=wheel_drive,
                                 differential=differential,
                                 gearbox=gearbox)

minimalistic_em_vehicle = Vehicle(energy_sources=[battery],
                                  converters=[electric_motor],
                                  drive_train=drive_train,
                                  links=[bat_motor_link, drivetrain_link])
