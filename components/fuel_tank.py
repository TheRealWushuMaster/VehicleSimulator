"""
This module contains definitions for fuel tanks for various fuels.
"""

from dataclasses import dataclass
from components.energy_source import LiquidFuelTank, GaseousFuelTank
from components.fuel_type import Biodiesel, Ethanol, Diesel, Gasoline, \
    HydrogenGas, HydrogenLiquid, Methanol, Methane

# =================
# LIQUID FUEL TANKS
# =================

@dataclass
class GasolineTank(LiquidFuelTank):
    """
    Models a gasoline (liquid) tank.
    """
    def __init__(self,
                 name: str,
                 capacity_litres: float,
                 litres: float,
                 tank_mass: float):
        super().__init__(name=name,
                         fuel=Gasoline(),
                         capacity_litres=capacity_litres,
                         litres=litres,
                         tank_mass=tank_mass)


@dataclass
class DieselTank(LiquidFuelTank):
    """
    Models a diesel (liquid) tank.
    """
    def __init__(self,
                 name: str,
                 capacity_litres: float,
                 litres: float,
                 tank_mass: float):
        super().__init__(name=name,
                         fuel=Diesel(),
                         capacity_litres=capacity_litres,
                         litres=litres,
                         tank_mass=tank_mass)


@dataclass
class HydrogenLiquidTank(LiquidFuelTank):
    """
    Models a hydrogen (liquid) tank.
    """
    def __init__(self,
                 name: str,
                 capacity_litres: float,
                 litres: float,
                 tank_mass: float):
        super().__init__(name=name,
                         fuel=HydrogenLiquid(),
                         capacity_litres=capacity_litres,
                         litres=litres,
                         tank_mass=tank_mass)


@dataclass
class EthanolTank(LiquidFuelTank):
    """
    Models an ethanol (liquid) tank.
    """
    def __init__(self,
                 name: str,
                 capacity_litres: float,
                 litres: float,
                 tank_mass: float):
        super().__init__(name=name,
                         fuel=Ethanol(),
                         capacity_litres=capacity_litres,
                         litres=litres,
                         tank_mass=tank_mass)


@dataclass
class MethanolTank(LiquidFuelTank):
    """
    Models a methanol (liquid) tank.
    """
    def __init__(self,
                 name: str,
                 capacity_litres: float,
                 litres: float,
                 tank_mass: float):
        super().__init__(name=name,
                         fuel=Methanol(),
                         capacity_litres=capacity_litres,
                         litres=litres,
                         tank_mass=tank_mass)


@dataclass
class BiodieselTank(LiquidFuelTank):
    """
    Models a biodiesel (liquid) tank.
    """
    def __init__(self,
                 name: str,
                 capacity_litres: float,
                 litres: float,
                 tank_mass: float):
        super().__init__(name=name,
                         fuel=Biodiesel(),
                         capacity_litres=capacity_litres,
                         litres=litres,
                         tank_mass=tank_mass)

# ==================
# GASEOUS FUEL TANKS
# ==================

@dataclass
class HydrogenGasTank(GaseousFuelTank):
    """
    Models a hydrogen (gaseous) tank.
    """
    def __init__(self,
                 name: str,
                 capacity_kg: float,
                 kg: float,
                 tank_mass: float):
        super().__init__(name=name,
                         fuel=HydrogenGas(),
                         capacity_kg=capacity_kg,
                         kg=kg,
                         tank_mass=tank_mass)


@dataclass
class MethaneTank(GaseousFuelTank):
    """
    Models a methane (gaseous) tank.
    """
    def __init__(self,
                 name: str,
                 capacity_kg: float,
                 kg: float,
                 tank_mass: float):
        super().__init__(name=name,
                         fuel=Methane(),
                         capacity_kg=capacity_kg,
                         kg=kg,
                         tank_mass=tank_mass)
