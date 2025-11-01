"""
This module implements a simulator that resolve the state of each
component of a vehicle at each time step.
"""

from copy import deepcopy
from dataclasses import dataclass
from math import sin, cos
from typing import Any, Optional
from components.component_snapshot import ElectricMotorSnapshot, \
    RechargeableBatterySnapshot, NonRechargeableBatterySnapshot
from components.converter import Converter
from components.drive_train import DriveTrain
from components.energy_source import EnergySource, Battery
from components.message import RequestMessage, DeliveryMessage
from components.motor import ElectricMotor
from components.vehicle import Vehicle
from simulation.constants import DEFAULT_PRECISION, DRIVE_TRAIN_ID, VEHICLE_ID, GRAVITY
from simulation.track import Track
from helpers.functions import assert_type, assert_type_and_range, rpm_to_velocity


@dataclass
class Simulator():
    """
    Carries out the simulation at each time step.
    """
    name: str
    time_steps: int
    delta_t: float
    throttle_signal: list[float]
    brake_signal: list[float]
    vehicle: Vehicle
    track: Track
    history: dict[str, dict[str, Any]]
    _precision: int=DEFAULT_PRECISION

    def __init__(self, name: str,
                 time_steps: int,
                 delta_t: float,
                 throttle_signal: list[float],
                 brake_signal: list[float],
                 vehicle: Vehicle,
                 track: Track,
                 precision: int=DEFAULT_PRECISION) -> None:
        assert len(name) > 0
        assert_type(time_steps,
                    expected_type=int)
        assert_type_and_range(time_steps, delta_t,
                              more_than=0.0,
                              include_more=False)
        for throttle in throttle_signal:
            assert_type_and_range(throttle,
                                  more_than=0.0,
                                  less_than=1.0)
        for brake in brake_signal:
            assert_type_and_range(brake,
                                  more_than=0.0,
                                  less_than=1.0)
        assert_type(vehicle,
                    expected_type=Vehicle)
        assert isinstance(precision, int)
        precision = max(precision, -1)
        self.name = name
        self.time_steps = time_steps
        self.delta_t = delta_t
        self.throttle_signal = throttle_signal
        self.brake_signal = brake_signal
        self.vehicle = vehicle
        self.track = track
        self.history = {}
        self._precision = precision
        self._create_history_structure()

    def _create_history_structure(self) -> None:
        """
        Fills the history element with sections
        for each component in the vehicle.
        """
        for source in self.vehicle.energy_sources:
            self.history[source.id] = {
                "snapshots": [],
                "comp_name": source.name,
                "comp_type": source.__class__.__name__,
                "snap_type": source.snapshot.__class__.__name__
            }
        for converter in self.vehicle.converters:
            self.history[converter.id] = {
                "snapshots": [],
                "comp_name": converter.name,
                "comp_type": converter.__class__.__name__,
                "snap_type": converter.snapshot.__class__.__name__
            }
        self.history[DRIVE_TRAIN_ID] = {
            "snapshots": [],
            "comp_name": "Drivetrain",
            "comp_type": self.vehicle.drive_train.__class__.__name__,
            "snap_type": self.vehicle.drive_train.snapshot.__class__.__name__
        }
        self.history[VEHICLE_ID] = {
            "snapshots": [],
            "comp_name": "Vehicle",
            "comp_type": self.vehicle.__class__.__name__,
            "snap_type": self.vehicle.snapshot.__class__.__name__
        }

    @property
    def precision(self) -> int:
        """
        Returns the default precision.
        """
        return self._precision

    def simulate(self, load_torque: float) -> None:
        """
        Simulates all time steps and stores state
        variables in the simulation history list.
        """
        for n in range(self.time_steps):
            self.vehicle.request_stack.reset()
            load_torque = self._track_load_torque()
            for converter in self.vehicle.converters:
                self._process_converter(converter=converter,
                                        load_torque=load_torque,
                                        n=n)
            for energy_source in self.vehicle.energy_sources:
                self._process_energy_source(energy_source=energy_source)
            self._process_drive_train()
            self._process_vehicle(n=n,
                                  load_torque=load_torque)

    def _track_load_torque(self, d: Optional[float]=None) -> float:
        if d is None:
            d = self.vehicle.snapshot.state.position
        front_contact = self.track.wheel_contact_point(d=d,
                                                       wheel=self.vehicle.drive_train.front_axle.wheel)
        rear_d = self.track.rear_axle_location(front_axle_d=d,
                                               axle_distance=self.vehicle.body.axle_distance,
                                               front_wheel=self.vehicle.drive_train.front_axle.wheel,
                                               rear_wheel=self.vehicle.drive_train.rear_axle.wheel)
        if rear_d is None:
            return 0.0
        rear_contact = self.track.wheel_contact_point(d=rear_d,
                                                      wheel=self.vehicle.drive_train.rear_axle.wheel)
        assert rear_contact is not None
        vehicle_weight = self.vehicle.total_mass * GRAVITY
        rear_weight = vehicle_weight * self.vehicle.body.cg_location
        front_weight = vehicle_weight - rear_weight
        drag_force = self.drag_force()
        front_angle = self.track.angle_degrees(d=front_contact)
        assert front_angle is not None
        rear_angle = self.track.angle_degrees(d=rear_contact)
        assert rear_angle is not None
        front_normal = front_weight * cos(front_angle)
        front_longitudinal = - front_weight * sin(front_angle)
        rear_normal = rear_weight * cos(rear_angle)
        rear_longitudinal = - rear_weight * sin(rear_angle)
        
        return 0.0
        

    def _propagate_output(self, component: Converter) -> None:
        """
        Propagates an output of a converter to the inputs
        of all components connected to it via its output.
        """
        comp_list = self.vehicle.find_suppliers_output(requester=component)
        out_io = deepcopy(component.snapshot.io.output_port) # type: ignore
        out_st = deepcopy(component.snapshot.state.output_port) # type: ignore
        if comp_list is None:
            return
        for comp, _ in comp_list:   # pylint: disable=E1133
            comp.snapshot.io.input_port = out_io   # type: ignore
            comp.snapshot.state.input_port = out_st # type: ignore

    def _resolve_stack(self) -> None:
        """
        Attempts to resolve any pending resource requests.
        """
        request = self.vehicle.request_stack.pending_request
        if request is None:
            return
        requester = self.vehicle.find_component_with_id(component_id=request.sender_id)
        assert requester is not None and requester.input is not None
        which_port = requester.return_which_port(port=request.from_port)
        assert which_port is not None
        suppliers = self.vehicle.find_suppliers(requester=requester,
                                                which_port=which_port)
        if suppliers is not None:
            for supplier in suppliers:
                assert isinstance(supplier[0], Battery)
                delivered = supplier[0].add_delivery(amount=request.remaining,
                                                     which_port=supplier[1])
                delivery = DeliveryMessage(sender_id=supplier[0].id,
                                           from_port=supplier[0].output,
                                           delivery=delivered)
                request.add_delivery(delivery=delivery)
        if not request.fulfilled:
            pass # If the request could not be fulfilled,
                 # must update the requester's snapshot
                 # accordingly by recalculating the output.

    def _process_converter(self, converter: Converter,
                           load_torque: float,
                           n: int) -> None:
        if isinstance(converter, ElectricMotor):
            assert isinstance(converter.snapshot, ElectricMotorSnapshot)
            inertia = self.vehicle.downstream_inertia(component_id=converter.id)
            new_conv_snap, new_state = converter.dynamic_response.compute_forward(
                snap=converter.snapshot,
                load_torque=load_torque,
                downstream_inertia=inertia,
                delta_t=self.delta_t,
                throttle_signal=self.throttle_signal[n],
                efficiency=converter.consumption,
                limits=converter.limits)
            energy = converter.consumption.compute_in_to_out(snap=new_conv_snap,
                                                                delta_t=self.delta_t)
            power = energy / self.delta_t
            if power > 0.0:
                if self.vehicle.request_stack.add_request(request=RequestMessage(sender_id=converter.id,
                                                                                    from_port=converter.input,
                                                                                    requested=power)):
                    self._resolve_stack()
            self.history[converter.id]["snapshots"].append(new_conv_snap)
            converter.snapshot.io = new_conv_snap.io
            self._propagate_output(component=converter)
            converter.snapshot.state = new_state

    def _process_energy_source(self, energy_source: EnergySource) -> None:
        if isinstance(energy_source, Battery):
            assert isinstance(energy_source.snapshot, (RechargeableBatterySnapshot,
                                                        NonRechargeableBatterySnapshot))
            energy_source.update_charge(delta_t=self.delta_t)
            new_source_snap = deepcopy(energy_source.snapshot)
            self.history[energy_source.id]["snapshots"].append(new_source_snap)
            energy_source.snapshot.io.output_port.electric_power = 0.0

    def _process_drive_train(self) -> None:
        new_dt_snap, new_dt_state = self.vehicle.drive_train.process_drive(snap=self.vehicle.drive_train.snapshot)
        self.history[self.vehicle.drive_train.id]["snapshots"].append(new_dt_snap)
        self.vehicle.drive_train.snapshot.io = deepcopy(new_dt_snap.io)
        self.vehicle.drive_train.snapshot.state = deepcopy(new_dt_state)

    def _process_vehicle(self, n: int,
                         load_torque: float) -> None:
        """
        Updates vehicle properties at the time step.
        """
        new_snap = deepcopy(self.vehicle.snapshot)
        new_snap.io.inputs.throttle = self.throttle_signal[n]
        new_snap.io.inputs.brake = self.brake_signal[n]
        new_snap.io.inputs.load_torque = load_torque
        new_snap.io.outputs.tractive_torque = self.vehicle.drive_train.snapshot.io.output_port.torque
        new_snap.state.velocity = rpm_to_velocity(rpm=self.vehicle.drive_train.snapshot.state.output_port.rpm,
                                                  radius=self.vehicle.drive_train.front_axle.wheel.radius)
        new_position = self.track.advance_distance(d=self.vehicle.snapshot.state.position,
                                                   distance=new_snap.state.velocity * self.delta_t)
        if new_position is not None:
            new_snap.state.position = new_position
        self.history[self.vehicle.id]["snapshots"].append(new_snap)
        self.vehicle.snapshot = new_snap

    def wheels_in_same_section(self) -> Optional[bool]:
        """
        Returns if both axles lie within the same track section.
        """
        section_result = self.track.find_section(d=self.vehicle.snapshot.state.position)
        if section_result is None:
            return None
        beta = section_result.section.angle_degrees(d=section_result.in_section_d)
        if beta is None:
            return None
        front_contact = self.track.wheel_contact_point(d=section_result.in_section_d,
                                                       wheel=self.vehicle.drive_train.front_axle.wheel)
        if front_contact is None:
            return None
        if front_contact - self.vehicle.body.axle_distance * cos(beta) >= 0.0:
            return True
        return False

    def drag_force(self, d: Optional[float]=None) -> float:
        """
        Returns the value of aerodynamic drag force.
        """
        if d is None:
            d = self.vehicle.snapshot.state.position
        front_area = self.vehicle.body.front_area
        density = self.track.air_density(d=d)
        velocity = self.vehicle.snapshot.state.velocity
        drag_coefficient = self.vehicle.body.drag_coefficient
        if density is not None:
            return 0.5 * drag_coefficient * front_area * density * velocity**2
        return 0.0

    def vehicle_angle(self) -> float:
        """
        Returns the angle of the vehicle as the angle between
        the horizontal and the line between both axles.
        """
        if self.wheels_in_same_section():
            section_result = self.track.find_section(d=self.vehicle.snapshot.state.position)
            assert section_result is not None
            front_contact = self.track.wheel_contact_point(d=section_result.in_section_d,
                                                           wheel=self.vehicle.drive_train.front_axle.wheel)
            assert front_contact is not None
            angle = section_result.section.angle_degrees(d=front_contact) 
            assert angle is not None
            return angle
        return 0.0

    def get_input_load_torque(self, component: EnergySource|Converter|DriveTrain
                              ) -> Optional[float]:
        """
        Returns the load torque as seen
        upstream from the component's input.
        """
        if not component.reversible:
            return None
        downstream_components = self.vehicle.find_suppliers_output(requester=component)
        if downstream_components is not None:
            for load_comp in downstream_components:
                pass
        return 0.0

    def get_output_load_torque(self, component: EnergySource|Converter|DriveTrain
                               ) -> float:
        """
        Returns the load torque as seen 
        downstream from the component's output.
        """
        if isinstance(component, DriveTrain):
            pass
        downstream_components = self.vehicle.find_suppliers_output(requester=component)
        if downstream_components is not None:
            for load_comp in downstream_components:
                pass
        return 0.0
