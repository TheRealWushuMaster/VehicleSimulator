"""This module contains methods for testing consumption classes."""

from components.consumption import \
    RechargeableBatteryConsumption, NonRechargeableBatteryConsumption, \
    ElectricGeneratorConsumption, ElectricMotorConsumption, \
    CombustionEngineConsumption, FuelCellConsumption, \
    PureElectricConsumption, PureMechanicalConsumption, \
    return_rechargeable_battery_consumption, return_non_rechargeable_battery_consumption, \
    return_electric_generator_consumption, return_electric_motor_consumption, \
    return_combustion_engine_consumption, return_fuel_cell_consumption, \
    return_pure_electric_consumption, return_pure_mechanical_consumption
from components.state import return_rechargeable_battery_state, return_non_rechargeable_battery_state, \
    return_electric_generator_state, return_electric_motor_state, \
    return_liquid_combustion_engine_state, return_gaseous_combustion_engine_state, \
    return_fuel_cell_state, return_pure_electric_state, return_pure_mechanical_state

delta_t: float = 0.1
eff1: float = 0.95
eff2: float = 0.90
fuel_cons_per_sec: float = 0.5
electric_energy_stored: float = 1_000
voltage1: float = 300.0
current1: float = 100.0
voltage2: float = 250.0
current2: float = 80.0


def create_rechargeable_battery_consumption(eff: float,
                                            rev_eff: float
                                            ) -> RechargeableBatteryConsumption:
    consumption = return_rechargeable_battery_consumption(
        efficiency_func=lambda s: eff,
        reverse_efficiency_func=lambda s: rev_eff
    )
    assert isinstance(consumption, RechargeableBatteryConsumption)
    return consumption

def create_non_rechargeable_battery_consumption(eff: float
                                                ) -> NonRechargeableBatteryConsumption:
    consumption = return_non_rechargeable_battery_consumption(
        efficiency_func=lambda s: eff
    )
    assert isinstance(consumption, NonRechargeableBatteryConsumption)
    return consumption

def create_electric_generator_consumption(eff: float
                                          ) -> ElectricGeneratorConsumption:
    consumption = return_electric_generator_consumption(
        efficiency_func=lambda s: eff
    )
    assert isinstance(consumption, ElectricGeneratorConsumption)
    return consumption

def create_electric_motor_consumption(eff: float,
                                      rev_eff: float
                                      ) -> ElectricMotorConsumption:
    consumption = return_electric_motor_consumption(
        efficiency_func=lambda s: eff,
        reverse_efficiency_func=lambda s: rev_eff
    )
    assert isinstance(consumption, ElectricMotorConsumption)
    return consumption

def create_combustion_engine_consumption(fuel_cons: float
                                         ) -> CombustionEngineConsumption:
    consumption = return_combustion_engine_consumption(
        fuel_consumption_func=lambda s: fuel_cons
    )
    assert isinstance(consumption, CombustionEngineConsumption)
    return consumption

def create_fuel_cell_consumption(fuel_cons: float
                                 ) -> FuelCellConsumption:
    consumption = return_fuel_cell_consumption(
        fuel_consumption_func=lambda s: fuel_cons
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


def test_rechargeable_battery_consumption() -> None:
    consumption = create_rechargeable_battery_consumption(eff=eff1,
                                                          rev_eff=eff2)
    # Discharge
    state = return_rechargeable_battery_state(energy=electric_energy_stored,
                                              voltage_out=voltage2,
                                              current_out=current2)
    energy_consumption = consumption.internal.compute(state=state,
                                                      delta_t=delta_t)
    result = voltage2 * current2 * delta_t / eff1
    assert energy_consumption == result

    # Recharge
    state = return_rechargeable_battery_state(energy=electric_energy_stored,
                                              voltage_in=voltage1,
                                              current_in=current1)
    energy_recovered = consumption.internal.reverse_compute(state=state,
                                                            delta_t=delta_t)
    result = voltage1 * current1 * delta_t * eff2
    assert energy_recovered == result
