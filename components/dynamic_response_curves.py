"""This module contains several dynamic response curves for different components."""

from typing import Callable
from components.consumption import ElectricMotorConsumption, ElectricGeneratorConsumption, \
    LiquidCombustionEngineConsumption, GaseousCombustionEngineConsumption, \
    FuelCellConsumption
from components.limitation import ElectricGeneratorLimits, \
    ElectricMotorLimits, LiquidCombustionEngineLimits, GaseousCombustionEngineLimits, \
        FuelCellLimits
from components.component_io import GearBoxIO, MechanicalIO, ElectricRectifierIO, \
    ElectricIO, ElectricInverterIO, ElectricMotorIO, ElectricGeneratorIO, \
    LiquidInternalCombustionEngineIO, GaseousInternalCombustionEngineIO, \
    FuelCellIO
from components.component_snapshot import GearBoxSnapshot, \
    ElectricInverterSnapshot, ElectricRectifierSnapshot, \
    ElectricMotorSnapshot, ElectricGeneratorSnapshot, \
    LiquidCombustionEngineSnapshot, GaseousCombustionEngineSnapshot, \
    FuelCellSnapshot
from components.component_state import PureMechanicalState, \
    PureElectricState, \
    ElectricMotorState, ElectricGeneratorState, \
    InternalCombustionEngineState, \
    RotatingState, FuelCellState
from helpers.functions import assert_type, assert_type_and_range, \
    ang_vel_to_rpm


