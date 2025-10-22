"""
This module contains definitions of
constants for use in the project.
"""

from math import pi

# Miscellaneous
EPSILON: float = 0.001
DEFAULT_TEMPERATURE: float = 300.0
DEFAULT_PRECISION: int = 8
DRIVE_TRAIN_ID: str = "DriveTrain"
DRIVE_TRAIN_INPUT_ID: str = "DriveTrainInput"
GRAVITY: float = 9.81   # m/s²
AIR_DENSITY_AT_SEA_LEVEL: float = 1.225  # kg/m³
REFERENCE_ALTITUDE: float = 8_500.0      # For use in air density calculations

# Friction coefficients
KINETIC_PERCENTAGE: float = 0.8
STATIC_FRICTION_COEFFICIENTS: dict[str, float] = {"Dry asphalt": 0.80,
                                                  "Wet asphalt": 0.50,
                                                  "Icy asphalt": 0.15,
                                                  "Dry concrete": 0.725,
                                                  "Wet concrete": 0.575,
                                                  "Loose gravel": 0.50,
                                                  "Compacted gravel": 0.60,
                                                  "Dry dirt": 0.60,
                                                  "Wet dirt": 0.40,
                                                  "Hard-packed dirt": 0.70}
KINETIC_FRICTION_COEFFICIENTS: dict[str, float] = {}
for key, value in STATIC_FRICTION_COEFFICIENTS.items():
    KINETIC_FRICTION_COEFFICIENTS[key] = round(KINETIC_PERCENTAGE * value, DEFAULT_PRECISION)

# Energy conversion
KWH_TO_JOULES: float = 3.6e6
WH_TO_JOULES: float = KWH_TO_JOULES / 1_000
JOULES_TO_KWH: float = 1 / KWH_TO_JOULES
JOULES_TO_WH: float = 1 / WH_TO_JOULES

# Power conversion
HP_TO_W: float = 745.7
HP_TO_KW: float = HP_TO_W / 1_000
W_TO_HP: float = 1 / HP_TO_W
KW_TO_HP: float = 1 / HP_TO_KW

# RPM and Angular Velocity conversions
RPM_TO_ANG_VEL: float = 2 * pi / 60
ANG_VEL_TO_RPM: float = 1 / RPM_TO_ANG_VEL

# Volume conversion
CUBIC_METERS_TO_LTS: float = 1_000
LTS_TO_CUBIC_METERS: float = 1 / CUBIC_METERS_TO_LTS

# Fuel energy densities (J/kg)
ENERGY_DENSITY_GASOLINE: float = 44.4e6
ENERGY_DENSITY_DIESEL: float = 45.4e6
ENERGY_DENSITY_HYDROGEN: float = 130e6
ENERGY_DENSITY_ETHANOL: float = 26.8e6
ENERGY_DENSITY_METHANOL: float = 22.6e6
ENERGY_DENSITY_BIODIESEL: float = 37.8e6
ENERGY_DENSITY_METHANE: float = 53e6

# Fuel mass densities (kg/m^3)
DENSITY_GASOLINE: float = 742.9
DENSITY_DIESEL: float = 830.0
DENSITY_ETHANOL: float = 789.0
DENSITY_METHANOL: float = 791.3
DENSITY_BIODIESEL: float = 874.7
DENSITY_HYDROGEN_LIQUID: float = 70.85

BATTERY_EFFICIENCY_DEFAULT: float = 0.95
HYDROGEN_FUEL_CELL_EFFICIENCY_DEFAULT: float = 0.60

