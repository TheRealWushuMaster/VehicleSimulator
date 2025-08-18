"""
This module contains definitions for motors and engines.
"""

from dataclasses import dataclass
from components.fuel_type import LiquidFuel, GaseousFuel
from components.consumption import ElectricMotorConsumption, \
    CombustionEngineConsumption, ElectricGeneratorConsumption
from components.converter import MechanicalConverter
from components.dynamic_response import ElectricMotorDynamicResponse, \
    ElectricGeneratorDynamicResponse, \
    LiquidCombustionDynamicResponse, GaseousCombustionDynamicResponse
from components.limitation import ElectricMotorLimits, LiquidCombustionEngineLimits, \
    GaseousCombustionEngineLimits, ElectricGeneratorLimits
from components.port import PortInput, PortOutput, PortBidirectional
from helpers.functions import assert_type
from helpers.types import PowerType, ElectricSignalType


@dataclass
class ElectricMotor(MechanicalConverter):
    """
    Models a reversible electric motor (can act as a generator).
    """
    def __init__(self,
                 name: str,
                 mass: float,
                 limits: ElectricMotorLimits,
                 consumption: ElectricMotorConsumption,
                 dynamic_response: ElectricMotorDynamicResponse,
                 electric_type: ElectricSignalType,
                 inertia: float):
        assert_type(electric_type,
                    expected_type=ElectricSignalType)
        
        super().__init__(name=name,
                         mass=mass,
                         input_port=PortBidirectional(exchange=PowerType.ELECTRIC_AC
                                                      if electric_type==ElectricSignalType.AC
                                                      else PowerType.ELECTRIC_DC),
                         output_port=PortBidirectional(exchange=PowerType.MECHANICAL),
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         inertia=inertia)

    @property
    def electric_type(self) -> ElectricSignalType:
        """
        Returns the type of input electric signal.
        """
        return (ElectricSignalType.AC
                if self.input.exchange == PowerType.ELECTRIC_AC
                else ElectricSignalType.DC)


@dataclass
class LiquidInternalCombustionEngine(MechanicalConverter, ForwardConverter):
    """
    Models an internal combustion engine
    (irreversible) that runs on a liquid fuel.
    """
    def __init__(self,
                 name: str,
                 mass: float,
                 limits: LiquidCombustionEngineLimits,
                 consumption: CombustionEngineConsumption,
                 dynamic_response: LiquidCombustionDynamicResponse,
                 inertia: float,
                 fuel: LiquidFuel):
        super().__init__(inertia=inertia)
        ForwardConverter.__init__(self=self,
                                  name=name,
                                  mass=mass,
                                  input_port=PortInput(exchange=fuel),
                                  output_port=PortOutput(exchange=PowerType.MECHANICAL),
                                  limits=limits,
                                  consumption=consumption,
                                  dynamic_response=dynamic_response)


@dataclass
class GaseousInternalCombustionEngine(MechanicalConverter, ForwardConverter):
    """
    Models an internal combustion engine
    (irreversible) that runs on a gaseous fuel.
    """
    def __init__(self,
                 name: str,
                 mass: float,
                 limits: GaseousCombustionEngineLimits,
                 consumption: CombustionEngineConsumption,
                 dynamic_response: GaseousCombustionDynamicResponse,
                 inertia: float,
                 fuel: GaseousFuel):
        super().__init__(inertia=inertia)
        ForwardConverter.__init__(self=self,
                                  name=name,
                                  mass=mass,
                                  input_port=PortInput(exchange=fuel),
                                  output_port=PortOutput(exchange=PowerType.MECHANICAL),
                                  limits=limits,
                                  consumption=consumption,
                                  dynamic_response=dynamic_response)


@dataclass
class ElectricGenerator(MechanicalConverter, ForwardConverter):
    """
    Models an irreversible electric generator.
    """
    def __init__(self,
                 name: str,
                 mass: float,
                 limits: ElectricGeneratorLimits,
                 consumption: ElectricGeneratorConsumption,
                 dynamic_response: ElectricGeneratorDynamicResponse,
                 inertia: float):
        super().__init__(inertia=inertia)
        ForwardConverter.__init__(self=self,
                                  name=name,
                                  mass=mass,
                                  input_port=PortInput(exchange=PowerType.MECHANICAL),
                                  output_port=PortOutput(exchange=PowerType.ELECTRIC_AC),
                                  limits=limits,
                                  consumption=consumption,
                                  dynamic_response=dynamic_response)

    @property
    def electric_type(self) -> ElectricSignalType:
        """
        Returns the type of output electric signal.
        """
        return ElectricSignalType.AC
