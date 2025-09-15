"""This module contains routines for creating components' snapshots,
containing inputs, outputs, and state variables for convenient simulation."""

from dataclasses import dataclass
from components.component_io import ElectricMotorIO, ElectricGeneratorIO, \
    LiquidInternalCombustionEngineIO, GaseousInternalCombustionEngineIO, \
    FuelCellIO, ElectricInverterIO, ElectricRectifierIO, GearBoxIO, \
    ElectricIO, MechanicalIO, LiquidFuelIO, GaseousFuelIO, \
    LiquidFuelTankIO, GaseousFuelTankIO, \
    NonRechargeableBatteryIO, RechargeableBatteryIO
from components.component_state import ElectricMotorState, ElectricGeneratorState, \
    InternalCombustionEngineState, PureMechanicalState, PureElectricState, \
    MotorInternalState, BaseInternalState, RotatingState, \
    BatteryState, LiquidFuelTankState, GaseousFuelTankState, \
    BatteryInternalState, LiquidFuelTankInternalState, GaseousFuelTankInternalState, \
    FuelCellState, FuelCellInternalState, \
    PureElectricInternalState, PureMechanicalInternalState
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
    state: FuelCellState

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
    state: PureElectricState

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
    state: PureElectricState

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
                               rpm=self.state.input_port.rpm)

    @property
    def power_out(self) -> float:
        return torque_to_power(torque=self.io.output_port.torque,
                               rpm=self.state.output_port.rpm)

    @property
    def fuel_consumption_in(self) -> float:
        return 0.0


