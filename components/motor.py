"""
This module contains definitions for motors and engines.
"""

from dataclasses import dataclass
from components.fuel_type import LiquidFuel, GaseousFuel
from components.component_io import return_electric_motor_io, ElectricMotorIO, \
    return_liquid_ice_io, LiquidInternalCombustionEngineIO, \
    return_gaseous_ice_io, GaseousInternalCombustionEngineIO, \
    return_electric_generator_io, ElectricGeneratorIO
from components.component_state import return_internal_combustion_engine_state, \
    return_electric_motor_state, return_electric_generator_state, \
    ElectricMotorState, InternalCombustionEngineState, ElectricGeneratorState
from components.consumption import ElectricMotorConsumption, \
    LiquidCombustionEngineConsumption, GaseousCombustionEngineConsumption, \
    ElectricGeneratorConsumption
from components.converter import MechanicalConverter
from components.dynamic_response import ElectricMotorDynamicResponse, \
    ElectricGeneratorDynamicResponse, \
    LiquidCombustionDynamicResponse, GaseousCombustionDynamicResponse
from components.limitation import ElectricMotorLimits, LiquidCombustionEngineLimits, \
    GaseousCombustionEngineLimits, ElectricGeneratorLimits
from components.port import PortInput, PortOutput, PortBidirectional, PortType
# from components.state import ElectricMotorState, LiquidCombustionEngineState, \
#     GaseousCombustionEngineState, ElectricGeneratorState, \
#     return_electric_motor_state, return_electric_generator_state, \
#     return_liquid_combustion_engine_state, return_gaseous_combustion_engine_state
from helpers.functions import assert_type, assert_type_and_range
from helpers.types import PowerType, ElectricSignalType


@dataclass
class ElectricMotor(MechanicalConverter):
    """
    Models a reversible electric motor (can act as a generator).
    """
    nominal_voltage: float
    state: ElectricMotorState  # type: ignore
    io_values: ElectricMotorIO  # type: ignore
    limits: ElectricMotorLimits  # type: ignore
    consumption: ElectricMotorConsumption  # type: ignore
    dynamic_response: ElectricMotorDynamicResponse  # type: ignore

    def __init__(self,
                 name: str,
                 mass: float,
                 nominal_voltage: float,
                 limits: ElectricMotorLimits,
                 consumption: ElectricMotorConsumption,
                 dynamic_response: ElectricMotorDynamicResponse,
                 electric_type: ElectricSignalType,
                 inertia: float):
        assert_type_and_range(nominal_voltage, inertia,
                              more_than=0.0,
                              include_more=False)
        assert_type(limits,
                    expected_type=ElectricMotorLimits)
        assert_type(consumption,
                    expected_type=ElectricMotorConsumption)
        assert_type(dynamic_response,
                    expected_type=ElectricMotorDynamicResponse)
        assert_type(electric_type,
                    expected_type=ElectricSignalType)
        state = return_electric_motor_state()
        io_values = return_electric_motor_io()
        super().__init__(name=name,
                         mass=mass,
                         input=PortBidirectional(exchange=PowerType.ELECTRIC_AC
                                                      if electric_type==ElectricSignalType.AC
                                                      else PowerType.ELECTRIC_DC),
                         output=PortBidirectional(exchange=PowerType.MECHANICAL),
                         io_values=io_values,
                         state=state,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         inertia=inertia)
        self.nominal_voltage = nominal_voltage

    @property
    def electric_type(self) -> ElectricSignalType:
        """
        Returns the type of input electric signal.
        """
        return (ElectricSignalType.AC
                if self.input.exchange == PowerType.ELECTRIC_AC
                else ElectricSignalType.DC)

    def add_delivery(self, amount: float,
                     which_port: PortType) -> float:
        """
        Sets the output according to a resource request.
        """
        if which_port==PortType.INPUT_PORT:
            self.io_values.input_port.electric_power += amount
            return self.io_values.input_port.electric_power
        self.io_values.output_port.torque += amount
        return self.io_values.output_port.torque


