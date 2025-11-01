"""
This module contains definitions for the drive train, including
all modules that transmit power to and from the ground.
"""

from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from components.component_io import GearBoxIO
from components.component_snapshot import return_gearbox_snapshot, \
    DriveTrainSnapshot, GearBoxSnapshot
from components.component_state import PureMechanicalState
from components.consumption import GearBoxConsumption
from components.converter import MechanicalConverter
from components.dynamic_response import PureMechanicalDynamicResponse
from components.dynamic_response_curves import MechanicalToMechanical
from components.limitation import MechanicalToMechanicalLimits
from components.port import PortBidirectional, PortInput, PortOutput, \
    PortType
from helpers.functions import assert_type, assert_type_and_range
from helpers.types import PowerType
from simulation.constants import DRIVE_TRAIN_ID


class WheelDrive(Enum):
    """
    Enum class for setting wheel drive.
    """
    FRONT_DRIVE = "FRONT_DRIVE"
    REAR_DRIVE = "REAR_DRIVE"
    ALL_WHEEL_DRIVE = "ALL_WHEEL_DRIVE"


@dataclass
class Wheel():
    """
    Defines the physical properties of the wheels.
    """
    radius: float
    width: float
    mass: float
    air_pressure: float

    def __post_init__(self):
        assert_type(self.radius, self.width, self.mass, self.air_pressure,
                    expected_type=float)

    @property
    def inertia(self) -> float:
        """
        Returns the moment of inertia.
        It assumes a "thick ring" type of wheel, with most of its
        mass concentrated near the rim.
        """
        return 0.75 * self.mass * self.radius**2


@dataclass
class Axle():
    """
    Models a wheel axle.
    """
    _inertia: float
    _mass: float
    _num_wheels: int
    wheel: Wheel

    def __post_init__(self):
        assert_type_and_range(self._inertia, self._mass,
                              more_than=0.0)
        assert_type_and_range(self._num_wheels,
                              more_than=1)
        assert_type(self.wheel,
                    expected_type=Wheel)

    @property
    def inertia(self) -> float:
        """
        Returns the inertia of the axle and its wheels.
        """
        return self._inertia + self._num_wheels * self.wheel.inertia

    @property
    def mass(self) -> float:
        """
        Returns the mass of the axle and its wheels.
        """
        return self._mass + self.wheel.mass * self._num_wheels

    @property
    def num_wheels(self) -> int:
        """
        Returns the number of wheels on the axle.
        """
        return self._num_wheels


@dataclass
class Differential(MechanicalConverter):
    """Models an axle differential."""
    def __init__(self,
                 name: str,
                 mass: float,
                 limits: MechanicalToMechanicalLimits,
                 gear_ratio: float,
                 efficiency: float,
                 inertia: float):
        snap = return_gearbox_snapshot()
        consumption = GearBoxConsumption(
            out_to_in_efficiency_func=lambda s: efficiency,
            in_to_out_efficiency_func=lambda s: efficiency
        )
        dynamic_response = PureMechanicalDynamicResponse(
            forward_response=MechanicalToMechanical.forward_gearbox(
                gear_ratio=gear_ratio,
                efficiency=efficiency
            ),
            reverse_response=MechanicalToMechanical.reverse_gearbox(
                gear_ratio=gear_ratio,
                efficiency=efficiency
            )
        )
        super().__init__(name=name,
                         mass=mass,
                         input=PortBidirectional(exchange=PowerType.MECHANICAL),
                         output=PortBidirectional(exchange=PowerType.MECHANICAL),
                         snapshot=snap,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         inertia=inertia)
        self.gear_ratio = gear_ratio


@dataclass
class GearBox(MechanicalConverter):
    """Models a gear box."""
    def __init__(self,
                 name: str,
                 mass: float,
                 limits: MechanicalToMechanicalLimits,
                 gear_ratio: float,
                 efficiency: float,
                 inertia: float):
        snap = return_gearbox_snapshot()
        consumption = GearBoxConsumption(
            out_to_in_efficiency_func=lambda s: efficiency,
            in_to_out_efficiency_func=lambda s: efficiency
        )
        dynamic_response = PureMechanicalDynamicResponse(
            forward_response=MechanicalToMechanical.forward_gearbox(
                gear_ratio=gear_ratio,
                efficiency=efficiency
            ),
            reverse_response=MechanicalToMechanical.reverse_gearbox(
                gear_ratio=gear_ratio,
                efficiency=efficiency
            )
        )
        super().__init__(name=name,
                         mass=mass,
                         input=PortBidirectional(exchange=PowerType.MECHANICAL),
                         output=PortBidirectional(exchange=PowerType.MECHANICAL),
                         snapshot=snap,
                         limits=limits,
                         consumption=consumption,
                         dynamic_response=dynamic_response,
                         inertia=inertia)
        self.gear_ratio = gear_ratio


@dataclass
class PlanetaryGear(MechanicalConverter):
    """Models a planetary gear train."""
