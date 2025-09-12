"""This module contains test routines for the component snapshot classes."""

from components.component_snapshot import ElectricMotorSnapshot, ElectricGeneratorSnapshot, \
    LiquidCombustionEngineSnapshot, GaseousCombustionEngineSnapshot, FuelCellSnapshot, \
    ElectricInverterSnapshot, ElectricRectifierSnapshot, GearBoxSnapshot, \
    NonRechargeableBatterySnapshot, RechargeableBatterySnapshot, \
    LiquidFuelTankSnapshot, GaseousFuelTankSnapshot, \
    return_electric_motor_snapshot, return_electric_generator_snapshot, \
    return_electric_inverter_snapshot, return_electric_rectifier_snapshot, \
    return_liquid_ice_snapshot, return_gaseous_ice_snapshot, \
    return_fuel_cell_snapshot, return_gearbox_snapshot, \
    return_non_rechargeable_battery_snapshot, return_rechargeable_battery_snapshot, \
    return_liquid_fuel_tank_snapshot, return_gaseous_fuel_tank_snapshot
from components.fuel_type import LiquidFuel, GaseousFuel, LIQUID_FUELS, GASEOUS_FUELS
from helpers.functions import torque_to_power
from simulation.constants import DEFAULT_TEMPERATURE

electric_power_in: float = 10_000.0
electric_power_out: float = 9_100.0
torque_in: float = 20.0
rpm_in: float = 1_200.0
torque_out: float = 15.0
rpm_out: float = 1_100.0
temperature: float = DEFAULT_TEMPERATURE
liters_flow_in: float = 0.54
liters_flow_out: float = 0.57
mass_flow_in: float = 0.61
mass_flow_out: float = 0.67
electric_energy_stored: float = 50_000.0
liters_stored: float = 50.0
mass_stored: float = 45.0

def create_electric_motor_snapshot() -> ElectricMotorSnapshot:
    return return_electric_motor_snapshot(electric_power_in=electric_power_in,
                                          torque_out=torque_out,
                                          temperature=temperature,
                                          on=True,
                                          rpm_out=rpm_out)

def create_electric_generator_snapshot() -> ElectricGeneratorSnapshot:
    return return_electric_generator_snapshot(torque_in=torque_in,
                                              electric_power_out=electric_power_out,
                                              rpm_in=rpm_in,
                                              temperature=temperature)

def create_electric_inverter_snapshot() -> ElectricInverterSnapshot:
    return return_electric_inverter_snapshot(electric_power_in=electric_power_in,
                                             electric_power_out=electric_power_out,
                                             temperature=temperature)

def create_electric_rectifier_snapshot() -> ElectricRectifierSnapshot:
    return return_electric_rectifier_snapshot(electric_power_in=electric_power_in,
                                              electric_power_out=electric_power_out,
                                              temperature=temperature)

def create_liquid_ice_snapshot(fuel_in: LiquidFuel) -> LiquidCombustionEngineSnapshot:
    return return_liquid_ice_snapshot(fuel_in=fuel_in,
                                      liters_flow_in=liters_flow_in,
                                      torque_out=torque_out,
                                      temperature=temperature,
                                      on=True,
                                      rpm_out=rpm_out)

def create_gaseous_ice_snapshot(fuel_in: GaseousFuel) -> GaseousCombustionEngineSnapshot:
    return return_gaseous_ice_snapshot(fuel_in=fuel_in,
                                       mass_flow_in=mass_flow_in,
                                       torque_out=torque_out,
                                       temperature=temperature,
                                       on=True,
                                       rpm_out=rpm_out)

def create_fuel_cell_snapshot(fuel_in: GaseousFuel) -> FuelCellSnapshot:
    return return_fuel_cell_snapshot(fuel_in=fuel_in,
                                     mass_flow_in=mass_flow_in,
                                     electric_power_out=electric_power_out,
                                     temperature=temperature)

def create_gearbox_snapshot() -> GearBoxSnapshot:
    return return_gearbox_snapshot(torque_in=torque_in,
                                   torque_out=torque_out,
                                   rpm_in=rpm_in,
                                   rpm_out=rpm_out,
                                   temperature=temperature)

# ========================

def create_non_rechargeable_battery_snapshot() -> NonRechargeableBatterySnapshot:
    return return_non_rechargeable_battery_snapshot(electric_power_out=electric_power_out,
                                                    temperature=temperature,
                                                    electric_energy_stored=electric_energy_stored)

def create_rechargeable_battery_snapshot() -> RechargeableBatterySnapshot:
    return return_rechargeable_battery_snapshot(electric_power_in=electric_power_in,
                                                electric_power_out=electric_power_out,
                                                temperature=temperature,
                                                electric_energy_stored=electric_energy_stored)

