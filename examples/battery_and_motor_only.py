"""
This module contains a minimalist vehicle
representation consisting solely of a battery
and an electric motor running free.
"""

from components.vehicle import Vehicle
from components.battery import LiPoBattery
from components.consumption import return_electric_motor_consumption, \
    return_rechargeable_battery_consumption
from components.dynamic_response import ElectricMotorDynamicResponse
from components.dynamic_response_curves import ElectricToMechanical, \
    MechanicalToElectric
from components.limitation import return_electric_motor_limits
from components.link import create_link, PortType
from components.motor import ElectricMotor
from components.motor_curves import \
    MechanicalPowerEfficiencyCurves, MechanicalMaxTorqueVsRPMCurves
from helpers.functions import power_to_torque
from helpers.types import ElectricSignalType
from simulation.constants import BATTERY_EFFICIENCY_DEFAULT

bat_nominal_energy: float = 5_000_000.0
bat_max_power: float = 250_000.0
bat_initial_soc: float = 1.0
bat_nominal_voltage: float = 200.0
bat_soh: float = 1.0
bat_efficiency: float = BATTERY_EFFICIENCY_DEFAULT

em_mass: float = 150.0
em_nominal_voltage: float = bat_nominal_voltage
em_inertia: float = 20.0
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
link = create_link(component1=battery,
                   component1_port=PortType.OUTPUT_PORT,
                   component2=electric_motor,
                   component2_port=PortType.INPUT_PORT)
assert link is not None

minimalistic_em_vehicle = Vehicle(energy_sources=[battery],
                                  converters=[electric_motor],
                                  links=[link])