@dataclass
class LiquidInternalCombustionEngine(MechanicalConverter):
    """
    Models an internal combustion engine
    (irreversible) that runs on a liquid fuel.
    """
    state: InternalCombustionEngineState  # type: ignore
    io_values: LiquidInternalCombustionEngineIO  # type: ignore
    limits: LiquidCombustionEngineLimits  # type: ignore
    consumption: LiquidCombustionEngineConsumption  # type: ignore
    dynamic_response: LiquidCombustionDynamicResponse  # type: ignore

    def __init__(self,
                 name: str,
                 mass: float,
                 limits: LiquidCombustionEngineLimits,
                 consumption: LiquidCombustionEngineConsumption,
                 dynamic_response: LiquidCombustionDynamicResponse,
                 inertia: float,
                 fuel: LiquidFuel):
        assert_type(limits,
                    expected_type=LiquidCombustionEngineLimits)
        assert_type(consumption,
                    expected_type=LiquidCombustionEngineConsumption)
        assert_type(dynamic_response,
                    expected_type=LiquidCombustionDynamicResponse)
        assert_type_and_range(inertia,
                              more_than=0.0,
                              include_more=False)
        assert_type(fuel,
                    expected_type=LiquidFuel)
        state = return_internal_combustion_engine_state()
        io_values = return_liquid_ice_io(fuel=fuel)
        super().__init__(name=name,
                         mass=mass,
                         input=PortInput(exchange=fuel),
                         output=PortOutput(exchange=PowerType.MECHANICAL),
                         state=state,
                         io_values=io_values,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         inertia=inertia)


@dataclass
class GaseousInternalCombustionEngine(MechanicalConverter):
    """
    Models an internal combustion engine
    (irreversible) that runs on a gaseous fuel.
    """
    state: InternalCombustionEngineState  # type: ignore
    io_values: GaseousInternalCombustionEngineIO  # type: ignore
    limits: GaseousCombustionEngineLimits  # type: ignore
    consumption: GaseousCombustionEngineConsumption  # type: ignore
    dynamic_response: GaseousCombustionDynamicResponse  # type: ignore

    def __init__(self,
                 name: str,
                 mass: float,
                 limits: GaseousCombustionEngineLimits,
                 consumption: GaseousCombustionEngineConsumption,
                 dynamic_response: GaseousCombustionDynamicResponse,
                 inertia: float,
                 fuel: GaseousFuel):
        assert_type(limits,
                    expected_type=GaseousCombustionEngineLimits)
        assert_type(consumption,
                    expected_type=GaseousCombustionEngineConsumption)
        assert_type(dynamic_response,
                    expected_type=GaseousCombustionDynamicResponse)
        assert_type_and_range(inertia,
                              more_than=0.0,
                              include_more=False)
        assert_type(fuel,
                    expected_type=GaseousFuel)
        state = return_internal_combustion_engine_state()
        io_values = return_gaseous_ice_io(fuel=fuel)
        super().__init__(name=name,
                         mass=mass,
                         input=PortInput(exchange=fuel),
                         output=PortOutput(exchange=PowerType.MECHANICAL),
                         state=state,
                         io_values=io_values,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         inertia=inertia)


@dataclass
class ElectricGenerator(MechanicalConverter):
    """
    Models an irreversible electric generator.
    """
    nominal_voltage: float
    state: ElectricGeneratorState  # type: ignore
    io_values: ElectricGeneratorIO  # type: ignore
    limits: ElectricGeneratorLimits  # type: ignore
    consumption: ElectricGeneratorConsumption  # type: ignore
    dynamic_response: ElectricGeneratorDynamicResponse  # type: ignore

    def __init__(self,
                 name: str,
                 mass: float,
                 nominal_voltage: float,
                 limits: ElectricGeneratorLimits,
                 consumption: ElectricGeneratorConsumption,
                 dynamic_response: ElectricGeneratorDynamicResponse,
                 inertia: float):
        assert_type_and_range(nominal_voltage, inertia,
                              more_than=0.0,
                              include_more=False)
        assert_type(limits,
                    expected_type=ElectricGeneratorLimits)
        assert_type(consumption,
                    expected_type=ElectricGeneratorConsumption)
        assert_type(dynamic_response,
                    expected_type=ElectricGeneratorDynamicResponse)
        state = return_electric_generator_state()
        io_values = return_electric_generator_io()
        super().__init__(name=name,
                         mass=mass,
                         input=PortInput(exchange=PowerType.MECHANICAL),
                         output=PortOutput(exchange=PowerType.ELECTRIC_AC),
                         state=state,
                         io_values=io_values,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         inertia=inertia)

    @property
    def electric_type(self) -> ElectricSignalType:
        """
        Returns the type of output electric signal.
        """
        return ElectricSignalType.AC
