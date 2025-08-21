"""
This module contains definitions for different types of fuel cells.
"""

from typing import Optional
from dataclasses import dataclass
from components.fuel_cell_curves import FuelCellEfficiencyCurves
from components.fuel_type import GaseousFuel, HydrogenGas
from components.consumption import FuelCellConsumption
from components.converter import Converter
from components.dynamic_response import FuelCellDynamicResponse
from components.dynamic_response_curves import FuelToElectric
from components.limitation import FuelCellLimits
from components.port import PortInput, PortOutput
from components.state import return_fuel_cell_state
from helpers.functions import assert_type, assert_type_and_range
from helpers.types import PowerType

fuel_cell_params = {"PEMembraneFC": {"EffAtZeroPower": 0.075,
                                     "MaxEfficiencyValue": 0.50,
                                     "MaxEfficiencyPower": 0.50,
                                     "EfficiencyAtMaxPower": 0.375,
                                     "MassPerKW": 1.0,
                                     "Fuel": HydrogenGas()},
                    "SolidOxideFC": {"EffAtZeroPower": 0.125,
                                     "MaxEfficiencyValue": 0.60,
                                     "MaxEfficiencyPower": 0.40,
                                     "EfficiencyAtMaxPower": 0.475,
                                     "MassPerKW": 12.5,
                                     "Fuel": HydrogenGas()},
                    "PhAcidFC": {"EffAtZeroPower": 0.10,
                                 "MaxEfficiencyValue": 0.40,
                                 "MaxEfficiencyPower": 0.60,
                                 "EfficiencyAtMaxPower": 0.325,
                                 "MassPerKW": 6.5,
                                 "Fuel": HydrogenGas()},
                    "AlkalineFC": {"EffAtZeroPower": 0.125,
                                   "MaxEfficiencyValue": 0.60,
                                   "MaxEfficiencyPower": 0.50,
                                   "EfficiencyAtMaxPower": 0.475,
                                   "MassPerKW": 4.0,
                                   "Fuel": HydrogenGas()},
                    "MoltenCarbonateFC": {"EffAtZeroPower": 0.15,
                                          "MaxEfficiencyValue": 0.50,
                                          "MaxEfficiencyPower": 0.45,
                                          "EfficiencyAtMaxPower": 0.425,
                                          "MassPerKW": 10.0,
                                          "Fuel": HydrogenGas()}, # Should be natural gas
                    "DirectMethanolFC": {"EffAtZeroPower": 0.055,
                                         "MaxEfficiencyValue": 0.25,
                                         "MaxEfficiencyPower": 0.30,
                                         "EfficiencyAtMaxPower": 0.175,
                                         "MassPerKW": 3.0,
                                         "Fuel": HydrogenGas()}} # Should be liquid methanol


@dataclass
class FuelCell(Converter):
    """Models a generic Fuel Cell."""
    nominal_voltage: float
    max_power: float

    def __init__(self,
                 name: str,
                 mass: float,
                 nominal_voltage: float,
                 limits: FuelCellLimits,
                 consumption: FuelCellConsumption,
                 max_power: float,
                 fuel: GaseousFuel,
                 dynamic_response: Optional[FuelCellDynamicResponse]=None):
        assert_type_and_range(mass, nominal_voltage, max_power,
                              more_than=0.0,
                              include_more=False)
        assert_type(limits,
                    expected_type=FuelCellLimits)
        assert_type(consumption,
                    expected_type=FuelCellConsumption)
        if dynamic_response is None:
            dynamic_response = FuelCellDynamicResponse(
                forward_response=FuelToElectric.gaseous_fuel_to_electric()
            )
        else:
            assert_type(dynamic_response,
                        expected_type=FuelCellDynamicResponse)
        assert_type(fuel,
                    expected_type=GaseousFuel)
        state = return_fuel_cell_state(fuel=fuel)
        super().__init__(name=name,
                         mass=mass,
                         input=PortInput(exchange=fuel),
                         output=PortOutput(exchange=PowerType.ELECTRIC_DC),
                         state=state,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response)
        self.nominal_voltage = nominal_voltage
        self.max_power = max_power


@dataclass
class PEMembraneFC(FuelCell):
    """Models a Polymer Electrolyte Membrane Fuel Cell."""
    def __init__(self,
                 name: str,
                 nominal_voltage: float,
                 limits: FuelCellLimits,
                 max_power: float,
                 dynamic_response: Optional[FuelCellDynamicResponse]=None):
        assert_type_and_range(nominal_voltage, max_power,
                              more_than=0.0,
                              include_more=False)
        values = fuel_cell_params["PEMembraneFC"]
        mass, consumption, fuel = return_fuel_cell_params(values=values,
                                                          max_power=max_power)
        super().__init__(name=name,
                         mass=mass,
                         nominal_voltage=nominal_voltage,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         max_power=max_power,
                         fuel=fuel)


