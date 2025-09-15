"""This module contains several dynamic response curves for different components."""

from typing import Callable
from components.consumption import ElectricMotorConsumption, ElectricGeneratorConsumption, \
    LiquidCombustionEngineConsumption, GaseousCombustionEngineConsumption, \
    FuelCellConsumption
from components.limitation import ElectricGeneratorLimits, \
    ElectricMotorLimits, LiquidCombustionEngineLimits, GaseousCombustionEngineLimits, \
        FuelCellLimits
from components.component_io import GearBoxIO, MechanicalIO, ElectricRectifierIO, \
    ElectricIO, ElectricInverterIO, ElectricMotorIO
from components.component_snapshot import GearBoxSnapshot, \
    ElectricInverterSnapshot, ElectricRectifierSnapshot, \
    ElectricMotorSnapshot, ElectricGeneratorSnapshot, \
    LiquidCombustionEngineSnapshot, GaseousCombustionEngineSnapshot
from components.component_state import PureMechanicalState, \
    PureElectricState, \
    ElectricMotorState, ElectricGeneratorState, \
    InternalCombustionEngineState, \
    RotatingState
# from components.state import ElectricIOState, RotatingIOState, \
#     PureMechanicalState, ElectricMotorState, ElectricGeneratorState, \
#     LiquidCombustionEngineState, GaseousCombustionEngineState, \
#     LiquidFuelIOState, GaseousFuelIOState, \
#     PureElectricState, FuelCellState
from helpers.functions import assert_type, assert_type_and_range, \
    ang_vel_to_rpm
from helpers.types import ElectricSignalType


class MechanicalToMechanical():
    """
    Contains generator methods for purely mechanical components.
    """
    @staticmethod
    def forward_gearbox(gear_ratio: float, efficiency: float
                        ) -> Callable[[GearBoxSnapshot],
                                      tuple[GearBoxSnapshot,
                                            PureMechanicalState]]:
        """
        Generates a forward response for a stateless pure
        mechanical component.
        Receives an input `torque` and `rpm` and outputs `rpm`
        affected by `gear_ratio`, `torque`, and `efficiency`.
        """
        assert_type_and_range(gear_ratio,
                              more_than=0.0)
        assert_type_and_range(efficiency,
                              more_than=0.0,
                              less_than=1.0,
                              include_more=False)
        def response(snap: GearBoxSnapshot) -> tuple[GearBoxSnapshot,
                                                     PureMechanicalState]:
            assert isinstance(snap, GearBoxSnapshot)
            torque_out = snap.io.output_port.torque * gear_ratio * efficiency
            rpm_out = snap.state.output_port.rpm / gear_ratio
            new_snap = GearBoxSnapshot(io=GearBoxIO(input_port=snap.io.input_port,
                                                    output_port=MechanicalIO(torque=torque_out)),
                                       state=snap.state)
            new_state = PureMechanicalState(input_port=snap.state.input_port,
                                            internal=snap.state.internal,
                                            output_port=RotatingState(rpm=rpm_out))
            return new_snap, new_state
        return response

    @staticmethod
    def reverse_gearbox(gear_ratio: float, efficiency: float
                        ) -> Callable[[GearBoxSnapshot],
                                      tuple[GearBoxSnapshot,
                                            PureMechanicalState]]:
        """
        Generates a reverse response for a stateless pure
        mechanical component.
        Receives an input `torque` and `rpm` and outputs `rpm`
        affected by `gear_ratio`, `torque`, and `efficiency`.
        """
        assert_type_and_range(gear_ratio,
                              more_than=0.0)
        assert_type_and_range(efficiency,
                              more_than=0.0,
                              less_than=1.0,
                              include_more=False)
        def response(snap: GearBoxSnapshot) -> tuple[GearBoxSnapshot,
                                                     PureMechanicalState]:
            assert isinstance(snap, GearBoxSnapshot)
            torque_in = snap.io.output_port.torque / gear_ratio * efficiency
            rpm_in = snap.state.output_port.rpm * gear_ratio
            new_snap = GearBoxSnapshot(io=GearBoxIO(input_port=MechanicalIO(torque=torque_in),
                                                    output_port=snap.io.output_port),
                                       state=snap.state)
            new_state = PureMechanicalState(input_port=RotatingState(rpm=rpm_in),
                                            internal=snap.state.internal,
                                            output_port=snap.state.output_port)
            return new_snap, new_state
        return response


