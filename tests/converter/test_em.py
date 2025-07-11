"""This module contains routines for testing Electric Motor creation."""

from typing import Literal, TypedDict
from components.motor import ElectricMotor, ElectricGenerator
from components.motor_curves import MechanicalMaxPowerVsRPMCurves, \
    MechanicalPowerEfficiencyCurves
from components.state import MechanicalState, zero_mechanical_state


class TestEMParams(TypedDict):
    mass: float
    max_power: float
    min_rpm: float
    max_rpm: float
    efficiency: float
    state: MechanicalState


em_defaults: TestEMParams = {"mass": 50.0,
                             "max_power": 50_000.0,
                             "min_rpm": 800.0,
                             "max_rpm": 5_000.0,
                             "efficiency": 0.91,
                             "state": zero_mechanical_state()}

# ============================

def create_electric_machine(machine_type: Literal["eg", "em"],
                            mass: float=em_defaults["mass"],
                            max_power: float=em_defaults["max_power"],
                            state: MechanicalState=em_defaults["state"]
                            ) -> ElectricGenerator|ElectricMotor:
    assert machine_type in ("eg", "em")
    power_func = MechanicalMaxPowerVsRPMCurves.constant(max_power=max_power,
                                                        max_rpm=em_defaults["max_rpm"],
                                                        min_rpm=em_defaults["min_rpm"])
    eff_func = MechanicalPowerEfficiencyCurves.constant(efficiency=em_defaults["efficiency"],
                                                        max_rpm=em_defaults["max_rpm"],
                                                        min_rpm=em_defaults["min_rpm"],
                                                        max_power_vs_rpm=power_func)
    if machine_type=="eg":
        return ElectricGenerator(name="Test Electric Generator",
                                 mass=mass,
                                 max_power=max_power,
                                 eff_func=eff_func,
                                 state=state,
                                 power_func=power_func)
    return ElectricMotor(name="Test Electric Motor",
                         mass=mass,
                         max_power=max_power,
                         eff_func=eff_func,
                         reverse_efficiency=1.0,
                         state=state,
                         power_func=power_func)

# ============================

def test_create_electric_generator() -> None:
    eg = create_electric_machine(machine_type="eg")
    assert isinstance(eg, ElectricGenerator)

def test_create_electric_motor() -> None:
    em = create_electric_machine(machine_type="em")
    assert isinstance(em, ElectricMotor)