@dataclass
class DirectMethanolFC(FuelCell):
    """Models a Direct Methanol Fuel Cell."""
    def __init__(self,
                 name: str,
                 nominal_voltage: float,
                 limits: FuelCellLimits,
                 max_power: float,
                 dynamic_response: Optional[FuelCellDynamicResponse]=None):
        assert_type_and_range(nominal_voltage, max_power,
                              more_than=0.0,
                              include_more=False)
        values = fuel_cell_params["DirectMethanolFC"]
        mass, consumption, fuel = return_fuel_cell_params(values=values,
                                                          max_power=max_power)
        super().__init__(name=name,
                         mass=mass,
                         nominal_voltage=nominal_voltage,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         max_power=max_power,
                         fuel=fuel)


@dataclass
class AlkalineFC(FuelCell):
    """Models an Alkaline Fuel Cell"""
    def __init__(self,
                 name: str,
                 nominal_voltage: float,
                 limits: FuelCellLimits,
                 max_power: float,
                 dynamic_response: Optional[FuelCellDynamicResponse]=None):
        assert_type_and_range(nominal_voltage, max_power,
                              more_than=0.0,
                              include_more=False)
        values = fuel_cell_params["AlkalineFC"]
        mass, consumption, fuel = return_fuel_cell_params(values=values,
                                                          max_power=max_power)
        super().__init__(name=name,
                         mass=mass,
                         nominal_voltage=nominal_voltage,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         max_power=max_power,
                         fuel=fuel)


@dataclass
class PhAcidFC(FuelCell):
    """Models a Phosphoric Acid Fuel Cell."""
    def __init__(self,
                 name: str,
                 nominal_voltage: float,
                 limits: FuelCellLimits,
                 max_power: float,
                 dynamic_response: Optional[FuelCellDynamicResponse]=None):
        assert_type_and_range(nominal_voltage, max_power,
                              more_than=0.0,
                              include_more=False)
        values = fuel_cell_params["PhAcidFC"]
        mass, consumption, fuel = return_fuel_cell_params(values=values,
                                                          max_power=max_power)
        super().__init__(name=name,
                         mass=mass,
                         nominal_voltage=nominal_voltage,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         max_power=max_power,
                         fuel=fuel)


@dataclass
class MoltenCarbonateFC(FuelCell):
    """Models a Molten Carbonate Fuel Cell."""
    def __init__(self,
                 name: str,
                 nominal_voltage: float,
                 limits: FuelCellLimits,
                 max_power: float,
                 dynamic_response: Optional[FuelCellDynamicResponse]=None):
        assert_type_and_range(nominal_voltage, max_power,
                              more_than=0.0,
                              include_more=False)
        values = fuel_cell_params["MoltenCarbonateFC"]
        mass, consumption, fuel = return_fuel_cell_params(values=values,
                                                          max_power=max_power)
        super().__init__(name=name,
                         mass=mass,
                         nominal_voltage=nominal_voltage,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         max_power=max_power,
                         fuel=fuel)


@dataclass
class SolidOxideFC(FuelCell):
    """Models a Solid Oxide Fuel Cell."""
    def __init__(self,
                 name: str,
                 nominal_voltage: float,
                 limits: FuelCellLimits,
                 max_power: float,
                 dynamic_response: Optional[FuelCellDynamicResponse]=None):
        assert_type_and_range(nominal_voltage, max_power,
                              more_than=0.0,
                              include_more=False)
        values = fuel_cell_params["SolidOxideFC"]
        mass, consumption, fuel = return_fuel_cell_params(values=values,
                                                          max_power=max_power)
        super().__init__(name=name,
                         mass=mass,
                         nominal_voltage=nominal_voltage,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         max_power=max_power,
                         fuel=fuel)


def return_fuel_cell_params(values: dict,
                            max_power: float
                            ) -> tuple[float,
                                       FuelCellConsumption,
                                       GaseousFuel]:
    power_peak_eff = values["MaxEfficiencyPower"] * max_power
    peak_eff = values["MaxEfficiencyValue"]
    consumption = FuelCellConsumption(
        in_to_out_fuel_consumption_func=FuelCellEfficiencyCurves.gaussian(
            min_power=0.0, min_power_eff=values["EffAtZeroPower"],
            power_peak_eff=power_peak_eff, peak_eff=peak_eff,
            max_power=max_power, max_power_eff=values["EfficiencyAtMaxPower"]
        )
    )
    mass = max_power * values["MassPerKW"] / 1_000.0
    fuel = values["Fuel"]
    return mass, consumption, fuel

FUEL_CELL_TYPES = [PhAcidFC, AlkalineFC, PEMembraneFC,
                   SolidOxideFC, DirectMethanolFC,
                   MoltenCarbonateFC]