class ElectricToElectric():
    """
    Contains responses for electric to electric components.
    """
    @staticmethod
    def rectifier_response(voltage_gain: float,
                           efficiency: float
                           ) -> Callable[[ElectricRectifierSnapshot],
                                         tuple[ElectricRectifierSnapshot,
                                               PureElectricState]]:
        """
        Returns a response for an electric
        rectifier with constant efficiency.
        """
        def response(snap: ElectricRectifierSnapshot
                     ) -> tuple[ElectricRectifierSnapshot,
                                PureElectricState]:
            assert_type(snap,
                        expected_type=ElectricRectifierSnapshot)
            electric_power_out = snap.io.input_port.electric_power * efficiency
            new_snap = ElectricRectifierSnapshot(io=ElectricRectifierIO(input_port=snap.io.input_port,
                                                                        output_port=ElectricIO(electric_power=electric_power_out)),
                                                                        internal=snap.internal)
            new_state = PureElectricState(internal=snap.internal)
            return new_snap, new_state
        return response

    @staticmethod
    def inverter_response(voltage_gain: float,
                          efficiency: float
                          ) -> Callable[[ElectricInverterSnapshot],
                                        tuple[ElectricInverterSnapshot,
                                              PureElectricState]]:
        """
        Returns a response for an electric
        inverter with constant efficiency.
        """
        def response(snap: ElectricInverterSnapshot
                     ) -> tuple[ElectricInverterSnapshot,
                                PureElectricState]:
            assert_type(snap,
                        expected_type=ElectricInverterSnapshot)
            electric_power_out = snap.io.input_port.electric_power * efficiency
            new_snap = ElectricInverterSnapshot(io=ElectricInverterIO(input_port=snap.io.input_port,
                                                                      output_port=ElectricIO(electric_power=electric_power_out)),
                                                internal=snap.internal)
            new_state = PureElectricState(internal=snap.internal)
            return new_snap, new_state
        return response


class ElectricToMechanical():
    """
    Contains generator methods for electric motors.
    """
    @staticmethod
    def forward_driven_first_order() -> Callable[[ElectricMotorSnapshot, float,
                                                  float, float, float,
                                                  ElectricMotorConsumption,
                                                  ElectricMotorLimits],
                                                 tuple[ElectricMotorSnapshot,
                                                       ElectricMotorState]]:
        """
        Returns a response for an electric generator
        with a first-order lag response.
        """
        def response(snap: ElectricMotorSnapshot,
                     load_torque: float,
                     downstream_inertia: float,
                     delta_t: float,
                     control_signal: float,
                     efficiency: ElectricMotorConsumption,
                     limits: ElectricMotorLimits) -> tuple[ElectricMotorSnapshot,
                                                           ElectricMotorState]:
            assert_type(snap,
                        expected_type=ElectricMotorSnapshot)
            assert_type(efficiency,
                        expected_type=ElectricMotorConsumption)
            assert_type(limits,
                        expected_type=ElectricMotorLimits)
            assert_type_and_range(load_torque, downstream_inertia,
                                  delta_t,
                                  more_than=0.0)
            assert_type_and_range(control_signal,
                                  more_than=0.0,
                                  less_than=1.0)
            min_torque = limits.relative_limits.output.torque.min(snap)
            max_torque = limits.relative_limits.output.torque.max(snap)
            torque = (max_torque - min_torque) * control_signal + min_torque
            w_dot = (torque - load_torque) / downstream_inertia
            efficiency_value = efficiency.in_to_out_efficiency_value(snapshot=snap)
            new_snap = ElectricMotorSnapshot(io=ElectricMotorIO(input_port=ElectricIO(electric_power=0.0),
                                                                output_port=MechanicalIO(torque=torque)),
                                             state=snap.state)
            new_snap.io.input_port.electric_power = new_snap.power_out / efficiency_value
            new_rpm = snap.state.output_port.rpm + ang_vel_to_rpm(ang_vel=w_dot*delta_t)
            new_state = ElectricMotorState(internal=snap.state.internal,
                                           output_port=RotatingState(rpm=new_rpm))
            return new_snap, new_state
        return response


