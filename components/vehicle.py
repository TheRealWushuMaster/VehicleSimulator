"""
This module contains definitions for creating a complete vehicle
for the simulation.
"""

from dataclasses import dataclass, field
from typing import Optional
#from components.body import Body
#from components.brake import Brake
from components.converter import Converter
#from components.drive_train import DriveTrain
#from components.ecu import ECU
from components.energy_source import EnergySource
from components.link import Link
from components.message import MessageStack
from components.port import PortType


@dataclass
class Vehicle():
    """
    Combines all vehicle components into a comprehensive model.
    """
    energy_sources: list[EnergySource]
    converters: list[Converter]
    #body: Body
    #brake: Brake
    #drive_train: DriveTrain
    links: list[Link]
    #ecu: Optional[ECU]=field(default=None)
    request_stack: MessageStack=field(init=False)

    def __post_init__(self):
        self.request_stack = MessageStack()

    # def add_ecu(self, ecu: ECU) -> bool:
    #     """
    #     Adds an ECU to the vehicle, which needs
    #     access to all vehicle components.
    #     """
    #     if isinstance(ecu, ECU):
    #         self.ecu = ecu
    #         ecu.vehicle = self
    #         return True
    #     return False

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

    @property
    def return_all_components(self) -> list[EnergySource|Converter]:
        """
        Returns a list of all components registered.
        """
        return self.energy_sources + self.converters

    def find_component_with_id(self, component_id: str
                               ) -> Optional[EnergySource|Converter]:
        """
        Returns the component with corresponding id.
        """
        all_components = self.return_all_components
        return next((component for component in all_components
                     if component.id==component_id), None)

    def find_suppliers(self, requester: EnergySource|Converter,
                       which_port: PortType
                       ) -> Optional[list[EnergySource|Converter]]:
        """
        Returns the list of components that can supply resources
        to a component's input port, obtained via analysis of the
        established links between the components.
        """
        connected_links = [link for link in self.links
                          if (requester.id, which_port) in
                          [(link.component1_id, link.component1_port),
                           (link.component2_id, link.component2_port)]]
        if not connected_links:
            return None
        supplier_ids = [link.component1_id if link.component1_id!=requester.id else link.component2_id
                        for link in connected_links]
        if not supplier_ids:
            return None
        return [component
                for component_id in supplier_ids
                if (component := self.find_component_with_id(component_id)) is not None]
