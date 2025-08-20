"""This module contains class definitions for electric converters."""

from dataclasses import dataclass
from components.consumption import PureElectricConsumption
from components.converter import Converter
from components.dynamic_response import InverterDynamicResponse, \
    RectifierDynamicResponse
from components.limitation import ElectricToElectricLimits
from components.port import PortInput, PortOutput
from components.state import return_pure_electric_state
from helpers.functions import assert_type_and_range
from helpers.types import ElectricSignalType, PowerType


@dataclass
class PureElectricConverter(Converter):
    """
    Base class for electric to electric converters.
    """
    max_power: float
    nominal_voltage_in: float
    nominal_voltage_out: float

    def __post_init__(self):
        super().__post_init__()
        assert_type_and_range(self.max_power, self.nominal_voltage_in,
                              self.nominal_voltage_out,
                              more_than=0.0,
                              include_more=False)


@dataclass
class Inverter(PureElectricConverter):
    """
    Models an electric inverter, which converts DC to AC.
    """
    def __init__(self, name: str,
                 mass: float,
                 max_power: float,
                 limits: ElectricToElectricLimits,
                 eff_func: PureElectricConsumption,
                 dynamic_response: InverterDynamicResponse,
                 nominal_voltage_in: float,
                 nominal_voltage_out: float):
        state = return_pure_electric_state(signal_type_in=ElectricSignalType.DC,
                                           signal_type_out=ElectricSignalType.AC)
        super().__init__(name=name,
                         mass=mass,
                         input=PortInput(exchange=PowerType.ELECTRIC_DC),
                         output=PortOutput(exchange=PowerType.ELECTRIC_AC),
                         state=state,
                         limits=limits,
                         consumption=eff_func,
                         dynamic_response=dynamic_response,
                         max_power=max_power,
                         nominal_voltage_in=nominal_voltage_in,
                         nominal_voltage_out=nominal_voltage_out)


@dataclass
class Rectifier(PureElectricConverter):
    """
    Models an electric rectifier, which converts AC to DC.
    """
    def __init__(self, name: str,
                 mass: float,
                 max_power: float,
                 limits: ElectricToElectricLimits,
                 eff_func: PureElectricConsumption,
                 dynamic_response: RectifierDynamicResponse,
                 nominal_voltage_in: float,
                 nominal_voltage_out: float):
        state = return_pure_electric_state(signal_type_in=ElectricSignalType.AC,
                                           signal_type_out=ElectricSignalType.DC)
        super().__init__(name=name,
                         mass=mass,
                         input=PortInput(exchange=PowerType.ELECTRIC_AC),
                         output=PortOutput(exchange=PowerType.ELECTRIC_DC),
                         state=state,
                         limits=limits,
                         consumption=eff_func,
                         dynamic_response=dynamic_response,
                         max_power=max_power,
                         nominal_voltage_in=nominal_voltage_in,
                         nominal_voltage_out=nominal_voltage_out)