@dataclass
class NonRechargeableBatterySnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for a non rechargeable battery.
    """
    io: NonRechargeableBatteryIO
    state: BatteryState

    @property
    def power_in(self) -> float:
        return 0.0

    @property
    def power_out(self) -> float:
        return self.io.output_port.electric_power

    @property
    def fuel_consumption_in(self) -> float:
        return 0.0


@dataclass
class RechargeableBatterySnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for a rechargeable battery.
    """
    io: RechargeableBatteryIO
    state: BatteryState

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
class LiquidFuelTankSnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for a liquid fuel tank.
    """
    io: LiquidFuelTankIO
    state: LiquidFuelTankState

    @property
    def power_in(self) -> float:
        return 0.0

    @property
    def power_out(self) -> float:
        return 0.0

    @property
    def fuel_consumption_in(self) -> float:
        return 0.0

    @property
    def fuel_out(self) -> float:
        """
        Returns the fuel being transferred at the output.
        """
        return self.io.output_port.liters_flow


@dataclass
class GaseousFuelTankSnapshot(BaseSnapshot):
    """
    Defines the snapshot contents for a gaseous fuel tank.
    """
    io: GaseousFuelTankIO
    state: GaseousFuelTankState

    @property
    def power_in(self) -> float:
        return 0.0

    @property
    def power_out(self) -> float:
        return 0.0

    @property
    def fuel_consumption_in(self) -> float:
        return 0.0

    @property
    def fuel_out(self) -> float:
        """
        Returns the fuel being transferred at the output.
        """
        return self.io.output_port.mass_flow


def return_electric_motor_snapshot(electric_power_in: float=0.0,
                                   torque_out: float=0.0,
                                   temperature: float=DEFAULT_TEMPERATURE,
                                   on: bool=True,
                                   rpm_out: float=0.0) -> ElectricMotorSnapshot:
    """
    Returns an instance of `ElectricMotorSnapshot`.
    """
    return ElectricMotorSnapshot(io=ElectricMotorIO(input_port=ElectricIO(electric_power=electric_power_in),
                                                    output_port=MechanicalIO(torque=torque_out)),
                                 state=ElectricMotorState(internal=MotorInternalState(temperature=temperature,
                                                                                      on=on),
                                                          output_port=RotatingState(rpm=rpm_out)))

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
                              electric_power_out: float=0.0,
                              temperature: float=DEFAULT_TEMPERATURE) -> FuelCellSnapshot:
    """
    Returns an instance of `FuelCellSnapshot`.
    """
    return FuelCellSnapshot(io=FuelCellIO(input_port=GaseousFuelIO(_fuel=fuel_in,
                                                                   mass_flow=mass_flow_in),
                                          output_port=ElectricIO(electric_power=electric_power_out)),
                            state=FuelCellState(internal=FuelCellInternalState(temperature=temperature)))

def return_electric_inverter_snapshot(electric_power_in: float=0.0,
                                      electric_power_out: float=0.0,
                                      temperature: float=DEFAULT_TEMPERATURE) -> ElectricInverterSnapshot:
    """
    Returns an instance of `ElectricInverterSnapshot`.
    """
    return ElectricInverterSnapshot(io=ElectricInverterIO(input_port=ElectricIO(electric_power=electric_power_in),
                                                          output_port=ElectricIO(electric_power=electric_power_out)),
                                    state=PureElectricState(internal=PureElectricInternalState(temperature=temperature)))

def return_electric_rectifier_snapshot(electric_power_in: float=0.0,
                                       electric_power_out: float=0.0,
                                       temperature: float=DEFAULT_TEMPERATURE) -> ElectricRectifierSnapshot:
    """
    Returns an instance of `ElectricInverterSnapshot`.
    """
    return ElectricRectifierSnapshot(io=ElectricRectifierIO(input_port=ElectricIO(electric_power=electric_power_in),
                                                            output_port=ElectricIO(electric_power=electric_power_out)),
                                    state=PureElectricState(internal=PureElectricInternalState(temperature=temperature)))

def return_gearbox_snapshot(torque_in: float=0.0,
                            torque_out: float=0.0,
                            rpm_in: float=0.0,
                            rpm_out: float=0.0,
                            temperature: float=DEFAULT_TEMPERATURE) -> GearBoxSnapshot:
    """
    Returns an instance of `GearBoxSnapshot`.
    """
    return GearBoxSnapshot(io=GearBoxIO(input_port=MechanicalIO(torque=torque_in),
                                        output_port=MechanicalIO(torque=torque_out)),
                           state=PureMechanicalState(input_port=RotatingState(rpm=rpm_in),
                                                     internal=PureMechanicalInternalState(temperature=temperature),
                                                     output_port=RotatingState(rpm=rpm_out)))

def return_non_rechargeable_battery_snapshot(electric_power_out: float=0.0,
                                             temperature: float=DEFAULT_TEMPERATURE,
                                             electric_energy_stored: float=0.0) -> NonRechargeableBatterySnapshot:
    """
    Returns an instance of `NonRechargeableBatterySnapshot`.
    """
    return NonRechargeableBatterySnapshot(io=NonRechargeableBatteryIO(output_port=ElectricIO(electric_power=electric_power_out)),
                                          state=BatteryState(internal=BatteryInternalState(temperature=temperature,
                                                                                           electric_energy_stored=electric_energy_stored)))

def return_rechargeable_battery_snapshot(electric_power_in: float=0.0,
                                         electric_power_out: float=0.0,
                                         temperature: float=DEFAULT_TEMPERATURE,
                                         electric_energy_stored: float=0.0) -> RechargeableBatterySnapshot:
    """
    Returns an instance of `RechargeableBatterySnapshot`.
    """
    return RechargeableBatterySnapshot(io=RechargeableBatteryIO(input_port=ElectricIO(electric_power=electric_power_in),
                                                                output_port=ElectricIO(electric_power=electric_power_out)),
                                       state=BatteryState(internal=BatteryInternalState(temperature=temperature,
                                                                                        electric_energy_stored=electric_energy_stored)))

def return_liquid_fuel_tank_snapshot(fuel: LiquidFuel,
                                     liters_flow_out: float=0.0,
                                     temperature: float=DEFAULT_TEMPERATURE,
                                     liters_stored: float=0.0) -> LiquidFuelTankSnapshot:
    """
    Returns an instance of `LiquidFuelTankSnapshot`.
    """
    return LiquidFuelTankSnapshot(io=LiquidFuelTankIO(output_port=LiquidFuelIO(_fuel=fuel,
                                                                               liters_flow=liters_flow_out)),
                                  state=LiquidFuelTankState(internal=LiquidFuelTankInternalState(temperature=temperature,
                                                                                                 liters_stored=liters_stored)))

def return_gaseous_fuel_tank_snapshot(fuel: GaseousFuel,
                                      mass_flow_out: float = 0.0,
                                      temperature: float = DEFAULT_TEMPERATURE,
                                      mass_stored: float = 0.0) -> GaseousFuelTankSnapshot:
    """
    Returns an instance of `GaseousFuelTankSnapshot`.
    """
    return GaseousFuelTankSnapshot(io=GaseousFuelTankIO(output_port=GaseousFuelIO(_fuel=fuel,
                                                                                  mass_flow=mass_flow_out)),
                                   state=GaseousFuelTankState(internal=GaseousFuelTankInternalState(temperature=temperature,
                                                                                                    mass_stored=mass_stored)))
