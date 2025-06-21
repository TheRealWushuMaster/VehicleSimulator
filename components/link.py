"""
This module defines the connection object that ties components
in the vehicle, allowing them to interact.
"""

from dataclasses import dataclass
from typing import Optional
from components.converter import Converter
from components.energy_source import EnergySource
from components.port import PortType
from helpers.functions import assert_type


@dataclass
class Link():
    """
    Defines a link between two components.
    """
    component1_id: str
    component1_port: PortType
    component2_id: str
    component2_port: PortType

    def __post_init__(self):
        assert_type(self.component1_id, self.component2_id,
                    expected_type=str)
        assert_type(self.component1_port, self.component2_port,
                    expected_type=PortType)


def create_link(component1: Converter|EnergySource,
                component1_port: PortType,
                component2: Converter|EnergySource,
                component2_port: PortType) -> Optional[Link]:
    """
    This function creates a link between two components between
    one of their ports.
    """
    assert_type(component1, component2,
                expected_type=(Converter, EnergySource))
    assert_type(component1_port, component2_port,
                expected_type=PortType)
    port1 = component1.return_port(which=component1_port)
    port2 = component2.return_port(which=component2_port)
    assert port1 is not None and port2 is not None
    if port1.is_compatible_with(other=port2):
        return Link(component1_id=component1.id,
                    component1_port=component1_port,
                    component2_id=component2.id,
                    component2_port=component2_port,)
    return None
