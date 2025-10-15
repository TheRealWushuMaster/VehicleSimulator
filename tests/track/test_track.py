"""This module contains test routines for the Track class."""

from math import tan
from helpers.functions import degrees_to_radians, estimate_air_density
from simulation.track import Track, TrackSection, \
    SlopeSection, FlatSection

length: float = 5.0
slope_degrees: float = 30.0

def create_flat_section(section_length: float=length) -> FlatSection:
    return FlatSection(horizontal_length=section_length)

def create_slope_section(section_slope_degrees: float=slope_degrees,
                         section_length: float=length) -> SlopeSection:
    return SlopeSection(slope_degrees=section_slope_degrees,
                        horizontal_length=section_length)

def create_test_track() -> Track:
    flat_section1: FlatSection = create_flat_section()
    flat_section2: FlatSection = create_flat_section()
    slope_section: SlopeSection = create_slope_section()
    sections_list: list[TrackSection] = [flat_section1, slope_section, flat_section2]
    test_track = Track(sections=sections_list)
    return test_track

def test_create_track() -> None:
    test_track = create_test_track()
    assert isinstance(test_track, Track)

def test_track_altitude() -> None:
    test_track = create_test_track()
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
    test_track = create_test_track()
    for d in range(int(test_track.total_length)):
        altitude = test_track.altitude_value(d=d)
        assert altitude is not None
        density = test_track.air_density(d=d)
        assert density == estimate_air_density(altitude=altitude)
