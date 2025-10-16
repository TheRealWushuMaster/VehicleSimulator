"""This module contains test routines for the Track class."""

from math import tan
from helpers.functions import degrees_to_radians, estimate_air_density
from simulation.materials import TrackMaterial
from simulation.track import Track, TrackSection, \
    SlopeSection, FlatSection

length: float = 5.0
slope_degrees: float = 30.0

def create_flat_section(material: TrackMaterial,
                        section_length: float=length) -> FlatSection:
    return FlatSection(horizontal_length=section_length,
                       material=material)

def create_slope_section(material: TrackMaterial,
                         section_slope_degrees: float=slope_degrees,
                         section_length: float=length) -> SlopeSection:
    return SlopeSection(slope_degrees=section_slope_degrees,
                        horizontal_length=section_length,
                        material=material)

def create_test_track(material: TrackMaterial) -> Track:
    flat_section1: FlatSection = create_flat_section(material=material)
    flat_section2: FlatSection = create_flat_section(material=material)
    slope_section: SlopeSection = create_slope_section(material=material)
    sections_list: list[TrackSection] = [flat_section1, slope_section, flat_section2]
    test_track = Track(sections=sections_list)
    return test_track

def test_create_track() -> None:
    for material in TrackMaterial:
        test_track = create_test_track(material=material)
        assert isinstance(test_track, Track)

def test_track_altitude() -> None:
    for material in TrackMaterial:
        test_track = create_test_track(material=material)
        for d in range(int(test_track.total_length)):
            altitude = test_track.altitude_value(d=d)
            if 0 <= d < length:
                assert altitude == 0.0
            elif length <= d < 2*length:
                assert altitude == (
                    d-length) * tan(degrees_to_radians(angle_degrees=slope_degrees))
            else:
                assert altitude == length * \
                    tan(degrees_to_radians(angle_degrees=slope_degrees))

def test_track_air_density() -> None:
    for material in TrackMaterial:
        test_track = create_test_track(material=material)
        for d in range(int(test_track.total_length)):
            altitude = test_track.altitude_value(d=d)
            assert altitude is not None
            density = test_track.air_density(d=d)
            assert density == estimate_air_density(altitude=altitude)

def test_static_friction_coefficient() -> None:
    for material in TrackMaterial:
        test_track = create_test_track(material=material)
        for d in range(int(test_track.total_length)):
            coefficient = test_track.static_friction_coefficient(d=d)
            assert coefficient == material.value[1]

def test_kinetic_friction_coefficient() -> None:
    for material in TrackMaterial:
        test_track = create_test_track(material=material)
        for d in range(int(test_track.total_length)):
            coefficient = test_track.kinetic_friction_coefficient(d=d)
            assert coefficient == material.value[2]

def test_track_angle() -> None:
    for material in TrackMaterial:
        test_track = create_test_track(material=material)
        for d in range(int(test_track.total_length)):
            d_p = d + 0.1
            angle = test_track.angle_degrees(d=d_p)
            if 0 <= d_p < length:
                assert angle == 0.0
            elif length <= d_p < 2*length:
                assert angle == slope_degrees
            else:
                assert angle == 0.0
