"""
This module contains definitions for mechanical braking systems.
"""

from dataclasses import dataclass

@dataclass
class Brake():
    ...


@dataclass
class DiskBrake(Brake):
    ...


@dataclass
class DrumBrake(Brake):
    ...
