"""
This module implements a simulator that resolve the state of each
component of a vehicle at each time step.
"""

from dataclasses import dataclass
from typing import Any
from components.message import RequestMessage
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
        for n in range(self.time_steps):
            for converter in self.vehicle.converters:
                new_state = converter.dynamic_response.compute_forward(state=converter.state, # type: ignore
                                                                       load_torque=load_torque,
                                                                       downstream_inertia=converter.inertia,  # type: ignore
                                                                       delta_t=self.delta_t,
                                                                       control_signal=self.control_signal[n],
                                                                       efficiency=converter.consumption,
                                                                       limits=converter.limits)
                converter.state.output.torque = new_state.output.torque  # type: ignore
                energy = converter.consumption.compute_in_to_out(state=converter.state,  # type: ignore
                                                                 delta_t=self.delta_t)
                #new_state.input.electric_power = energy / self.delta_t
                self.vehicle.request_stack.add_request(request=RequestMessage(sender_id=converter.id,
                                                                              from_port=converter.input,
                                                                              requested=energy / self.delta_t))
                self.resolve_stack()
                self.history[converter.id]["states"].append(new_state)
                converter.state = new_state

    def resolve_stack(self):
        for message in self.vehicle.request_stack.requests:
            if not message.fulfilled:
                requester = self.vehicle.find_component_with_id(component_id=message.sender_id)
                assert requester is not None and requester.input is not None
                which_port = requester.return_which_port(port=message.from_port)
                assert which_port is not None
                suppliers = self.vehicle.find_suppliers(requester=requester,
                                                        which_port=which_port)
                if suppliers is not None:
                    pass
                    
