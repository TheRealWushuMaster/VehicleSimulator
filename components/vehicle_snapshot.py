"""This module contains definitions for the snapshot of the `Vehicle` class."""

from dataclasses import dataclass
from helpers.functions import assert_type, assert_type_and_range
from simulation.constants import DEFAULT_TEMPERATURE


@dataclass
class VehicleInputs():
    """
    Contains the inputs of the vehicle.
    """
    throttle: float
    brake: float
    load_torque: float

    def __post_init__(self):
        assert_type_and_range(self.throttle, self.brake,
                              more_than=0.0,
                              less_than=1.0)
        assert_type_and_range(self.load_torque)


@dataclass
class VehicleOutputs():
    """
    Contains the outputs of the vehicle.
    """
    tractive_torque: float

    def __post_init__(self):
        assert_type_and_range(self.tractive_torque)


@dataclass
class VehicleIO():
    """
    Contains the inputs and outputs of the vehicle.
    """
    inputs: VehicleInputs
    outputs: VehicleOutputs

    def __post_init__(self):
        assert_type(self.inputs,
                    expected_type=VehicleInputs)
        assert_type(self.outputs,
                    expected_type=VehicleOutputs)


@dataclass
class VehicleState():
    """
    Contains the state variables of the vehicle.
    """
    position: float=0.0
    temperature: float=DEFAULT_TEMPERATURE
    velocity: float=0.0

    def __post_init__(self):
        assert_type_and_range(self.temperature,
                              more_than=0.0)
        assert_type_and_range(self.position, self.velocity)


@dataclass
class VehicleSnapshot():
    """
    Contains the full details of the vehicle
    """
    io: VehicleIO
    state: VehicleState

    def __post_init__(self):
        assert_type(self.io,
                    expected_type=VehicleIO)
        assert_type(self.state,
                    expected_type=VehicleState)

    @property
    def to_dict(self) -> dict[str, float]:
        return {"throttle": self.io.inputs.throttle,
                "brake": self.io.inputs.brake,
                "load_torque": self.io.inputs.load_torque,
                "tractive_torque": self.io.outputs.tractive_torque,
                "position": self.state.position,
                "velocity": self.state.velocity,
                "temperature": self.state.temperature}


def return_vehicle_snapshot(throttle: float=0.0,
                            brake: float=0.0,
                            load_torque: float=0.0,
                            tractive_torque: float=0.0,
                            position: float=0.0,
                            temperature: float=DEFAULT_TEMPERATURE,
                            velocity: float=0.0) -> VehicleSnapshot:
    """
    Returns an instance of `VehicleSnapshot`.
    """
    return VehicleSnapshot(io=VehicleIO(inputs=VehicleInputs(throttle=throttle,
                                                             brake=brake,
                                                             load_torque=load_torque),
                                        outputs=VehicleOutputs(tractive_torque=tractive_torque)),
                           state=VehicleState(position=position,
                                              temperature=temperature,
                                              velocity=velocity))
