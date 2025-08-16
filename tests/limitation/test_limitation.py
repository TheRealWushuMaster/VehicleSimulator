"""This module contains test routines for the limitation classes."""

from components.limitation import return_electric_generator_limits, return_electric_motor_limits, \
    return_electric_to_electric_limits, return_gaseous_combustion_engine_limits, \
    return_liquid_combustion_engine_limits, return_mechanical_to_mechanical_limits, \
    return_non_rechargeable_battery_limits, return_rechargeable_battery_limits, \
    return_fuel_cell_limits, \
    return_liquid_fuel_tank_limits, return_gaseous_fuel_tank_limits, \
    RechargeableBatteryLimits, NonRechargeableBatteryLimits, \
    ElectricMotorLimits, ElectricGeneratorLimits, \
    LiquidCombustionEngineLimits, GaseousCombustionEngineLimits, \
    MechanicalToMechanicalLimits, ElectricToElectricLimits, \
    FuelCellLimits, \
    LiquidFuelTankLimits, GaseousFuelTankLimits

abs_max_temp: float = 300.0
abs_min_temp: float = 200.0
abs_max_power_in: float = 400.0
abs_min_power_in: float = 0.0
abs_max_power_out: float = 400.0
abs_min_power_out: float = 0.0
abs_max_torque_in: float = 40.0
abs_min_torque_in: float = 0.0
abs_max_rpm_in: float = 6_000.0
abs_min_rpm_in: float = 0.0
abs_max_torque_out: float = 40.0
abs_min_torque_out: float = 0.0
abs_max_rpm_out: float = 6_000.0
abs_min_rpm_out: float = 0.0
abs_max_fuel_liters_in: float = 6.0
abs_min_fuel_liters_in: float = 0.0
abs_max_fuel_mass_in: float = 4.0
abs_min_fuel_mass_in: float = 0.0
electric_energy_capacity: float = 1_000.0
fuel_liters_capacity: float = 50.0
abs_max_fuel_liters_transfer: float = 1.0
abs_min_fuel_liters_transfer: float = 0.0
fuel_mass_capacity: float = 40.0
abs_max_fuel_mass_transfer: float = 1.0
abs_min_fuel_mass_transfer: float = 0.0
def rel_max_temp(s) -> float:
    return abs_max_temp
def rel_min_temp(s) -> float:
    return abs_min_temp
def rel_max_power_in(s) -> float:
    return abs_max_power_in
def rel_min_power_in(s) -> float:
    return abs_min_power_in
def rel_max_power_out(s) -> float:
    return abs_max_power_out
def rel_min_power_out(s) -> float:
    return abs_min_power_out
def rel_max_torque_in(s) -> float:
    return abs_max_torque_in
def rel_min_torque_in(s) -> float:
    return abs_min_torque_in
def rel_max_rpm_in(s) -> float:
    return abs_max_rpm_in
def rel_min_rpm_in(s) -> float:
    return abs_min_rpm_in
def rel_max_torque_out(s) -> float:
    return abs_max_torque_out
def rel_min_torque_out(s) -> float:
    return abs_min_torque_out
def rel_max_rpm_out(s) -> float:
    return abs_max_rpm_out
def rel_min_rpm_out(s) -> float:
    return abs_min_rpm_out
def rel_max_fuel_liters_in(s) -> float:
    return abs_max_fuel_liters_in
def rel_min_fuel_liters_in(s) -> float:
    return abs_min_fuel_liters_in
def rel_max_fuel_mass_in(s) -> float:
    return abs_max_fuel_mass_in
def rel_min_fuel_mass_in(s) -> float:
    return abs_min_fuel_mass_in

def test_create_rechargeable_battery_limitation() -> None:
    limitation = return_rechargeable_battery_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                    abs_max_power_in=abs_max_power_in, abs_min_power_in=abs_min_power_in,
                                                    abs_max_power_out=abs_max_power_out, abs_min_power_out=abs_min_power_out,
                                                    rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                    rel_max_power_in=rel_max_power_in, rel_min_power_in=rel_min_power_in,
                                                    rel_max_power_out=rel_max_power_out, rel_min_power_out=rel_min_power_out,
                                                    electric_energy_capacity=electric_energy_capacity)
    assert isinstance(limitation, RechargeableBatteryLimits)