class MechanicalToElectric():
    """
    Contains generator methods for electric generators or reversed motors.
    """
    @staticmethod
    def forward_generator() -> Callable[[ElectricGeneratorState,
                                         ElectricGeneratorConsumption,
                                         ElectricGeneratorLimits],
                                        ElectricGeneratorState]:
        """
        Returns a response for an electric generator.
        """
        def response(state: ElectricGeneratorState,
                     efficiency: ElectricGeneratorConsumption,
                     limits: ElectricGeneratorLimits) -> ElectricGeneratorState:
            assert_type(state,
                        expected_type=ElectricGeneratorState)
            assert_type(efficiency,
                        expected_type=ElectricGeneratorConsumption)
            assert_type(limits,
                        expected_type=ElectricGeneratorLimits)
            new_state = ElectricGeneratorState(input=RotatingIOState(torque=state.input.torque,
                                                                     rpm=state.input.rpm),
                                               output=ElectricIOState(signal_type=state.output.signal_type,
                                                                      nominal_voltage=state.output.nominal_voltage,
                                                                      electric_power=0.0),
                                               internal=state.internal)
            efficiency_value = efficiency.in_to_out_efficiency_value(state=new_state)
            new_state.output.electric_power = new_state.input.power / efficiency_value
            return new_state
        return response

    @staticmethod
    def reversed_motor() -> Callable[[ElectricMotorState,
                                      ElectricMotorConsumption,
                                      ElectricMotorLimits],
                                      ElectricMotorState]:
        """
        Returns a response for a reversed
        electric motor acting as a generator.
        """
        def response(state: ElectricMotorState,
                     efficiency: ElectricMotorConsumption,
                     limits: ElectricMotorLimits) -> ElectricMotorState:
            assert_type(state,
                        expected_type=ElectricMotorState)
            assert_type(efficiency,
                        expected_type=ElectricMotorConsumption)
            assert_type(limits,
                        expected_type=ElectricMotorLimits)
            new_state = ElectricMotorState(input=ElectricIOState(signal_type=state.input.signal_type,
                                                                 nominal_voltage=state.input.nominal_voltage,
                                                                 electric_power=0.0),
                                           output=RotatingIOState(torque=state.output.torque,
                                                                  rpm=state.output.rpm),
                                           internal=state.internal)
            efficiency_value = efficiency.out_to_in_efficiency_value(state=new_state)
            new_state.input.electric_power = new_state.output.power / efficiency_value
            return new_state
        return response


