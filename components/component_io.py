"""This module contains definitions for inputs and outputs of components."""

from dataclasses import dataclass
from components.component_state import RotatingState
from components.fuel_type import LiquidFuel, GaseousFuel
from helpers.functions import torque_to_power

# ========
# BASE IOs
# ========


@dataclass
class BaseEnergyIO():
    """
    Base class for energy IO.
    """
    def power(self, state) -> float:
        """
        Returns the power being transferred.
        """
        raise NotImplementedError


@dataclass
class ElectricIO(BaseEnergyIO):
    """
    Describes an electric input or output.
    """
    electric_power: float=0.0

    def power(self, state) -> float:
        """
        Returns the power being transferred.
        """
        return self.electric_power


@dataclass
class MechanicalIO():
    """
    Describes a mechanical input or output.
    """
    torque: float=0.0

    def power(self, state: RotatingState) -> float:
        """
        Returns the power being transferred.
        """
        return torque_to_power(torque=self.torque,
                               rpm=state.rpm)


@dataclass
class LiquidFuelIO():
    """
    Describes a liquid fuel input or output.
    """
    _fuel: LiquidFuel
    liters_flow: float=0.0


@dataclass
class GaseousFuelIO():
    """
    Describes a gaseous fuel input or output.
    """
    _fuel: GaseousFuel
    mass_flow: float=0.0


# ===============
# CONVERTERS' IOs
# ===============


@dataclass
class ConverterIO():
    """
    Base class for converters' inputs and outputs.
    """


@dataclass
class ElectricMotorIO(ConverterIO):
    """
    Describes an electric motor's input and output.
    """
    input_port: ElectricIO
    output_port: MechanicalIO


@dataclass
class LiquidInternalCombustionEngineIO(ConverterIO):
    """
    Describes a liquid fuel internal
    combustion engine's input and output.
    """
    input_port: LiquidFuelIO
    output_port: MechanicalIO


@dataclass
class GaseousInternalCombustionEngineIO(ConverterIO):
    """
    Describes a gaseous fuel internal
    combustion engine's input and output.
    """
    input_port: GaseousFuelIO
    output_port: MechanicalIO


@dataclass
class ElectricGeneratorIO(ConverterIO):
    """
    Describes an electric generator's input and output.
    """
    input_port: MechanicalIO
    output_port: ElectricIO


@dataclass
class FuelCellIO(ConverterIO):
    """
    Describes a fuel cell's input and output.
    """
    input_port: GaseousFuelIO
    output_port: ElectricIO


@dataclass
class PureElectricIO(ConverterIO):
    """
    Describes the input and output
    of a purely electric component.
    """
    input_port: ElectricIO
    output_port: ElectricIO


@dataclass
class PureMechanicalIO(ConverterIO):
    """
    Describes the input and output
    of a purely mechanical component.
    """
    input_port: MechanicalIO
    output_port: MechanicalIO


@dataclass
class ElectricInverterIO(PureElectricIO):
    """
    Describes an electric inverter's input and output.
    """


@dataclass
class ElectricRectifierIO(PureElectricIO):
    """
    Describes an electric rectifier's input and output.
    """


@dataclass
class GearBoxIO(PureMechanicalIO):
    """
    Describes a gearbox's input and output.
    """


# ===================
# ENERGY SOURCES' IOs
# ===================


@dataclass
class EnergySourceIO():
    """
    Base class for an energy source's input and output.
    """


@dataclass
class BatteryIO(EnergySourceIO):
    """
    Base class for a battery's input and output.
    """


@dataclass
class FuelTankIO(EnergySourceIO):
    """
    Base class for a fuel tank's output.
    """


@dataclass
class NonRechargeableBatteryIO(BatteryIO):
    """
    Describes a non rechargeable battery's output.
    """
    output_port: ElectricIO


@dataclass
class RechargeableBatteryIO(NonRechargeableBatteryIO):
    """
    Describes a rechargeable battery's input and output.
    """
    input_port: ElectricIO


@dataclass
class LiquidFuelTankIO(FuelTankIO):
    """
    Describes a liquid fuel tank's output.
    """
    output_port: LiquidFuelIO


@dataclass
class GaseousFuelTankIO(FuelTankIO):
    """
    Describes a gaseous fuel tank's output.
    """
    output_port: GaseousFuelIO


def return_electric_motor_io(electric_power: float=0.0,
                             torque: float=0.0) -> ElectricMotorIO:
    """
    Returns an instance of `ElectricMotorIO`.
    """
    return ElectricMotorIO(input_port=ElectricIO(electric_power=electric_power),
                           output_port=MechanicalIO(torque=torque))

def return_liquid_ice_io(fuel: LiquidFuel,
                         liters_flow: float=0.0,
                         torque: float=0.0) -> LiquidInternalCombustionEngineIO:
    """
    Returns an instance of `LiquidInternalCombustionEngineIO`.
    """
    return LiquidInternalCombustionEngineIO(input_port=LiquidFuelIO(_fuel=fuel,
                                                                    liters_flow=liters_flow),
                                            output_port=MechanicalIO(torque=torque))
