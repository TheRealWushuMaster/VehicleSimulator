"""
This module contains definitions for mechanical braking systems.
"""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Brake():
    """
    Base class for all types of brakes.
    """
    id: str=field(init=False)
    name: str

    def __post_init__(self):
        self.id = f"Brake-{uuid4()}"


@dataclass
class DiskBrake(Brake):
    ...


@dataclass
class DrumBrake(Brake):
    ...
