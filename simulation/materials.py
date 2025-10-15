"""This module contains definitions for track materials."""

from enum import Enum
from simulation.constants import  STATIC_FRICTION_COEFFICIENTS, \
    KINETIC_FRICTION_COEFFICIENTS


class TrackMaterial(Enum):
    """
    Materials for use when simulating tracks.
    """
    DRY_ASPHALT = ("Dry asphalt",
                   STATIC_FRICTION_COEFFICIENTS["Dry asphalt"],
                   KINETIC_FRICTION_COEFFICIENTS["Dry asphalt"])
    WET_ASPHALT = ("Wet asphalt",
                   STATIC_FRICTION_COEFFICIENTS["Wet asphalt"],
                   KINETIC_FRICTION_COEFFICIENTS["Wet asphalt"])
    ICY_ASPHALT = ("Icy asphalt",
                   STATIC_FRICTION_COEFFICIENTS["Icy asphalt"],
                   KINETIC_FRICTION_COEFFICIENTS["Icy asphalt"])
    DRY_CONCRETE = ("Dry concrete",
                    STATIC_FRICTION_COEFFICIENTS["Dry concrete"],
                    KINETIC_FRICTION_COEFFICIENTS["Dry concrete"])
    WET_CONCRETE = ("Wet concrete",
                    STATIC_FRICTION_COEFFICIENTS["Wet concrete"],
                    KINETIC_FRICTION_COEFFICIENTS["Wet concrete"])
    LOOSE_GRAVEL = ("Loose gravel",
                    STATIC_FRICTION_COEFFICIENTS["Loose gravel"],
                    KINETIC_FRICTION_COEFFICIENTS["Loose gravel"])
    COMPACTED_GRAVEL = ("Compacted gravel",
                        STATIC_FRICTION_COEFFICIENTS["Compacted gravel"],
                        KINETIC_FRICTION_COEFFICIENTS["Compacted gravel"])
    DRY_DIRT = ("Dry dirt",
                STATIC_FRICTION_COEFFICIENTS["Dry dirt"],
                KINETIC_FRICTION_COEFFICIENTS["Dry dirt"])
    WET_DIRT = ("Wet dirt",
                STATIC_FRICTION_COEFFICIENTS["Wet dirt"],
                KINETIC_FRICTION_COEFFICIENTS["Wet dirt"])
    HARD_PACKED_DIRT = ("Hard-packed dirt",
                        STATIC_FRICTION_COEFFICIENTS["Hard-packed dirt"],
                        KINETIC_FRICTION_COEFFICIENTS["Hard-packed dirt"])
