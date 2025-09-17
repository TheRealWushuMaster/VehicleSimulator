"""This module contains methods for testing consumption classes."""

from components.consumption import \
    RechargeableBatteryConsumption, NonRechargeableBatteryConsumption, \
    ElectricGeneratorConsumption, ElectricMotorConsumption, \
    LiquidCombustionEngineConsumption, GaseousCombustionEngineConsumption, \
    FuelCellConsumption, \
    ElectricInverterConsumption, ElectricRectifierConsumption, \
    GearBoxConsumption, \
    return_rechargeable_battery_consumption, return_non_rechargeable_battery_consumption, \
    return_electric_generator_consumption, return_electric_motor_consumption, \
    return_liquid_combustion_engine_consumption, return_gaseous_combustion_engine_consumption, \
    return_fuel_cell_consumption, \
    return_electric_inverter_consumption, return_electric_rectifier_consumption, \
    return_gearbox_consumption
from components.fuel_type import LIQUID_FUELS, GASEOUS_FUELS
from components.component_snapshot import \
    return_rechargeable_battery_snapshot, return_non_rechargeable_battery_snapshot, \
    return_electric_motor_snapshot, return_electric_generator_snapshot, \
    return_liquid_ice_snapshot, return_gaseous_ice_snapshot, return_fuel_cell_snapshot, \
    return_electric_inverter_snapshot, return_electric_rectifier_snapshot, \
    return_gearbox_snapshot
from helpers.functions import torque_to_power


delta_t: float = 0.1
eff1: float = 0.95
eff2: float = 0.90
fuel_cons_per_sec: float = 0.5
fuel_liters_in: float = 0.15
fuel_mass_in: float = 0.12
electric_energy_stored: float = 1_000
voltage_in: float = 300.0
voltage_out: float = 250.0
power_in: float = 3_000.0
power_out: float = 2_750.0
torque_in: float = 2.0
rpm_in: float = 100.0
torque_out: float = 4.0
rpm_out: float = 150.0


def create_rechargeable_battery_consumption(discharge_eff: float,
                                            recharge_eff: float
                                            ) -> RechargeableBatteryConsumption:
    consumption = return_rechargeable_battery_consumption(
        discharge_efficiency_func=lambda s: discharge_eff,
        recharge_efficiency_func=lambda s: recharge_eff
    )
    assert isinstance(consumption, RechargeableBatteryConsumption)
    return consumption

def create_non_rechargeable_battery_consumption(discharge_eff: float
                                                ) -> NonRechargeableBatteryConsumption:
    consumption = return_non_rechargeable_battery_consumption(
        discharge_efficiency_func=lambda s: discharge_eff
    )
    assert isinstance(consumption, NonRechargeableBatteryConsumption)
    return consumption

def create_electric_generator_consumption(gen_eff: float
                                          ) -> ElectricGeneratorConsumption:
    consumption = return_electric_generator_consumption(
        generator_efficiency_func=lambda s: gen_eff
    )
    assert isinstance(consumption, ElectricGeneratorConsumption)
    return consumption

def create_electric_motor_consumption(motor_eff: float,
                                      gen_eff: float
                                      ) -> ElectricMotorConsumption:
    consumption = return_electric_motor_consumption(
        motor_efficiency_func=lambda s: motor_eff,
        generator_efficiency_func=lambda s: gen_eff
    )
    assert isinstance(consumption, ElectricMotorConsumption)
    return consumption

def create_liquid_combustion_engine_consumption(fuel_cons: float
                                                ) -> LiquidCombustionEngineConsumption:
    func = lambda s: fuel_cons
    consumption = return_liquid_combustion_engine_consumption(
        fuel_consumption_func=func
    )
    assert isinstance(consumption, LiquidCombustionEngineConsumption)
    return consumption

