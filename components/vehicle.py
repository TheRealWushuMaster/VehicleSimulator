"""
This module contains definitions for creating a complete vehicle
for the simulation.
"""

from dataclasses import dataclass, field
from typing import Optional
from components.body import Body
#from components.brake import Brake
from components.converter import Converter
from components.drive_train import DriveTrain
#from components.ecu import ECU
from components.energy_source import EnergySource
from components.link import Link
from components.message import MessageStack
from components.port import PortType
from components.vehicle_snapshot import VehicleSnapshot
from helpers.functions import assert_type
from simulation.constants import DRIVE_TRAIN_ID, VEHICLE_ID


@dataclass
class Vehicle():
    """
    Combines all vehicle components into a comprehensive model.
    """
    id: str=field(init=False)
    energy_sources: list[EnergySource]
    converters: list[Converter]
    body: Body
    #brake: Brake
    drive_train: DriveTrain
    links: list[Link]
    #ecu: Optional[ECU]=field(default=None)
    request_stack: MessageStack=field(init=False)
    snapshot: VehicleSnapshot

    def __post_init__(self):
        for energy_source in self.energy_sources:
            assert_type(energy_source,
                        expected_type=EnergySource)
        for converter in self.converters:
            assert_type(converter,
                        expected_type=Converter)
        assert_type(self.drive_train,
                    expected_type=DriveTrain)
        for link in self.links:
            assert_type(link,
                        expected_type=Link)
        assert_type(self.snapshot,
                    expected_type=VehicleSnapshot)
        self.request_stack = MessageStack()
        self.id = VEHICLE_ID

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

    def _get_inertia(self, component_id: str,
                     which_port: PortType) -> float:
        component = self.find_component_with_id(component_id=component_id)
        if component is None:
            return 0.0
        if not hasattr(component, "inertia"):
            return 0.0
        inertia = getattr(component, "inertia")
        if which_port == PortType.INPUT_PORT:
            comp_list = self.find_suppliers_input(requester=component)
        else:
            comp_list = self.find_suppliers_output(requester=component)
        if comp_list is not None:
            for comp in comp_list:
                if hasattr(comp[0], "inertia"):
                    inertia += self.downstream_inertia(component_id=comp[0].id)
        return inertia

    def downstream_inertia(self, component_id: str) -> float:
        """
        Returns the inertia value as seen from a component's output.
        """
        return self._get_inertia(component_id=component_id,
                                 which_port=PortType.OUTPUT_PORT)

    def upstream_inertia(self, component_id: str) -> float:
        """
        Returns the inertia value as seen from a component's input.
        """
        return self._get_inertia(component_id=component_id,
                                 which_port=PortType.INPUT_PORT)

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
                               ) -> Optional[EnergySource|Converter|DriveTrain]:
        """
        Returns the component with corresponding id.
        """
        if component_id == DRIVE_TRAIN_ID:
            return self.drive_train
        all_components = self.return_all_components
        return next((component for component in all_components
                     if component.id==component_id), None)

    def find_suppliers(self, requester: EnergySource|Converter|DriveTrain,
                       which_port: PortType
                       ) -> Optional[list[tuple[EnergySource|Converter|DriveTrain, PortType]]]:
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
        supplier_info = []
        for link in connected_links:
            if link.component1_id==requester.id:
                supplier_info.append((link.component2_id, link.component2_port))
            else:
                supplier_info.append((link.component1_id, link.component1_port))
        if not supplier_info:
            return None
        result = []
        for supplier_id, supplier_port in supplier_info:
            component = self.find_component_with_id(supplier_id)
            if component is not None:
                result.append((component, supplier_port))
            elif supplier_id == DRIVE_TRAIN_ID:
                result.append((self.drive_train, PortType.INPUT_PORT))
        return result if result else None

    def find_suppliers_input(self, requester: EnergySource|Converter|DriveTrain
                             ) -> Optional[list[tuple[EnergySource|Converter|DriveTrain, PortType]]]:
        """
        Returns suppliers for the `requester` on its input.
        """
        return self.find_suppliers(requester=requester,
                                   which_port=PortType.INPUT_PORT)

    def find_suppliers_output(self, requester: EnergySource|Converter|DriveTrain
                              ) -> Optional[list[tuple[EnergySource|Converter|DriveTrain, PortType]]]:
        """
        Returns suppliers for the `requester` on its output.
        """
        return self.find_suppliers(requester=requester,
                                   which_port=PortType.OUTPUT_PORT)

    @property
    def total_mass(self) -> float:
        """
        Returns the total mass of the vehicle,
        including components and fuel.
        """
        mass: float = 0.0
        for energy_source in self.energy_sources:
            mass += energy_source.total_mass
        for converter in self.converters:
            mass += converter.mass
        mass += self.body.mass
        mass += self.drive_train.mass
        return mass

    def get_input_load_torque(self, component: EnergySource|Converter|DriveTrain
                              ) -> Optional[float]:
        """
        Returns the load torque as seen
        upstream from the component's input.
        """
        if not component.reversible:
            return None
        if isinstance(component, DriveTrain):
            pass
        downstream_components = self.find_suppliers_output(requester=component)
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
        downstream_components = self.find_suppliers_output(requester=component)
        if downstream_components is not None:
            for load_comp in downstream_components:
                pass
        return 0.0
