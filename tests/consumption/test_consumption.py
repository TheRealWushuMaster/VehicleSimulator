"""This module contains methods for testing consumption classes."""

from components.consumption import \
    RechargeableBatteryConsumption, NonRechargeableBatteryConsumption, \
    ElectricGeneratorConsumption, ElectricMotorConsumption, \
    LiquidCombustionEngineConsumption, GaseousCombustionEngineConsumption, \
    FuelCellConsumption, \
    PureElectricConsumption, PureMechanicalConsumption, \
    return_rechargeable_battery_consumption, return_non_rechargeable_battery_consumption, \
    return_electric_generator_consumption, return_electric_motor_consumption, \
    return_liquid_combustion_engine_consumption, return_gaseous_combustion_engine_consumption, \
    return_fuel_cell_consumption, \
    return_pure_electric_consumption, return_pure_mechanical_consumption
from components.fuel_type import LIQUID_FUELS, GASEOUS_FUELS
from components.state import return_rechargeable_battery_state, return_non_rechargeable_battery_state, \
    return_electric_generator_state, return_electric_motor_state, \
    return_liquid_combustion_engine_state, return_gaseous_combustion_engine_state, \
    return_fuel_cell_state, return_pure_electric_state, return_pure_mechanical_state
from helpers.functions import torque_to_power
from helpers.types import ElectricSignalType


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
    func = lambda s: fuel_cons * s.output.power
    consumption = return_liquid_combustion_engine_consumption(
        fuel_consumption_func=func
    )
    assert isinstance(consumption, LiquidCombustionEngineConsumption)
    return consumption

def create_gaseous_combustion_engine_consumption(fuel_cons: float
                                                 ) -> GaseousCombustionEngineConsumption:
    func = lambda s: fuel_cons * s.output.power
    consumption = return_gaseous_combustion_engine_consumption(
        fuel_consumption_func=func
    )
    assert isinstance(consumption, GaseousCombustionEngineConsumption)
    return consumption

def create_fuel_cell_consumption(fuel_cons: float
                                 ) -> FuelCellConsumption:
    func = lambda s: fuel_cons * s.output.power
    consumption = return_fuel_cell_consumption(
        fuel_consumption_func=func
    )
    assert isinstance(consumption, FuelCellConsumption)
    return consumption

def create_pure_electric_consumption(eff: float
                                     ) -> PureElectricConsumption:
    consumption = return_pure_electric_consumption(
        efficiency_func=lambda s: eff
    )
    assert isinstance(consumption, PureElectricConsumption)
    return consumption

def create_pure_mechanical_consumption(eff: float,
                                       rev_eff: float
                                       ) -> PureMechanicalConsumption:
    consumption = return_pure_mechanical_consumption(
        efficiency_func=lambda s: eff,
        reverse_efficiency_func=lambda s: rev_eff
    )
    assert isinstance(consumption, PureMechanicalConsumption)
    return consumption

# =========================

def test_rechargeable_battery_consumption() -> None:
    consumption = create_rechargeable_battery_consumption(discharge_eff=eff1,
                                                          recharge_eff=eff2)
    state = return_rechargeable_battery_state(energy=electric_energy_stored,
                                              nominal_voltage=voltage_in,
                                              power_in=power_in,
                                              power_out=power_out)
    # Discharge to output
    energy_consumption = consumption.compute_internal_to_out(state=state,
                                                             delta_t=delta_t)
    result = power_out * delta_t / eff1
    assert energy_consumption == result
    # Discharge to input
    energy_consumption = consumption.compute_internal_to_in(state=state,
                                                            delta_t=delta_t)
    result = power_in * delta_t / eff1
    assert energy_consumption == result
    # Recharge from output
    energy_recovered = consumption.compute_out_to_internal(state=state,
                                                           delta_t=delta_t)
    result = power_out * delta_t * eff2
    assert energy_recovered == result
    # Recharge from input
    energy_recovered = consumption.compute_in_to_internal(state=state,
                                                          delta_t=delta_t)
    result = power_in * delta_t * eff2
    assert energy_recovered == result

def test_non_rechargeable_battery_consumption() -> None:
    consumption = create_non_rechargeable_battery_consumption(discharge_eff=eff1)
    state = return_non_rechargeable_battery_state(energy=electric_energy_stored,
                                                  power_out=power_out)
    # Discharge to output
    energy_consumption = consumption.compute_internal_to_out(state=state,
                                                             delta_t=delta_t)
    result = power_out * delta_t / eff1
    assert energy_consumption == result