#     def __init__(self,
#                  name: str,
#                  mass: float,
#                  efficiency: float,
#                  reverse_efficiency: float,
#                  inertia: float,
#                  max_power: float=float("inf")):
#         super().__init__(name=name,
#                          mass=mass,
#                          input=PowerType.MECHANICAL,
#                          output=PowerType.MECHANICAL,
#                          max_power=max_power,
#                          efficiency=efficiency,
#                          reverse_efficiency=reverse_efficiency,
#                          inertia=inertia)


@dataclass
class DriveTrain():
    """
    Models the full drive train for the vehicle.
    """
    id: str=field(init=False)
    input: PortBidirectional=field(init=False)
    output: PortBidirectional = field(init=False)
    snapshot: DriveTrainSnapshot=field(init=False)
    front_axle: Axle
    rear_axle: Axle
    wheel_drive: WheelDrive
    differential: Differential
    gearbox: Optional[GearBox]
    #planetarygear: Optional[PlanetaryGear]

    def __post_init__(self):
        for axle in (self.front_axle, self.rear_axle):
            assert_type(axle,
                        expected_type=Axle)
        assert_type(self.wheel_drive,
                    expected_type=WheelDrive)
        assert_type(self.differential,
                    expected_type=Differential)
        assert_type(self.gearbox,
                    expected_type=GearBox,
                    allow_none=True)
        # assert_type(self.planetarygear,
        #             expected_type=PlanetaryGear,
        #             allow_none=True)
        assert isinstance(self.differential.snapshot, GearBoxSnapshot)
        if self.gearbox is not None:
            assert isinstance(self.gearbox.snapshot, GearBoxSnapshot)
            self.snapshot = DriveTrainSnapshot(io=GearBoxIO(input_port=self.gearbox.snapshot.io.input_port,  # pylint: disable=E1101
                                                            output_port=self.differential.snapshot.io.output_port),  # pylint: disable=E1101
                                               state=PureMechanicalState(input_port=self.gearbox.snapshot.state.input_port,  # pylint: disable=E1101
                                                                         output_port=self.differential.snapshot.state.output_port,  # pylint: disable=E1101
                                                                         internal=self.gearbox.snapshot.state.internal))  # pylint: disable=E1101
        else:
            self.snapshot = DriveTrainSnapshot(io=GearBoxIO(input_port=self.differential.snapshot.io.input_port,  # pylint: disable=E1101
                                                            output_port=self.differential.snapshot.io.output_port),  # pylint: disable=E1101
                                               state=PureMechanicalState(input_port=self.differential.snapshot.state.input_port,  # pylint: disable=E1101
                                                                         output_port=self.differential.snapshot.state.output_port,  # pylint: disable=E1101
                                                                         internal=self.differential.snapshot.state.internal))  # pylint: disable=E1101
        self.input = PortBidirectional(exchange=PowerType.MECHANICAL)
        self.output = PortBidirectional(exchange=PowerType.MECHANICAL)
        self.id = DRIVE_TRAIN_ID

    @property
    def inertia(self) -> float:
        """
        Returns the inertia of the full drive train.
        """
        if self.wheel_drive==WheelDrive.FRONT_DRIVE:
            inertia = self.front_axle.inertia * self.differential.gear_ratio**2
        elif self.wheel_drive==WheelDrive.REAR_DRIVE:
            inertia = self.rear_axle.inertia * self.differential.gear_ratio**2
        else:
            inertia = (self.front_axle.inertia + self.rear_axle.inertia) \
                * self.differential.gear_ratio**2
        if self.gearbox is not None:
            return inertia * self.gearbox.gear_ratio**2
        return inertia

    @property
    def mass(self) -> float:
        """
        Returns the mass of the drive train.
        """
        mass = self.front_axle.mass + self.rear_axle.mass + self.differential.mass
        if self.gearbox is None:
            return mass
        return mass + self.gearbox.mass

    def process_drive(self, snap: DriveTrainSnapshot) -> tuple[DriveTrainSnapshot,
                                                               PureMechanicalState]:
        """
        Processes the drive train from its input.
        """
        assert isinstance(self.differential.snapshot, GearBoxSnapshot)
        assert isinstance(self.differential.dynamic_response, PureMechanicalDynamicResponse)
        if self.gearbox is not None:
            assert isinstance(self.gearbox, GearBox)
            assert isinstance(self.gearbox.snapshot, GearBoxSnapshot)
            assert isinstance(self.gearbox.dynamic_response, PureMechanicalDynamicResponse)
            self.gearbox.snapshot.io.input_port = snap.io.input_port  # pylint: disable=E1101
            self.gearbox.snapshot.state.input_port = snap.state.input_port  # pylint: disable=E1101
            gearbox_snap, gearbox_new_state = self.gearbox.dynamic_response.compute_forward(snap=self.gearbox.snapshot)  # pylint: disable=E1101
            self.gearbox.snapshot = gearbox_snap
            self.gearbox.snapshot.state = gearbox_new_state
            self.differential.snapshot.io.input_port = gearbox_snap.io.output_port  # pylint: disable=E1101
            self.differential.snapshot.state.input_port = gearbox_snap.state.output_port    # pylint: disable=E1101
        else:
            self.differential.snapshot.io.input_port = snap.io.input_port  # pylint: disable=E1101
            self.differential.snapshot.state.input_port = snap.state.input_port    # pylint: disable=E1101
        diff_snap, diff_new_state = self.differential.dynamic_response.compute_forward(snap=self.differential.snapshot)  # pylint: disable=E1101
        self.differential.snapshot = diff_snap
        self.differential.snapshot.state = diff_new_state
        new_snap = deepcopy(snap)
        if self.gearbox is not None:
            new_snap.io.input_port = gearbox_snap.io.input_port # type: ignore
            new_snap.state.input_port = gearbox_new_state.input_port # type: ignore
        else:
            new_snap.io.input_port = diff_snap.io.input_port
            new_snap.state.input_port = diff_new_state.input_port
        new_snap.io.output_port = diff_snap.io.output_port
        new_snap.state.output_port = diff_new_state.output_port
        return new_snap, new_snap.state

    def process_recover(self, snap: DriveTrainSnapshot) -> tuple[DriveTrainSnapshot,
                                                                 PureMechanicalState]:
        """
        Processes the drive train from its output.
        """
        assert isinstance(self.differential.snapshot, GearBoxSnapshot)
        assert isinstance(self.differential.dynamic_response, PureMechanicalDynamicResponse)
        self.differential.snapshot.io.output_port = snap.io.output_port  # pylint: disable=E1101
        diff_snap, diff_new_state = self.differential.dynamic_response.compute_reverse(snap=self.differential.snapshot)  # pylint: disable=E1101
        self.differential.snapshot = diff_snap
        assert isinstance(self.gearbox, GearBox)
        assert isinstance(self.gearbox.snapshot, GearBoxSnapshot)
        assert isinstance(self.gearbox.dynamic_response, PureMechanicalDynamicResponse)
        self.gearbox.snapshot.io.input_port = snap.io.input_port  # pylint: disable=E1101
        gearbox_snap, gearbox_new_state = self.gearbox.dynamic_response.compute_reverse(snap=self.gearbox.snapshot)  # pylint: disable=E1101
        self.gearbox.snapshot = gearbox_snap
        new_snap = snap
        new_snap.io.input_port = gearbox_snap.io.input_port
        new_snap.io.output_port = diff_snap.io.output_port
        new_state = self.snapshot.state
        new_state.input_port = gearbox_new_state.input_port
        new_state.output_port = diff_new_state.output_port
        return new_snap, new_state

    def return_which_port(self, port: PortInput|PortOutput|PortBidirectional) -> Optional[PortType]:
        """
        Returns whether the port is the converter's input or output port.
        """
        if self.input == port:
            return PortType.INPUT_PORT
        if self.output == port:
            return PortType.OUTPUT_PORT
        return None

    @property
    def reversible(self) -> bool:
        """
        Returns the `DriveTrain` as reversible.
        """
        return True