def create_gaseous_combustion_engine_consumption(fuel_cons: float
                                                 ) -> GaseousCombustionEngineConsumption:
    func = lambda s: fuel_cons
    consumption = return_gaseous_combustion_engine_consumption(
        fuel_consumption_func=func
    )
    assert isinstance(consumption, GaseousCombustionEngineConsumption)
    return consumption

def create_fuel_cell_consumption(fuel_cons: float
                                 ) -> FuelCellConsumption:
    func = lambda s: fuel_cons
    consumption = return_fuel_cell_consumption(
        fuel_consumption_func=func
    )
    assert isinstance(consumption, FuelCellConsumption)
    return consumption

def create_electric_inverter_consumption(eff: float
                                         ) -> ElectricInverterConsumption:
    consumption = return_electric_inverter_consumption(
        efficiency_func=lambda s: eff
    )
    assert isinstance(consumption, ElectricInverterConsumption)
    return consumption

def create_electric_rectifier_consumption(eff: float
                                          ) -> ElectricRectifierConsumption:
    consumption = return_electric_rectifier_consumption(
        efficiency_func=lambda s: eff
    )
    assert isinstance(consumption, ElectricRectifierConsumption)
    return consumption

def create_gearbox_consumption(eff: float,
                               rev_eff: float
                               ) -> GearBoxConsumption:
    consumption = return_gearbox_consumption(
        efficiency_func=lambda s: eff,
        reverse_efficiency_func=lambda s: rev_eff
    )
    assert isinstance(consumption, GearBoxConsumption)
    return consumption

# =========================

def test_rechargeable_battery_consumption() -> None:
    consumption = create_rechargeable_battery_consumption(discharge_eff=eff1,
                                                          recharge_eff=eff2)
    snap = return_rechargeable_battery_snapshot(electric_power_in=power_in,
                                                electric_power_out=power_out,
                                                electric_energy_stored=electric_energy_stored)
    # Discharge to output
    energy_consumption = consumption.compute_internal_to_out(snap=snap,
                                                             delta_t=delta_t)
    result = power_out * delta_t / eff1
    assert energy_consumption == result
    # Discharge to input
    energy_consumption = consumption.compute_internal_to_in(snap=snap,
                                                            delta_t=delta_t)
    result = power_in * delta_t / eff1
    assert energy_consumption == result
    # Recharge from output
    energy_recovered = consumption.compute_out_to_internal(snap=snap,
                                                           delta_t=delta_t)
    result = power_out * delta_t * eff2
    assert energy_recovered == result
    # Recharge from input
    energy_recovered = consumption.compute_in_to_internal(snap=snap,
                                                          delta_t=delta_t)
    result = power_in * delta_t * eff2
    assert energy_recovered == result

def test_non_rechargeable_battery_consumption() -> None:
    consumption = create_non_rechargeable_battery_consumption(discharge_eff=eff1)
    snap = return_non_rechargeable_battery_snapshot(electric_power_out=power_out,
                                                    electric_energy_stored=electric_energy_stored)
    # Discharge to output
    energy_consumption = consumption.compute_internal_to_out(snap=snap,
                                                             delta_t=delta_t)
    result = power_out * delta_t / eff1
    assert energy_consumption == result

def test_electric_generator_consumption() -> None:
    consumption = create_electric_generator_consumption(gen_eff=eff1)
    snap = return_electric_generator_snapshot(torque_in=torque_in,
                                              electric_power_out=power_out,
                                              rpm_in=rpm_in)
    energy_consumption = consumption.compute_in_to_out(snap=snap,
                                                       delta_t=delta_t)
    result = power_out * delta_t / eff1
    assert energy_consumption == result

