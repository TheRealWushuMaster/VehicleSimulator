"""This module contains routines for generating example tracks."""

from simulation.materials import TrackMaterial
from simulation.track import Track, FlatSection, SlopeSection

def return_flat_track(length: float,
                      material: TrackMaterial=TrackMaterial.DRY_ASPHALT
                      ) -> Track:
    """
    Returns a simple flat track of specified
    length and friction coefficient.
    """
    section = FlatSection(horizontal_length=length,
                          material=material)
    return Track(sections=[section])

def return_slope_track(length: float,
                       slope_degrees: float,
                       material: TrackMaterial=TrackMaterial.DRY_ASPHALT
                       ) -> Track:
    """
    Returns a simple slope track of specified
    length, friction, coefficient, and slope.
    """
    section = SlopeSection(slope_degrees=slope_degrees,
                           horizontal_length=length,
                           material=material)
    return Track(sections=[section])

def return_flat_slope_flat_track(length1: float,
                                 length2: float,
                                 length3: float,
                                 slope_degrees: float,
                                 material: TrackMaterial=TrackMaterial.DRY_ASPHALT
                                 ) -> Track:
    """
    Returns a track with two flats and a slope.
    """
    section1 = FlatSection(horizontal_length=length1,
                           material=material)
    section2 = SlopeSection(slope_degrees=slope_degrees,
                            horizontal_length=length2,
                            material=material)
    section3 = FlatSection(horizontal_length=length3,
                           material=material)
    return Track(sections=[section1, section2, section3])
