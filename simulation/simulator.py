"""
This module implements a simulator that resolve the state of each
component of a vehicle at each time step.
"""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any
from components.component_snapshot import ElectricMotorSnapshot, \
    RechargeableBatterySnapshot, NonRechargeableBatterySnapshot
from components.energy_source import Battery
from components.message import RequestMessage, DeliveryMessage
from components.motor import ElectricMotor
from components.vehicle import Vehicle
from simulation.constants import DEFAULT_PRECISION
from helpers.functions import assert_type, assert_type_and_range


@dataclass
class Simulator():
    """
    Carries out the simulation at each time step.
    """
    name: str
    time_steps: int
    delta_t: float
    control_signal: list[float]
    vehicle: Vehicle
    history: dict[str, dict[str, Any]]
    _precision: int=DEFAULT_PRECISION

    def __init__(self, name: str,
                 time_steps: int,
                 delta_t: float,
                 control_signal: list[float],
                 vehicle: Vehicle,
                 precision: int=DEFAULT_PRECISION) -> None:
        assert len(name) > 0
        assert_type(time_steps,
                    expected_type=int)
        assert_type_and_range(time_steps, delta_t,
                              more_than=0.0,
                              include_more=False)
        for control in control_signal:
            assert_type_and_range(control,
                                  more_than=0.0,
                                  less_than=1.0)
        assert_type(vehicle,
                    expected_type=Vehicle)
        assert isinstance(precision, int)
        precision = max(precision, -1)
        self.name = name
        self.time_steps = time_steps
        self.delta_t = delta_t
        self.control_signal = control_signal
        self.vehicle = vehicle
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
                "snap_type": converter.snapshot.__class__
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
            for converter in self.vehicle.converters:
                if isinstance(converter, ElectricMotor):
                    assert isinstance(converter.snapshot, ElectricMotorSnapshot)
                    new_snap, new_state = converter.dynamic_response.compute_forward(
                        snap=converter.snapshot,
                        load_torque=load_torque,
                        downstream_inertia=converter.inertia,
                        delta_t=self.delta_t,
                        control_signal=self.control_signal[n],
                        efficiency=converter.consumption,
                        limits=converter.limits)
                    energy = converter.consumption.compute_in_to_out(snap=new_snap,
                                                                     delta_t=self.delta_t)
                    power = energy / self.delta_t
                    if power > 0.0:
                        if self.vehicle.request_stack.add_request(request=RequestMessage(sender_id=converter.id,
                                                                                         from_port=converter.input,
                                                                                         requested=power)):
                            self.resolve_stack()
                    self.history[converter.id]["snapshots"].append(new_snap)
                    converter.snapshot.io = new_snap.io
                    converter.snapshot.state = new_state
            for energy_source in self.vehicle.energy_sources:
                if isinstance(energy_source, Battery):
                    assert isinstance(energy_source.snapshot, (RechargeableBatterySnapshot,
                                                               NonRechargeableBatterySnapshot))
                    energy_source.update_charge(delta_t=self.delta_t)
                    new_snap = deepcopy(energy_source.snapshot)  # type: ignore
                    self.history[energy_source.id]["snapshots"].append(new_snap)
                    energy_source.snapshot.io.output_port.electric_power = 0.0

    def resolve_stack(self) -> None:
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