# =====================
# CONVENIENCE FUNCTIONS
# =====================

def return_wheel(radius: float,
                 width: float,
                 mass: float,
                 pressure: float) -> Wheel:
    """
    Returns a `Wheel` object.
    """
    return Wheel(radius=radius,
                 width=width,
                 mass=mass,
                 air_pressure=pressure)

def return_axle(inertia: float,
                mass: float,
                num_wheels: int,
                wheel: Wheel) -> Axle:
    """
    Returns an `Axle` object.
    """
    return Axle(_inertia=inertia,
                _mass=mass,
                _num_wheels=num_wheels,
                wheel=wheel)

def return_differential(mass: float,
                        limits: MechanicalToMechanicalLimits,
                        gear_ratio: float,
                        efficiency: float,
                        inertia: float,
                        name: Optional[str]=None) -> Differential:
    """
    Returns a `Differential` object.
    """
    return Differential(name=name if name is not None else "Differential",
                        mass=mass,
                        limits=limits,
                        gear_ratio=gear_ratio,
                        efficiency=efficiency,
                        inertia=inertia)

def return_gearbox(mass: float,
                   limits: MechanicalToMechanicalLimits,
                   gear_ratio: float,
                   efficiency: float,
                   inertia: float,
                   name: Optional[str]=None) -> GearBox:
    """
    Returns a `GearBox` object.
    """
    return GearBox(name=name if name is not None else "Gearbox",
                   mass=mass,
                   limits=limits,
                   gear_ratio=gear_ratio,
                   efficiency=efficiency,
                   inertia=inertia)

def return_drive_train(front_axle: Axle,
                       rear_axle: Axle,
                       wheel_drive: WheelDrive,
                       differential: Differential,
                       gearbox: Optional[GearBox]=None) -> DriveTrain:
    """
    Returns a full `DriveTrain` object
    by combining each individual component.
    """
    return DriveTrain(front_axle=front_axle,
                      rear_axle=rear_axle,
                      wheel_drive=wheel_drive,
                      differential=differential,
                      gearbox=gearbox)