def create_liquid_fuel_tank_snapshot(fuel: LiquidFuel) -> LiquidFuelTankSnapshot:
    return return_liquid_fuel_tank_snapshot(fuel=fuel,
                                            liters_flow_out=liters_flow_out,
                                            temperature=temperature,
                                            liters_stored=liters_stored)

def create_gaseous_fuel_tank_snapshot(fuel: GaseousFuel) -> GaseousFuelTankSnapshot:
    return return_gaseous_fuel_tank_snapshot(fuel=fuel,
                                             mass_flow_out=mass_flow_out,
                                             temperature=temperature,
                                             mass_stored=mass_stored)

# ========================

def test_create_electric_motor_snapshot() -> None:
    em_snap = create_electric_motor_snapshot()
    assert isinstance(em_snap, ElectricMotorSnapshot)
    assert em_snap.power_in==electric_power_in
    assert em_snap.power_out==torque_to_power(torque=torque_out,
                                              rpm=rpm_out)

def test_create_electric_generator_snapshot() -> None:
    eg_snap = create_electric_generator_snapshot()
    assert isinstance(eg_snap, ElectricGeneratorSnapshot)
    assert eg_snap.power_in==torque_to_power(torque=torque_in,
                                             rpm=rpm_in)
    assert eg_snap.power_out==electric_power_out

def test_create_electric_inverter_snapshot() -> None:
    ei_snap = create_electric_inverter_snapshot()
    assert isinstance(ei_snap, ElectricInverterSnapshot)
    assert ei_snap.power_in==electric_power_in
    assert ei_snap.power_out==electric_power_out

def test_create_electric_rectifier_snapshot() -> None:
    er_snap = create_electric_rectifier_snapshot()
    assert isinstance(er_snap, ElectricRectifierSnapshot)
    assert er_snap.power_in==electric_power_in
    assert er_snap.power_out==electric_power_out

def test_create_liquid_ice_snapshot() -> None:
    for fuel in LIQUID_FUELS:
        l_ice = create_liquid_ice_snapshot(fuel_in=fuel)
        assert isinstance(l_ice, LiquidCombustionEngineSnapshot)
        assert l_ice.fuel_consumption_in==liters_flow_in
        assert l_ice.power_out==torque_to_power(torque=torque_out,
                                                rpm=rpm_out)

def test_create_gaseous_ice_snapshot() -> None:
    for fuel in GASEOUS_FUELS:
        g_ice_snap = create_gaseous_ice_snapshot(fuel_in=fuel)
        assert isinstance(g_ice_snap, GaseousCombustionEngineSnapshot)
        assert g_ice_snap.fuel_consumption_in==mass_flow_in
        assert g_ice_snap.power_out==torque_to_power(torque=torque_out,
                                                  rpm=rpm_out)

def test_create_fuel_cell_snapshot() -> None:
    for fuel in GASEOUS_FUELS:
        fc_snap = create_fuel_cell_snapshot(fuel_in=fuel)
        assert isinstance(fc_snap, FuelCellSnapshot)
        assert fc_snap.fuel_consumption_in==mass_flow_in
        assert fc_snap.power_out==electric_power_out

def test_create_gearbox_snapshot() -> None:
    gb_snap = create_gearbox_snapshot()
    assert isinstance(gb_snap, GearBoxSnapshot)
    assert gb_snap.power_in==torque_to_power(torque=torque_in,
                                             rpm=rpm_in)
    assert gb_snap.power_out==torque_to_power(torque=torque_out,
                                              rpm=rpm_out)

# ========================

def test_create_non_rechargeable_battery_snapshot() -> None:
    nr_bat = create_non_rechargeable_battery_snapshot()
    assert isinstance(nr_bat, NonRechargeableBatterySnapshot)
    assert nr_bat.power_out==electric_power_out
    assert nr_bat.state.internal.electric_energy_stored==electric_energy_stored

def test_create_rechargeable_battery_snapshot() -> None:
    r_bat = create_rechargeable_battery_snapshot()
    assert isinstance(r_bat, RechargeableBatterySnapshot)
    assert r_bat.power_in==electric_power_in
    assert r_bat.power_out==electric_power_out
    assert r_bat.state.internal.electric_energy_stored==electric_energy_stored

def test_create_liquid_fuel_tank_snapshot() -> None:
    for fuel in LIQUID_FUELS:
        lft_snap = create_liquid_fuel_tank_snapshot(fuel=fuel)
        assert isinstance(lft_snap, LiquidFuelTankSnapshot)
        assert lft_snap.fuel_out==liters_flow_out
        assert lft_snap.state.internal.liters_stored==liters_stored

def test_create_gaseous_fuel_tank_snapshot() -> None:
    for fuel in GASEOUS_FUELS:
        gft_snap = create_gaseous_fuel_tank_snapshot(fuel=fuel)
        assert isinstance(gft_snap, GaseousFuelTankSnapshot)
        assert gft_snap.fuel_out==mass_flow_out
        assert gft_snap.state.internal.mass_stored==mass_stored
