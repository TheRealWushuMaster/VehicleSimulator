"""
This module contains definitions for different types of fuel cells.
"""

from dataclasses import dataclass
from components.fuel_type import Fuel, HydrogenGas, Methanol
from components.power_converter import PowerConverter
from helpers.types import PowerType
from simulation.constants import FUEL_CELL_AFC_DEFAULT_EFFICIENCY, \
    FUEL_CELL_DIR_METH_DEFAULT_EFFICIENCY, FUEL_CELL_MOL_CARB_DEFAULT_EFFICIENCY, \
    FUEL_CELL_PEM_DEFAULT_EFFICIENCY, FUEL_CELL_PH_AC_DEFAULT_EFFICIENCY, \
    FUEL_CELL_SOX_DEFAULT_EFFICIENCY


@dataclass
class FuelCell(PowerConverter):
    """Models a generic Hydrogen Fuel Cell."""
    def __init__(self,
                 name: str,
                 power_rating: float,
                 efficiency: float,
                 fuel: Fuel):
        super().__init__(name=name,
                         input_power=PowerType.CHEMICAL,
                         output_power=PowerType.ELECTRIC,
                         power_rating=power_rating,
                         efficiency=efficiency,
                         fuel=fuel,
                         reverse_efficiency=None)


@dataclass
class PEMembraneFC(FuelCell):
    """Models a Polymer Electrolyte Membrane Fuel Cell."""
    def __init__(self,
                 name: str,
                 power_rating: float):
        super().__init__(name=name,
                         power_rating=power_rating,
                         efficiency=FUEL_CELL_PEM_DEFAULT_EFFICIENCY,
                         fuel=HydrogenGas())


@dataclass
class DirectMethanolFC(FuelCell):
    """Models a Direct Methanol Fuel Cell."""
    def __init__(self,
                 name: str,
                 power_rating: float):
        super().__init__(name=name,
                         power_rating=power_rating,
                         efficiency=FUEL_CELL_DIR_METH_DEFAULT_EFFICIENCY,
                         fuel=Methanol())


@dataclass
class AlkalineFC(FuelCell):
    """Models an Alkaline Fuel Cell"""
    def __init__(self,
                 name: str,
                 power_rating: float):
        super().__init__(name=name,
                         power_rating=power_rating,
                         efficiency=FUEL_CELL_AFC_DEFAULT_EFFICIENCY,
                         fuel=HydrogenGas())


@dataclass
class PhAcidFC(FuelCell):
    """Models a Phosphoric Acid Fuel Cell."""
    def __init__(self,
                 name: str,
                 power_rating: float):
        super().__init__(name=name,
                         power_rating=power_rating,
                         efficiency=FUEL_CELL_PH_AC_DEFAULT_EFFICIENCY,
                         fuel=HydrogenGas())


@dataclass
class MoltenCarbonateFC(FuelCell):
    """Models a Molten Carbonate Fuel Cell."""
    def __init__(self,
                 name: str,
                 power_rating: float):
        super().__init__(name=name,
                         power_rating=power_rating,
                         efficiency=FUEL_CELL_MOL_CARB_DEFAULT_EFFICIENCY,
                         fuel=HydrogenGas())


@dataclass
class SolidOxideFC(FuelCell):
    """Models a Solid Oxide Fuel Cell."""
    def __init__(self,
                 name: str,
                 power_rating: float):
        super().__init__(name=name,
                         power_rating=power_rating,
                         efficiency=FUEL_CELL_SOX_DEFAULT_EFFICIENCY,
                         fuel=HydrogenGas())