def test_electric_motor_consumption() -> None:
    consumption = create_electric_motor_consumption(motor_eff=eff1,
                                                    gen_eff=eff2)
    snap = return_electric_motor_snapshot(electric_power_in=power_in,
                                          torque_out=torque_out,
                                          rpm_out=rpm_out)
    # Acting as motor
    energy_consumption = consumption.compute_in_to_out(snap=snap,
                                                       delta_t=delta_t)
    result = torque_to_power(torque=torque_out,
                             rpm=rpm_out) * delta_t / eff1
    assert energy_consumption == result
    # Acting as generator
    energy_consumption = consumption.compute_out_to_in(snap=snap,
                                                       delta_t=delta_t)
    result = power_in * delta_t / eff2
    assert energy_consumption == result

def test_create_liquid_combustion_engine_consumption() -> None:
    consumption = create_liquid_combustion_engine_consumption(fuel_cons=fuel_cons_per_sec)
    for fuel in LIQUID_FUELS:
        snap = return_liquid_ice_snapshot(fuel_in=fuel,
                                          liters_flow_in=fuel_liters_in,
                                          torque_out=torque_out,
                                          rpm_out=rpm_out)
        fuel_consumption = consumption.compute_in_to_out(snap=snap,
                                                         delta_t=delta_t)
        result = fuel_cons_per_sec * delta_t
        assert fuel_consumption == result

def test_create_gaseous_combustion_engine_consumption() -> None:
    consumption = create_gaseous_combustion_engine_consumption(fuel_cons=fuel_cons_per_sec)
    for fuel in GASEOUS_FUELS:
        snap = return_gaseous_ice_snapshot(fuel_in=fuel,
                                           mass_flow_in=fuel_mass_in,
                                           torque_out=torque_out,
                                           rpm_out=rpm_out)
        fuel_consumption = consumption.compute_in_to_out(snap=snap,
                                                         delta_t=delta_t)
        result = fuel_cons_per_sec * delta_t
        assert fuel_consumption == result

def test_create_fuel_cell_consumption() -> None:
    consumption = create_fuel_cell_consumption(fuel_cons=fuel_cons_per_sec)
    for fuel in GASEOUS_FUELS:
        snap = return_fuel_cell_snapshot(fuel_in=fuel,
                                         mass_flow_in=fuel_mass_in,
                                         electric_power_out=power_out)
        fuel_consumption = consumption.compute_in_to_out(snap=snap,
                                                         delta_t=delta_t)
        result = fuel_cons_per_sec * delta_t
        assert fuel_consumption == result

def test_create_electric_inverter_consumption() -> None:
    consumption = create_electric_inverter_consumption(eff=eff1)
    snap = return_electric_inverter_snapshot(electric_power_in=power_in,
                                             electric_power_out=power_out)
    energy_consumption = consumption.compute_in_to_out(snap=snap,
                                                       delta_t=delta_t)
    result = power_out * delta_t / eff1
    assert energy_consumption == result

def test_create_electric_rectifier_consumption() -> None:
    consumption = create_electric_rectifier_consumption(eff=eff1)
    snap = return_electric_rectifier_snapshot(electric_power_in=power_in,
                                              electric_power_out=power_out)
    energy_consumption = consumption.compute_in_to_out(snap=snap,
                                                       delta_t=delta_t)
    result = power_out * delta_t / eff1
    assert energy_consumption == result

def test_create_gearbox_consumption() -> None:
    consumption = create_gearbox_consumption(eff=eff1,
                                             rev_eff=eff2)
    snap = return_gearbox_snapshot(torque_in=torque_in,
                                   torque_out=torque_out,
                                   rpm_in=rpm_in,
                                   rpm_out=rpm_out)
    # Forward conversion
    energy_consumption = consumption.compute_in_to_out(snap=snap,
                                                       delta_t=delta_t)
    result = torque_to_power(torque=torque_out,
                             rpm=rpm_out) * delta_t / eff1
    assert energy_consumption == result
    # Reverse conversion
    energy_consumption = consumption.compute_out_to_in(snap=snap,
                                                       delta_t=delta_t)
    result = torque_to_power(torque=torque_in,
                             rpm=rpm_in) * delta_t / eff2
    assert energy_consumption == result
