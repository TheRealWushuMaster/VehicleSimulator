"""This module contains routines for creating components' snapshots,
containing inputs, outputs, and state variables for convenient simulation."""

from dataclasses import dataclass
from components.component_io import ElectricMotorIO, ElectricGeneratorIO, \
    LiquidInternalCombustionEngineIO, GaseousInternalCombustionEngineIO, \
    FuelCellIO, ElectricInverterIO, ElectricRectifierIO, GearBoxIO, \
    ElectricIO, MechanicalIO, LiquidFuelIO, GaseousFuelIO
from components.component_state import ElectricMotorState, ElectricGeneratorState, \
    InternalCombustionEngineState, PureMechanicalState, \
    MotorInternalState, BaseInternalState, RotatingState
from components.fuel_type import LiquidFuel, GaseousFuel
from helpers.functions import torque_to_power
from simulation.constants import DEFAULT_TEMPERATURE


@dataclass
class BaseSnapshot():
    """
    Base class for snapshot classes.
    """
    @property
    def power_in(self) -> float:
        """
        Calculates the power transferred through the input.
        """
        raise NotImplementedError

    @property
    def power_out(self) -> float:
        """
        Calculates the power transferred through the output.
        """
        raise NotImplementedError

    @property
    def forward_efficiency(self) -> float:
        """
        Calculates the power efficiency for a forward transfer.
        """
        return self.power_out / self.power_in if self.power_in > 0.0 else 0.0

    @property
    def reverse_efficiency(self) -> float:
        """
        Calculates the power efficiency for a reverse transfer.
        """
        return 1 / self.forward_efficiency if self.forward_efficiency > 0.0 else 0.0

    @property
    def fuel_consumption_in(self) -> float:
        """
        Calculates the fuel consumption at the input.
        """
        raise NotImplementedError


@dataclass
class ElectricMotorSnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for an electric motor.
    """
    io: ElectricMotorIO
    state: ElectricMotorState

    @property
    def power_in(self) -> float:
        return self.io.input_port.electric_power

    @property
    def power_out(self) -> float:
        return torque_to_power(torque=self.io.output_port.torque,
                               rpm=self.state.output_port.rpm)

    @property
    def fuel_consumption_in(self) -> float:
        return 0.0


@dataclass
class LiquidCombustionEngineSnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for a liquid fuel internal combustion engine.
    """
    io: LiquidInternalCombustionEngineIO
    state: InternalCombustionEngineState

    @property
    def power_in(self) -> float:
        return 0.0

    @property
    def power_out(self) -> float:
        return torque_to_power(torque=self.io.output_port.torque,
                               rpm=self.state.output_port.rpm)

    @property
    def fuel_consumption_in(self) -> float:
        return self.io.input_port.liters_flow


@dataclass
class GaseousCombustionEngineSnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for a gaseous fuel internal combustion engine.
    """
    io: GaseousInternalCombustionEngineIO
    state: InternalCombustionEngineState

    @property
    def power_in(self) -> float:
        return 0.0

    @property
    def power_out(self) -> float:
        return torque_to_power(torque=self.io.output_port.torque,
                               rpm=self.state.output_port.rpm)

    @property
    def fuel_consumption_in(self) -> float:
        return self.io.input_port.mass_flow


@dataclass
class ElectricGeneratorSnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for an electric generator.
    """
    io: ElectricGeneratorIO
    state: ElectricGeneratorState

    @property
    def power_in(self) -> float:
        return torque_to_power(torque=self.io.input_port.torque,
                               rpm=self.state.input_port.rpm)

    @property
    def power_out(self) -> float:
        return self.io.output_port.electric_power

    @property
    def fuel_consumption_in(self) -> float:
        return 0.0


@dataclass
class FuelCellSnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for a fuel cell.
    """
    io: FuelCellIO
    internal: BaseInternalState

    @property
    def power_in(self) -> float:
        return 0.0

    @property
    def power_out(self) -> float:
        return self.io.output_port.electric_power

    @property
    def fuel_consumption_in(self) -> float:
        return self.io.input_port.mass_flow


@dataclass
class ElectricInverterSnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for an electric inverter.
    """
    io: ElectricInverterIO
    internal: BaseInternalState

    @property
    def power_in(self) -> float:
        return self.io.input_port.electric_power

    @property
    def power_out(self) -> float:
        return self.io.output_port.electric_power

    @property
    def fuel_consumption_in(self) -> float:
        return 0.0


@dataclass
class ElectricRectifierSnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for an electric rectifier.
    """
    io: ElectricRectifierIO
    internal: BaseInternalState

    @property
    def power_in(self) -> float:
        return self.io.input_port.electric_power

    @property
    def power_out(self) -> float:
        return self.io.output_port.electric_power

    @property
    def fuel_consumption_in(self) -> float:
        return 0.0


@dataclass
class GearBoxSnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for a gearbox.
    """
    io: GearBoxIO
    state: PureMechanicalState

    @property
    def power_in(self) -> float:
        return torque_to_power(torque=self.io.input_port.torque,
                               rpm=self.state.output_port.rpm)

    @property
    def power_out(self) -> float:
        return torque_to_power(torque=self.io.output_port.torque,
                               rpm=self.state.output_port.rpm)

    @property
    def fuel_consumption_in(self) -> float:
        return 0.0


