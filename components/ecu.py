"""
This module contains definitions for different types of ECUs.
"""

from dataclasses import dataclass

@dataclass
class ECU():
    ...


@dataclass
class ElectricECU(ECU):
    ...


@dataclass
class HybridECU(ECU):
    ...


@dataclass
class PluginHybridECU(ECU):
    ...