class MechanicalToMechanical():
    """
    Contains generator methods for purely mechanical components.
    """
    @staticmethod
    def forward_gearbox(gear_ratio: float, efficiency: float
                        ) -> Callable[[GearBoxSnapshot, float, float, float],
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
        def response(snap: GearBoxSnapshot,
                     delta_t: float,
                     load_torque: float,
                     downstream_inertia: float) -> tuple[GearBoxSnapshot,
                                                     PureMechanicalState]:
            assert isinstance(snap, GearBoxSnapshot)
            inertia_at_input = downstream_inertia / gear_ratio**2
            load_torque_at_input = load_torque / gear_ratio / efficiency
            net_torque_at_input = snap.io.input_port.torque - load_torque_at_input 
            w_dot_in = net_torque_at_input / inertia_at_input
            rpm_in = snap.state.input_port.rpm + ang_vel_to_rpm(ang_vel=w_dot_in*delta_t)
            rpm_out = rpm_in / gear_ratio
            torque_out = snap.io.input_port.torque * gear_ratio * efficiency
            # w_dot_out = (torque_out - load_torque) / downstream_inertia
            # rpm_out = snap.state.output_port.rpm + ang_vel_to_rpm(ang_vel=w_dot_out*delta_t)
            # rpm_in = rpm_out * gear_ratio
            new_state = PureMechanicalState(input_port=RotatingState(rpm=rpm_in),
                                            internal=snap.state.internal,
                                            output_port=RotatingState(rpm=rpm_out))
            new_snap = GearBoxSnapshot(io=GearBoxIO(input_port=snap.io.input_port,
                                                    output_port=MechanicalIO(torque=torque_out)),
                                       state=new_state)
            return new_snap, new_state
        return response

    @staticmethod
    def reverse_gearbox(gear_ratio: float, efficiency: float
                        ) -> Callable[[GearBoxSnapshot, float, float, float],
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
        def response(snap: GearBoxSnapshot,
                     delta_t: float,
                     load_torque: float,
                     upstream_inertia: float) -> tuple[GearBoxSnapshot,
                                                     PureMechanicalState]:
            assert isinstance(snap, GearBoxSnapshot)
            torque_in = snap.io.output_port.torque / gear_ratio * efficiency
            w_dot = (torque_in - load_torque) / upstream_inertia
            rpm_in = snap.state.output_port.rpm * gear_ratio + ang_vel_to_rpm(ang_vel=w_dot*delta_t)
            new_state = PureMechanicalState(input_port=RotatingState(rpm=rpm_in),
                                            internal=snap.state.internal,
                                            output_port=snap.state.output_port)
            new_snap = GearBoxSnapshot(io=GearBoxIO(input_port=MechanicalIO(torque=torque_in),
                                                    output_port=snap.io.output_port),
                                       state=new_state)
            
            torque_in = snap.io.output_port.torque / gear_ratio * efficiency
            w_dot_in = (torque_in - load_torque) / upstream_inertia
            rpm_in = snap.state.input_port.rpm + ang_vel_to_rpm(ang_vel=w_dot_in*delta_t)
            rpm_out = rpm_in / gear_ratio
            new_state = PureMechanicalState(input_port=RotatingState(rpm=rpm_in),
                                            internal=snap.state.internal,
                                            output_port=RotatingState(rpm=rpm_out))
            new_snap = GearBoxSnapshot(io=GearBoxIO(input_port=MechanicalIO(torque=torque_in),
                                                    output_port=snap.io.input_port),
                                       state=new_state)
            return new_snap, new_state
        return response


class ElectricToElectric():
    """
    Contains responses for electric to electric components.
    """
    @staticmethod
    def rectifier_response(efficiency: float
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
                                                 state=snap.state)
            new_state = PureElectricState(internal=snap.state.internal)
            return new_snap, new_state
        return response

    @staticmethod
    def inverter_response(efficiency: float
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
                                                state=snap.state)
            new_state = PureElectricState(internal=snap.state.internal)
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
            efficiency_value = efficiency.in_to_out_efficiency_value(snap=snap)
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
    def forward_generator() -> Callable[[ElectricGeneratorSnapshot,
                                         ElectricGeneratorConsumption,
                                         ElectricGeneratorLimits],
                                        tuple[ElectricGeneratorSnapshot,
                                              ElectricGeneratorState]]:
        """
        Returns a response for an electric generator.
        """
        def response(snap: ElectricGeneratorSnapshot,
                     efficiency: ElectricGeneratorConsumption,
                     limits: ElectricGeneratorLimits) -> tuple[ElectricGeneratorSnapshot,
                                                               ElectricGeneratorState]:
            assert_type(snap,
                        expected_type=ElectricGeneratorSnapshot)
            assert_type(efficiency,
                        expected_type=ElectricGeneratorConsumption)
            assert_type(limits,
                        expected_type=ElectricGeneratorLimits)
            new_snap = ElectricGeneratorSnapshot(io=ElectricGeneratorIO(input_port=snap.io.input_port,
                                                                        output_port=snap.io.output_port),
                                                 state=ElectricGeneratorState(input_port=snap.state.input_port,
                                                                              internal=snap.state.internal))
            efficiency_value = efficiency.in_to_out_efficiency_value(snap=new_snap)
            power_out = new_snap.power_in * efficiency_value
            new_snap.io.output_port.electric_power = power_out
            new_state = new_snap.state
            return new_snap, new_state
        return response

    @staticmethod
    def reversed_motor() -> Callable[[ElectricMotorSnapshot,
                                      ElectricMotorConsumption,
                                      ElectricMotorLimits],
                                     tuple[ElectricMotorSnapshot,
                                           ElectricMotorState]]:
        """
        Returns a response for a reversed
        electric motor acting as a generator.
        """
        def response(snap: ElectricMotorSnapshot,
                     efficiency: ElectricMotorConsumption,
                     limits: ElectricMotorLimits) -> tuple[ElectricMotorSnapshot,
                                                           ElectricMotorState]:
            assert_type(snap,
                        expected_type=ElectricMotorSnapshot)
            assert_type(efficiency,
                        expected_type=ElectricMotorConsumption)
            assert_type(limits,
                        expected_type=ElectricMotorLimits)
            new_snap = ElectricMotorSnapshot(io=ElectricMotorIO(input_port=snap.io.input_port,
                                                                output_port=snap.io.output_port),
                                             state=ElectricMotorState(internal=snap.state.internal,
                                                                      output_port=snap.state.output_port))
            efficiency_value = efficiency.out_to_in_efficiency_value(snap=new_snap)
            power_in = new_snap.power_out * efficiency_value
            new_snap.io.input_port.electric_power = power_in
            new_state = snap.state
            return new_snap, new_state
        return response


class FuelToMechanical():
    """
    Contains combustion engines responses.
    """
    @staticmethod
    def liquid_combustion_to_mechanical() -> Callable[[LiquidCombustionEngineSnapshot, float,
                                                       float, float, float,
                                                       LiquidCombustionEngineConsumption,
                                                       LiquidCombustionEngineLimits],
                                                      tuple[LiquidCombustionEngineSnapshot,
                                                            InternalCombustionEngineState]]:
        """
        Returns a response for a liquid combustion
        engine with a first-order lag response.
        """
        def response(snap: LiquidCombustionEngineSnapshot,
                     load_torque: float,
                     downstream_inertia: float,
                     delta_t: float,
                     control_signal: float,
                     fuel_consumption: LiquidCombustionEngineConsumption,
                     limits: LiquidCombustionEngineLimits) -> tuple[LiquidCombustionEngineSnapshot,
                                                                    InternalCombustionEngineState]:
            assert_type(snap,
                        expected_type=LiquidCombustionEngineSnapshot)
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
            min_torque = limits.relative_limits.output.torque.min(snap)
            max_torque = limits.relative_limits.output.torque.max(snap)
            torque = (max_torque - min_torque) * control_signal + min_torque
            w_dot = (torque - load_torque) / downstream_inertia
            new_rpm = snap.state.output_port.rpm + ang_vel_to_rpm(ang_vel=w_dot * delta_t)
            new_snap = LiquidCombustionEngineSnapshot(io=LiquidInternalCombustionEngineIO(input_port=snap.io.input_port,
                                                                                          output_port=MechanicalIO(torque=torque)),
                                                      state=snap.state)
            fuel_consumption_value = fuel_consumption.in_to_out_fuel_consumption_value(snap=new_snap) * delta_t
            new_snap.io.input_port.liters_flow = fuel_consumption_value
            new_state = InternalCombustionEngineState(internal=snap.state.internal,
                                                      output_port=RotatingState(rpm=new_rpm))
            return new_snap, new_state
        return response

    @staticmethod
    def gaseous_combustion_to_mechanical() -> Callable[[GaseousCombustionEngineSnapshot, float,
                                                        float, float, float,
                                                        GaseousCombustionEngineConsumption,
                                                        GaseousCombustionEngineLimits],
                                                       tuple[GaseousCombustionEngineSnapshot,
                                                             InternalCombustionEngineState]]:
        """
        Returns a response for a gaseous combustion
        engine with a first-order lag response.
        """
        def response(snap: GaseousCombustionEngineSnapshot,
                     load_torque: float,
                     downstream_inertia: float,
                     delta_t: float,
                     control_signal: float,
                     fuel_consumption: GaseousCombustionEngineConsumption,
                     limits: GaseousCombustionEngineLimits) -> tuple[GaseousCombustionEngineSnapshot,
                                                                     InternalCombustionEngineState]:
            assert_type(snap,
                        expected_type=GaseousCombustionEngineSnapshot)
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
            min_torque = limits.relative_limits.output.torque.min(snap)
            max_torque = limits.relative_limits.output.torque.max(snap)
            torque = (max_torque - min_torque) * control_signal + min_torque
            w_dot = (torque - load_torque) / downstream_inertia
            new_rpm = snap.state.output_port.rpm + ang_vel_to_rpm(ang_vel=w_dot * delta_t)
            new_snap = GaseousCombustionEngineSnapshot(io=GaseousInternalCombustionEngineIO(input_port=snap.io.input_port,
                                                                                            output_port=MechanicalIO(torque=torque)),
                                                       state=snap.state)
            fuel_consumption_value = fuel_consumption.in_to_out_fuel_consumption_value(snap=new_snap) * delta_t
            new_snap.io.input_port.mass_flow = fuel_consumption_value
            new_state = InternalCombustionEngineState(internal=snap.state.internal,
                                                      output_port=RotatingState(rpm=new_rpm))
            return new_snap, new_state
        return response


class FuelToElectric():
    """
    Contains fuel cell responses.
    """
    @staticmethod
    def gaseous_fuel_to_electric() -> Callable[[FuelCellSnapshot, float, float,
                                                FuelCellConsumption, FuelCellLimits],
                                               tuple[FuelCellSnapshot,
                                                     FuelCellState]]:
        """
        Returns the response of a gaseous fuel cell.
        """
        def response(snap: FuelCellSnapshot,
                     delta_t: float,
                     control_signal: float,
                     fuel_consumption: FuelCellConsumption,
                     limits: FuelCellLimits) -> tuple[FuelCellSnapshot,
                                                      FuelCellState]:
            assert_type(snap,
                        expected_type=FuelCellSnapshot)
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
            power_out = (limits.relative_limits.output.power.max(snap) - \
                        limits.relative_limits.output.power.min(snap)) * control_signal + \
                        limits.relative_limits.output.power.min(snap)
            new_snap = FuelCellSnapshot(io=FuelCellIO(input_port=snap.io.input_port,
                                                      output_port=ElectricIO(electric_power=power_out)),
                                        state=snap.state)
            new_state = FuelCellState(internal=snap.state.internal)
            fuel_mass = fuel_consumption.in_to_out_fuel_consumption_value(snap=new_snap) * delta_t
            new_snap.io.input_port.mass_flow = fuel_mass
            return new_snap, new_state
        return response