class FuelToMechanical():
    """
    Contains combustion engines responses.
    """
    @staticmethod
    def liquid_combustion_to_mechanical() -> Callable[[LiquidCombustionEngineState, float,
                                                       float, float, float,
                                                       LiquidCombustionEngineConsumption,
                                                       LiquidCombustionEngineLimits],
                                                      LiquidCombustionEngineState]:
        """
        Returns a response for a liquid combustion
        engine with a first-order lag response.
        """
        def response(state: LiquidCombustionEngineState,
                     load_torque: float,
                     downstream_inertia: float,
                     delta_t: float,
                     control_signal: float,
                     fuel_consumption: LiquidCombustionEngineConsumption,
                     limits: LiquidCombustionEngineLimits) -> LiquidCombustionEngineState:
            assert_type(state,
                        expected_type=LiquidCombustionEngineState)
            assert_type(fuel_consumption,
                        expected_type=LiquidCombustionEngineConsumption)
            assert_type(limits,
                        expected_type=LiquidCombustionEngineLimits)
            assert_type_and_range(load_torque, downstream_inertia,
                                  delta_t,
                                  more_than=0.0)
            assert_type_and_range(control_signal,
                                  more_than=0.0,
                                  less_than=1.0)
            min_torque = limits.relative_limits.output.torque.min(state)
            max_torque = limits.relative_limits.output.torque.max(state)
            torque = (max_torque - min_torque) * control_signal + min_torque
            w_dot = (torque - load_torque) / downstream_inertia
            new_state = LiquidCombustionEngineState(input=LiquidFuelIOState(fuel=state.input.fuel,
                                                                            fuel_liters=0.0),
                                                    output=RotatingIOState(torque=torque,
                                                                           rpm=state.output.rpm + ang_vel_to_rpm(ang_vel=w_dot * delta_t)),
                                                    internal=state.internal)
            fuel_consumption_value = fuel_consumption.in_to_out_fuel_consumption_value(state=new_state)
            new_state.input.fuel_liters = fuel_consumption_value * delta_t
            return new_state
        return response

    @staticmethod
    def gaseous_combustion_to_mechanical() -> Callable[[GaseousCombustionEngineState, float,
                                                       float, float, float,
                                                       GaseousCombustionEngineConsumption,
                                                       GaseousCombustionEngineLimits],
                                                       GaseousCombustionEngineState]:
        """
        Returns a response for a gaseous combustion
        engine with a first-order lag response.
        """
        def response(state: GaseousCombustionEngineState,
                     load_torque: float,
                     downstream_inertia: float,
                     delta_t: float,
                     control_signal: float,
                     fuel_consumption: GaseousCombustionEngineConsumption,
                     limits: GaseousCombustionEngineLimits) -> GaseousCombustionEngineState:
            assert_type(state,
                        expected_type=GaseousCombustionEngineState)
            assert_type(fuel_consumption,
                        expected_type=GaseousCombustionEngineConsumption)
            assert_type(limits,
                        expected_type=GaseousCombustionEngineLimits)
            assert_type_and_range(load_torque, downstream_inertia,
                                  delta_t,
                                  more_than=0.0)
            assert_type_and_range(control_signal,
                                  more_than=0.0,
                                  less_than=1.0)
            min_torque = limits.relative_limits.output.torque.min(state)
            max_torque = limits.relative_limits.output.torque.max(state)
            torque = (max_torque - min_torque) * control_signal + min_torque
            w_dot = (torque - load_torque) / downstream_inertia
            new_state = GaseousCombustionEngineState(input=GaseousFuelIOState(fuel=state.input.fuel,
                                                                              fuel_mass=0.0),
                                                     output=RotatingIOState(torque=torque,
                                                                            rpm=state.output.rpm + ang_vel_to_rpm(ang_vel=w_dot * delta_t)),
                                                     internal=state.internal)
            fuel_consumption_value = fuel_consumption.in_to_out_fuel_consumption_value(state=new_state) * delta_t
            new_state.input.fuel_mass = fuel_consumption_value
            return new_state
        return response


class FuelToElectric():
    """
    Contains fuel cell responses.
    """
    @staticmethod
    def gaseous_fuel_to_electric() -> Callable[[FuelCellState, float, float,
                                                FuelCellConsumption, FuelCellLimits],
                                               FuelCellState]:
        """
        Returns the response of a gaseous fuel cell.
        """
        def response(state: FuelCellState,
                     delta_t: float,
                     control_signal: float,
                     fuel_consumption: FuelCellConsumption,
                     limits: FuelCellLimits) -> FuelCellState:
            assert_type(state,
                        expected_type=FuelCellState)
            assert_type_and_range(control_signal,
                                  more_than=0.0,
                                  less_than=1.0)
            assert_type_and_range(delta_t,
                                  more_than=0.0,
                                  include_more=False)
            assert_type(fuel_consumption,
                        expected_type=FuelCellConsumption)
            assert_type(limits,
                        expected_type=FuelCellLimits)
            power = (limits.relative_limits.output.power.max(state) - \
                     limits.relative_limits.output.power.min(state)) * control_signal + \
                    limits.relative_limits.output.power.min(state)
            new_state = FuelCellState(input=GaseousFuelIOState(fuel=state.input.fuel,
                                                               fuel_mass=0.0),
                                      output=ElectricIOState(signal_type=state.output.signal_type,
                                                             nominal_voltage=state.output.nominal_voltage,
                                                             electric_power=power),
                                      internal=state.internal)
            fuel_mass = fuel_consumption.in_to_out_fuel_consumption_value(state=new_state) * delta_t
            new_state.input.fuel_mass = fuel_mass
            return new_state
        return response