def test_create_non_rechargeable_battery_limitation() -> None:
    limitation = return_non_rechargeable_battery_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                        abs_max_power_out=abs_max_power_out, abs_min_power_out=abs_min_power_out,
                                                        rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                        rel_max_power_out=rel_max_power_out, rel_min_power_out=rel_min_power_out,
                                                        electric_energy_capacity=electric_energy_capacity)
    assert isinstance(limitation, NonRechargeableBatteryLimits)

def test_create_electric_motor_limitation() -> None:
    limitation = return_electric_motor_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                              abs_max_power_in=abs_max_power_in, abs_min_power_in=abs_min_power_in,
                                              abs_max_torque_out=abs_max_torque_out, abs_min_torque_out=abs_min_torque_out,
                                              abs_max_rpm_out=abs_max_rpm_out, abs_min_rpm_out=abs_min_rpm_out,
                                              rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                              rel_max_power_in=rel_max_power_in, rel_min_power_in=rel_min_power_in,
                                              rel_max_torque_out=rel_max_torque_out, rel_min_torque_out=rel_min_torque_out,
                                              rel_max_rpm_out=rel_max_rpm_out, rel_min_rpm_out=rel_min_rpm_out)
    assert isinstance(limitation, ElectricMotorLimits)

def test_create_electric_generator_limitation() -> None:
    limitation = return_electric_generator_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                  abs_max_torque_in=abs_max_torque_in, abs_min_torque_in=abs_min_torque_in,
                                                  abs_max_rpm_in=abs_max_rpm_in, abs_min_rpm_in=abs_min_rpm_in,
                                                  abs_max_power_out=abs_max_power_out, abs_min_power_out=abs_min_power_out,
                                                  rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                  rel_max_torque_in=rel_max_torque_in, rel_min_torque_in=rel_min_torque_in,
                                                  rel_max_rpm_in=rel_max_rpm_in, rel_min_rpm_in=rel_min_rpm_in,
                                                  rel_max_power_out=rel_max_power_out, rel_min_power_out=rel_min_power_out,)
    assert isinstance(limitation, ElectricGeneratorLimits)

def test_create_liquid_combustion_engine_limitation() -> None:
    limitation = return_liquid_combustion_engine_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                        abs_max_fuel_liters_in=abs_max_fuel_liters_in, abs_min_fuel_liters_in=abs_min_fuel_liters_in,
                                                        abs_max_torque_out=abs_max_torque_out, abs_min_torque_out=abs_min_torque_out,
                                                        abs_max_rpm_out=abs_max_rpm_out, abs_min_rpm_out=abs_min_rpm_out,
                                                        rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                        rel_max_fuel_liters_in=rel_max_fuel_liters_in, rel_min_fuel_liters_in=rel_min_fuel_liters_in,
                                                        rel_max_torque_out=rel_max_torque_out, rel_min_torque_out=rel_min_torque_out,
                                                        rel_max_rpm_out=rel_max_rpm_out, rel_min_rpm_out=rel_min_rpm_out)
    assert isinstance(limitation, LiquidCombustionEngineLimits)

def test_create_gaseous_combustion_engine_limitation() -> None:
    limitation = return_gaseous_combustion_engine_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                         abs_max_fuel_mass_in=abs_max_fuel_mass_in, abs_min_fuel_mass_in=abs_min_fuel_mass_in,
                                                         abs_max_torque_out=abs_max_torque_out, abs_min_torque_out=abs_min_torque_out,
                                                         abs_max_rpm_out=abs_max_rpm_out, abs_min_rpm_out=abs_min_rpm_out,
                                                         rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                         rel_max_fuel_mass_in=rel_max_fuel_mass_in, rel_min_fuel_mass_in=rel_min_fuel_mass_in,
                                                         rel_max_torque_out=rel_max_torque_out, rel_min_torque_out=rel_min_torque_out,
                                                         rel_max_rpm_out=rel_max_rpm_out, rel_min_rpm_out=rel_min_rpm_out)
    assert isinstance(limitation, GaseousCombustionEngineLimits)

