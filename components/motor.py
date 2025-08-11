"""
This module contains definitions for motors and engines.
"""

from dataclasses import dataclass
from components.fuel_type import Fuel
from components.consumption import ElectricMotorConsumption, \
    CombustionEngineConsumption, ElectricGeneratorConsumption
from components.converter import MechanicalConverter, \
    ForwardConverter, ReversibleConverter
from components.dynamic_response import ForwardDynamicResponse, \
    BidirectionalDynamicResponse
from components.limitation import ElectricMotorLimits, LiquidCombustionEngineLimits, \
    GaseousCombustionEngineLimits, ElectricGeneratorLimits
from components.port import PortInput, PortOutput, PortBidirectional
from helpers.types import PowerType, ElectricSignalType


@dataclass
class ElectricMotor(MechanicalConverter, ReversibleConverter):
    """
    Models a reversible electric motor (can act as a generator).
    """
    def __init__(self,
                 name: str,
                 mass: float,
                 limits: ElectricMotorLimits,
                 consumption: ElectricMotorConsumption,
                 dynamic_response: BidirectionalDynamicResponse,
                 electric_type: ElectricSignalType,
                 inertia: float):
        super().__init__(inertia=inertia)
        assert isinstance(electric_type, ElectricSignalType)
        ReversibleConverter.__init__(self=self,
                                     name=name,
                                     mass=mass,
                                     input_port=PortBidirectional(exchange=PowerType.ELECTRIC_AC
                                                                  if electric_type==ElectricSignalType.AC
                                                                  else PowerType.ELECTRIC_DC),
                                     output_port=PortBidirectional(exchange=PowerType.MECHANICAL),
                                     limits=limits,
                                     consumption=consumption,
                                     dynamic_response=dynamic_response)

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
                 dynamic_response: ForwardDynamicResponse,
                 inertia: float,
                 fuel: Fuel):
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
                 dynamic_response: ForwardDynamicResponse,
                 inertia: float,
                 fuel: Fuel):
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
                 dynamic_response: ForwardDynamicResponse,
                 electric_type: ElectricSignalType,
                 inertia: float):
        super().__init__(inertia=inertia)
        assert isinstance(electric_type, ElectricSignalType)
        ForwardConverter.__init__(self=self,
                                  name=name,
                                  mass=mass,
                                  input_port=PortInput(exchange=PowerType.MECHANICAL),
                                  output_port=PortOutput(exchange=PowerType.ELECTRIC_AC
                                                         if electric_type==ElectricSignalType.AC
                                                         else PowerType.ELECTRIC_DC),
                                  limits=limits,
                                  consumption=consumption,
                                  dynamic_response=dynamic_response)

    @property
    def electric_type(self) -> ElectricSignalType:
        """
        Returns the type of output electric signal.
        """
        return (ElectricSignalType.AC
                if self.output.exchange == PowerType.ELECTRIC_AC
                else ElectricSignalType.DC)