def test_electric_generator_consumption() -> None:
    consumption = create_electric_generator_consumption(gen_eff=eff1)
    state = return_electric_generator_state(torque_in=torque_in,
                                            rpm_in=rpm_in,
                                            power_out=power_out)
    energy_consumption = consumption.compute_in_to_out(state=state,
                                                       delta_t=delta_t)
    result = power_out * delta_t / eff1
    assert energy_consumption == result

def test_electric_motor_consumption() -> None:
    consumption = create_electric_motor_consumption(motor_eff=eff1,
                                                    gen_eff=eff2)
    state = return_electric_motor_state(signal_type=ElectricSignalType.AC,
                                        power_in=power_in,
                                        torque_out=torque_out,
                                        rpm_out=rpm_out)
    # Acting as motor
    energy_consumption = consumption.compute_in_to_out(state=state,
                                                       delta_t=delta_t)
    result = torque_to_power(torque=torque_out,
                             rpm=rpm_out) * delta_t / eff1
    assert energy_consumption == result
    # Acting as generator
    energy_consumption = consumption.compute_out_to_in(state=state,
                                                       delta_t=delta_t)
    result = power_in * delta_t / eff2
    assert energy_consumption == result

def test_create_liquid_combustion_engine_consumption() -> None:
    consumption = create_liquid_combustion_engine_consumption(fuel_cons=fuel_cons_per_sec)
    for fuel in LIQUID_FUELS:
        state = return_liquid_combustion_engine_state(fuel=fuel,
                                                      fuel_liters_in=fuel_liters_in,
                                                      torque_out=torque_out,
                                                      rpm_out=rpm_out)
        fuel_consumption = consumption.compute_in_to_out(state=state,
                                                         delta_t=delta_t)
        result = state.output.power * fuel_cons_per_sec * delta_t
        assert fuel_consumption == result

def test_create_gaseous_combustion_engine_consumption() -> None:
    consumption = create_gaseous_combustion_engine_consumption(fuel_cons=fuel_cons_per_sec)
    for fuel in GASEOUS_FUELS:
        state = return_gaseous_combustion_engine_state(fuel=fuel,
                                                       fuel_mass_in=fuel_mass_in,
                                                       torque_out=torque_out,
                                                       rpm_out=rpm_out)
        fuel_consumption = consumption.compute_in_to_out(state=state,
                                                         delta_t=delta_t)
        result = state.output.power * fuel_cons_per_sec * delta_t
        assert fuel_consumption == result

def test_create_fuel_cell_consumption() -> None:
    consumption = create_fuel_cell_consumption(fuel_cons=fuel_cons_per_sec)
    for fuel in GASEOUS_FUELS:
        state = return_fuel_cell_state(fuel=fuel,
                                       fuel_mass_in=fuel_mass_in,
                                       power_out=power_out)
        fuel_consumption = consumption.compute_in_to_out(state=state,
                                                         delta_t=delta_t)
        result = state.output.power * fuel_cons_per_sec * delta_t
        assert fuel_consumption == result

def test_create_pure_electric_consumption() -> None:
    consumption = create_pure_electric_consumption(eff=eff1)
    state = return_pure_electric_state(signal_type_in=ElectricSignalType.DC,
                                       signal_type_out=ElectricSignalType.DC,
                                       power_in=power_in,
                                       power_out=power_out)
    energy_consumption = consumption.compute_in_to_out(state=state,
                                                       delta_t=delta_t)
    result = power_out * delta_t / eff1
    assert energy_consumption == result

def test_create_pure_mechanical_consumption() -> None:
    consumption = create_pure_mechanical_consumption(eff=eff1,
                                                     rev_eff=eff2)
    state = return_pure_mechanical_state(torque_in=torque_in,
                                         rpm_in=rpm_in,
                                         torque_out=torque_out,
                                         rpm_out=rpm_out)
    # Forward conversion
    energy_consumption = consumption.compute_in_to_out(state=state,
                                                       delta_t=delta_t)
    result = torque_to_power(torque=torque_out,
                             rpm=rpm_out) * delta_t / eff1
    assert energy_consumption == result
    # Reverse conversion
    energy_consumption = consumption.compute_out_to_in(state=state,
                                                       delta_t=delta_t)
    result = torque_to_power(torque=torque_in,
                             rpm=rpm_in) * delta_t / eff2
    assert energy_consumption == result
