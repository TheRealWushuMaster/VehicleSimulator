"""
This module contains definitions for creating a complete vehicle
for the simulation.
"""

from dataclasses import dataclass, field
from components.body import Body
from components.brake import Brake
from components.converter import Converter
from components.drive_train import DriveTrain
from components.ecu import ECU
from components.energy_source import EnergySource
from components.link import Link
from components.message import RequestStack
from components.port import PortInput, PortBidirectional


@dataclass
class Vehicle():
    """
    Combines all vehicle components into a comprehensive model.
    """
    energy_sources: list[EnergySource]
    converters: list[Converter]
    body: Body
    brake: Brake
    drive_train: DriveTrain
    links: list[Link]
    ecu: ECU
    request_stack: RequestStack=field(init=False)

    def __post_init__(self):
        self.request_stack = RequestStack()

    def add_component(self, component: EnergySource|Converter) -> None:
        """
        Adds a new component to the vehicle.
        """
        if isinstance(component, EnergySource):
            if component not in self.energy_sources:
                self.energy_sources.append(component)
        elif isinstance(component, Converter):
            if component not in self.converters:
                self.converters.append(component)
        else:
            raise TypeError("Component must be either EnergySource or Converter.")

    def add_link(self, link: Link) -> None:
        """
        Adds a link to the vehicle.
        Both components to be linked must be present.
        """
        assert isinstance(link, Link)
        if not link in self.links:
            all_ids = [component.id for component in self.energy_sources + self.converters]
            if link.component1_id in all_ids and link.component2_id in all_ids:
                self.links.append(link)

    def find_suppliers(self, port: PortInput|PortBidirectional
                       ) -> list[EnergySource|Converter]:
        raise NotImplementedError