def return_electric_motor_snapshot(electric_power_in: float=0.0,
                                   torque_out: float=0.0,
                                   temperature: float=DEFAULT_TEMPERATURE,
                                   on: bool=True,
                                   rpm: float=0.0) -> ElectricMotorSnapshot:
    """
    Returns an instance of `ElectricMotorSnapshot`.
    """
    return ElectricMotorSnapshot(io=ElectricMotorIO(input_port=ElectricIO(electric_power=electric_power_in),
                                                    output_port=MechanicalIO(torque=torque_out)),
                                 state=ElectricMotorState(internal=MotorInternalState(temperature=temperature,
                                                                                      on=on),
                                                          output_port=RotatingState(rpm=rpm)))

def return_liquid_ice_snapshot(fuel_in: LiquidFuel,
                               liters_flow_in: float=0.0,
                               torque_out: float=0.0,
                               temperature: float=DEFAULT_TEMPERATURE,
                               on: bool=True,
                               rpm_out: float=0.0) -> LiquidCombustionEngineSnapshot:
    """
    Returns an instance of `LiquidCombustionEngineSnapshot`.
    """
    return LiquidCombustionEngineSnapshot(io=LiquidInternalCombustionEngineIO(input_port=LiquidFuelIO(_fuel=fuel_in,
                                                                                                      liters_flow=liters_flow_in),
                                                                              output_port=MechanicalIO(torque=torque_out)),
                                          state=InternalCombustionEngineState(internal=MotorInternalState(temperature=temperature,
                                                                                                          on=on),
                                                                              output_port=RotatingState(rpm=rpm_out)))

def return_gaseous_ice_snapshot(fuel_in: GaseousFuel,
                                mass_flow_in: float=0.0,
                                torque_out: float=0.0,
                                temperature: float=DEFAULT_TEMPERATURE,
                                on: bool=True,
                                rpm_out: float=0.0) -> GaseousCombustionEngineSnapshot:
    """
    Returns an instance of `LiquidCombustionEngineSnapshot`.
    """
    return GaseousCombustionEngineSnapshot(io=GaseousInternalCombustionEngineIO(input_port=GaseousFuelIO(_fuel=fuel_in,
                                                                                                         mass_flow=mass_flow_in),
                                                                                output_port=MechanicalIO(torque=torque_out)),
                                           state=InternalCombustionEngineState(internal=MotorInternalState(temperature=temperature,
                                                                                                           on=on),
                                                                               output_port=RotatingState(rpm=rpm_out)))

def return_electric_generator_snapshot(torque_in: float=0.0,
                                       electric_power_out: float=0.0,
                                       rpm_in: float=0.0,
                                       temperature: float=DEFAULT_TEMPERATURE) -> ElectricGeneratorSnapshot:
    """
    Returns an instance of `ElectricGeneratorSnapshot`.
    """
    return ElectricGeneratorSnapshot(io=ElectricGeneratorIO(input_port=MechanicalIO(torque=torque_in),
                                                            output_port=ElectricIO(electric_power=electric_power_out)),
                                     state=ElectricGeneratorState(input_port=RotatingState(rpm=rpm_in),
                                                                  internal=BaseInternalState(temperature=temperature)))

def return_fuel_cell_snapshot(fuel_in: GaseousFuel,
                              mass_flow_in: float=0.0,
                              electric_power_out: float=0.0) -> FuelCellSnapshot:
    """
    Returns an instance of `FuelCellSnapshot`.
    """
    return FuelCellSnapshot(io=FuelCellIO(input_port=GaseousFuelIO(_fuel=fuel_in,
                                                                   mass_flow=mass_flow_in),
                                          output_port=ElectricIO(electric_power=electric_power_out)))

def return_electric_inverter_snapshot(electric_power_in: float=0.0,
                                      electric_power_out: float=0.0) -> ElectricInverterSnapshot:
    """
    Returns an instance of `ElectricInverterSnapshot`.
    """
    return ElectricInverterSnapshot(io=ElectricInverterIO(input_port=ElectricIO(electric_power=electric_power_in),
                                                          output_port=ElectricIO(electric_power=electric_power_out)))

def return_electric_rectifier_snapshot(electric_power_in: float=0.0,
                                       electric_power_out: float=0.0) -> ElectricRectifierSnapshot:
    """
    Returns an instance of `ElectricInverterSnapshot`.
    """
    return ElectricRectifierSnapshot(io=ElectricRectifierIO(input_port=ElectricIO(electric_power=electric_power_in),
                                                            output_port=ElectricIO(electric_power=electric_power_out)))
