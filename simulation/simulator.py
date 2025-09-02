"""
This module implements a simulator that resolve the state of each
component of a vehicle at each time step.
"""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any
from components.energy_source import Battery
from components.message import RequestMessage, DeliveryMessage
from components.motor import ElectricMotor
from components.vehicle import Vehicle
from helpers.functions import assert_type, assert_type_and_range


@dataclass
class Simulator():
    """
    Carries out the simulation at each time step.
    """
    time_steps: int
    delta_t: float
    control_signal: list[float]
    vehicle: Vehicle
    history: dict[str, dict[str, Any]]

    def __init__(self, time_steps: int,
                 delta_t: float,
                 control_signal: list[float],
                 vehicle: Vehicle) -> None:
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
        self.time_steps = time_steps
        self.delta_t = delta_t
        self.control_signal = control_signal
        self.vehicle = vehicle
        self.history = {}
        self.create_history_structure()

    def create_history_structure(self) -> None:
        """
        Fills the history element with sections
        for each component in the vehicle.
        """
        for source in self.vehicle.energy_sources:
            self.history[source.id] = {
                "states": [],
                "component_type": source.__class__,
                "state_type": source.state.__class__
            }
        for converter in self.vehicle.converters:
            self.history[converter.id] = {
                "states": [],
                "type": converter.__class__,
                "state_type": converter.state.__class__
            }

    def simulate(self, load_torque: float) -> None:
        """
        Simulates all time steps and stores state
        variables in the simulation history list.
        """
        for n in range(self.time_steps):
            #self.vehicle.request_stack.reset
            for converter in self.vehicle.converters:
                if isinstance(converter, ElectricMotor):
                    new_state = converter.dynamic_response.compute_forward(state=converter.state,
                                                                           load_torque=load_torque,
                                                                           downstream_inertia=converter.inertia,
                                                                           delta_t=self.delta_t,
                                                                           control_signal=self.control_signal[n],
                                                                           efficiency=converter.consumption,
                                                                           limits=converter.limits)
                    converter.state.output.torque = new_state.output.torque
                    energy = converter.consumption.compute_in_to_out(state=converter.state,
                                                                     delta_t=self.delta_t)
                    power = energy / self.delta_t
                    if power > 0.0:
                        if self.vehicle.request_stack.add_request(request=RequestMessage(sender_id=converter.id,
                                                                                         from_port=converter.input,
                                                                                         requested=power)):
                            self.resolve_stack()
                            self.history[converter.id]["states"].append(new_state)
                    converter.state.output.rpm = new_state.output.rpm
            for energy_source in self.vehicle.energy_sources:
                if isinstance(energy_source, Battery):
                    energy_source.update_charge(delta_t=self.delta_t)
                    new_state = deepcopy(energy_source.state)
                    self.history[energy_source.id]["states"].append(new_state)
                    energy_source.state.output.electric_power = 0.0

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
                 # must update the requester's state accordingly
        else:
            port_type = requester.return_which_port(port=request.from_port)
            assert port_type is not None
            requester.add_request(amount=request.requested,
                                  which_port=port_type)