def test_create_fuel_cell_limitation() -> None:
    limitation = return_fuel_cell_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                         abs_max_fuel_mass_in=abs_max_fuel_mass_in, abs_min_fuel_mass_in=abs_min_fuel_mass_in,
                                         abs_max_power_out=abs_max_power_out, abs_min_power_out=abs_min_power_out,
                                         rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                         rel_max_fuel_mass_in=rel_max_fuel_mass_in, rel_min_fuel_mass_in=rel_min_fuel_mass_in,
                                         rel_max_power_out=rel_max_power_out, rel_min_power_out=rel_min_power_out)
    assert isinstance(limitation, FuelCellLimits)

def test_create_electric_to_electric_limitation() -> None:
    limitation = return_electric_to_electric_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                    abs_max_power_in=abs_max_power_in, abs_min_power_in=abs_min_power_in,
                                                    abs_max_power_out=abs_max_power_out, abs_min_power_out=abs_min_power_out,
                                                    rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                    rel_max_power_in=rel_max_power_in, rel_min_power_in=rel_min_power_in,
                                                    rel_max_power_out=rel_max_power_out, rel_min_power_out=rel_min_power_out,)
    assert isinstance(limitation, ElectricToElectricLimits)

def test_create_mechanical_to_mechanical_limitation() -> None:
    limitation = return_mechanical_to_mechanical_limits(abs_max_temp=abs_max_temp, abs_min_temp=abs_min_temp,
                                                        abs_max_torque_in=abs_max_torque_in, abs_min_torque_in=abs_min_torque_in,
                                                        abs_max_rpm_in=abs_max_rpm_in, abs_min_rpm_in=abs_min_rpm_in,
                                                        abs_max_torque_out=abs_max_torque_out, abs_min_torque_out=abs_min_torque_out,
                                                        abs_max_rpm_out=abs_max_rpm_out, abs_min_rpm_out=abs_min_rpm_out,
                                                        rel_max_temp=rel_max_temp, rel_min_temp=rel_min_temp,
                                                        rel_max_torque_in=rel_max_torque_in, rel_min_torque_in=rel_min_torque_in,
                                                        rel_max_rpm_in=rel_max_rpm_in, rel_min_rpm_in=rel_min_rpm_in,
                                                        rel_max_torque_out=rel_max_torque_out, rel_min_torque_out=rel_min_torque_out,
                                                        rel_max_rpm_out=rel_max_rpm_out, rel_min_rpm_out=rel_min_rpm_out)
    assert isinstance(limitation, MechanicalToMechanicalLimits)

def test_create_liquid_fuel_tank_limitation() -> None:
    limitation = return_liquid_fuel_tank_limits(abs_max_temperature=abs_max_temp, abs_min_temperature=abs_min_temp,
                                                abs_max_fuel_liters_transfer=abs_max_fuel_liters_transfer,
                                                abs_min_fuel_liters_transfer=abs_min_fuel_liters_transfer,
                                                fuel_liters_capacity=fuel_liters_capacity)
    assert isinstance(limitation, LiquidFuelTankLimits)

def test_create_gaseous_fuel_tank_limitation() -> None:
    limitation = return_gaseous_fuel_tank_limits(abs_max_temperature=abs_max_temp, abs_min_temperature=abs_min_temp,
                                                 abs_max_fuel_mass_transfer=abs_max_fuel_mass_transfer,
                                                 abs_min_fuel_mass_transfer=abs_min_fuel_mass_transfer,
                                                 fuel_mass_capacity=fuel_mass_capacity)
    assert isinstance(limitation, GaseousFuelTankLimits)