# Engine and motor default efficiencies
ELECTRIC_MOTOR_DEFAULT_EFFICIENCY: float = 0.93
GASOLINE_ENGINE_DEFAULT_EFFICIENCY: float = 0.30
DIESEL_ENGINE_DEFAULT_EFFICIENCY: float = 0.40
HYDROGEN_ENGINE_DEFAULT_EFFICIENCY: float = 0.30
ETHANOL_ENGINE_DEFAULT_EFFICIENCY: float = 0.27
METHANOL_ENGINE_DEFAULT_EFFICIENCY: float = 0.30
BIODIESEL_ENGINE_DEFAULT_EFFICIENCY: float = 0.35
ELECTRIC_GENERATOR_DEFAULT_EFFICIENCY: float = 0.90

ELECTRIC_MOTOR_DEFAULT_MAXIMUM_EFFICIENCY: float = 0.95
GASOLINE_ENGINE_DEFAULT_MAXIMUM_EFFICIENCY: float = 0.30
DIESEL_ENGINE_DEFAULT_MAXIMUM_EFFICIENCY: float = 0.41
HYDROGEN_ENGINE_DEFAULT_MAXIMUM_EFFICIENCY: float = 0.30
ETHANOL_ENGINE_DEFAULT_MAXIMUM_EFFICIENCY: float = 0.27
METHANOL_ENGINE_DEFAULT_MAXIMUM_EFFICIENCY: float = 0.3
BIODIESEL_ENGINE_DEFAULT_MAXIMUM_EFFICIENCY: float = 0.38
ELECTRIC_GENERATOR_DEFAULT_MAXIMUM_EFFICIENCY: float = 0.90

ELECTRIC_MOTOR_DEFAULT_MINIMUM_EFFICIENCY: float = 0.70
GASOLINE_ENGINE_DEFAULT_MINIMUM_EFFICIENCY: float = 0.10
DIESEL_ENGINE_DEFAULT_MINIMUM_EFFICIENCY: float = 0.15
HYDROGEN_ENGINE_DEFAULT_MINIMUM_EFFICIENCY: float = 0.10
ETHANOL_ENGINE_DEFAULT_MINIMUM_EFFICIENCY: float = 0.10
METHANOL_ENGINE_DEFAULT_MINIMUM_EFFICIENCY: float = 0.10
BIODIESEL_ENGINE_DEFAULT_MINIMUM_EFFICIENCY: float = 0.20
ELECTRIC_GENERATOR_DEFAULT_MINIMUM_EFFICIENCY: float = 0.70

# Battery state of health
BATTERY_DEFAULT_SOH: float = 1.0

# Gravimetric energy density for battery types (Wh/kg, converted to J/kg)
BATTERY_Al_AIR_ENERGY_DENSITY: float = 1300.0 * WH_TO_JOULES
BATTERY_Pb_ACID_ENERGY_DENSITY: float = 40.0 * WH_TO_JOULES
BATTERY_LiCo_ENERGY_DENSITY: float = 170.0 * WH_TO_JOULES
BATTERY_LiMn_ENERGY_DENSITY: float = 117.5 * WH_TO_JOULES
BATTERY_LiPh_ENERGY_DENSITY: float = 105.0 * WH_TO_JOULES
BATTERY_LiPo_ENERGY_DENSITY: float = 180.0 * WH_TO_JOULES
BATTERY_NiCd_ENERGY_DENSITY: float = 68.5 * WH_TO_JOULES
BATTERY_NiMH_ENERGY_DENSITY: float = 90.0 * WH_TO_JOULES
BATTERY_SOLID_STATE_ENERGY_DENSITY: float = 350.0 * WH_TO_JOULES

# Fuel cell efficiencies
FUEL_CELL_PEM_DEFAULT_EFFICIENCY: float = 0.60
FUEL_CELL_DIR_METH_DEFAULT_EFFICIENCY: float = 0.25
FUEL_CELL_AFC_DEFAULT_EFFICIENCY: float = 0.65
FUEL_CELL_PH_AC_DEFAULT_EFFICIENCY: float = 0.55
FUEL_CELL_MOL_CARB_DEFAULT_EFFICIENCY: float = 0.55
FUEL_CELL_SOX_DEFAULT_EFFICIENCY: float = 0.62
