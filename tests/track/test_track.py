"""This module contains test routines for the Track class."""

from math import tan, cos
import matplotlib.pyplot as plt
from components.drive_train import Wheel
from examples.battery_and_motor_only import minimalistic_em_vehicle
from helpers.functions import degrees_to_radians, estimate_air_density
from simulation.materials import TrackMaterial
from simulation.track import Track, TrackSection, \
    SlopeSection, FlatSection

length: float = 5.0
slope_degrees: float = 30.0

wheel: Wheel = Wheel(radius=0.3,
                     width=0.15,
                     mass=30.0,
                     air_pressure=1.0)

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

def test_advance_distance() -> None:
    for material in TrackMaterial:
        test_track = create_test_track(material=material)
        d_deg = cos(degrees_to_radians(slope_degrees))
        for d, c in (3.0, 5.0+d_deg), (8.0, 10+(3-2/d_deg)) , (11.0, 14.0):
            new_d = test_track.advance_distance(d=d,
                                                distance=3.0)
            assert new_d == c

def test_contact_point() -> None:
    # section_1 = create_slope_section(material=TrackMaterial.DRY_ASPHALT,
    #                                  section_slope_degrees=10.0,
    #                                  section_length=10)
    section_1 = create_flat_section(material=TrackMaterial.DRY_ASPHALT,
                                    section_length=10)
    section_2 = create_slope_section(material=TrackMaterial.DRY_ASPHALT,
                                     section_slope_degrees=30.0,
                                     section_length=10)
    track = Track(sections=[section_1, section_2])
    front_axle_ds: list[float] = []
    rear_axle_ds: list[float] = []
    front_contacts: list[float] = []
    rear_contacts: list[float] = []
    for d in range(int(track.total_length*10)):
        front_axle_d = d / 10.0
        front_contact = track.wheel_contact_point(d=front_axle_d,
                                                  wheel=minimalistic_em_vehicle.drive_train.front_axle.wheel)
        rear_axle_d = track.rear_axle_location(front_axle_d=front_axle_d,
                                               axle_distance=minimalistic_em_vehicle.body.axle_distance,
                                               front_wheel=minimalistic_em_vehicle.drive_train.front_axle.wheel,
                                               rear_wheel=minimalistic_em_vehicle.drive_train.rear_axle.wheel)
        rear_contact = track.wheel_contact_point(d=rear_axle_d,
                                                 wheel=minimalistic_em_vehicle.drive_train.rear_axle.wheel)
        front_axle_ds.append(front_axle_d)
        rear_axle_ds.append(rear_axle_d)
        front_contacts.append(front_contact)
        rear_contacts.append(rear_contact)
    plt.plot(front_axle_ds, label="Front axle")
    plt.plot(rear_axle_ds, label="Rear axle")
    plt.plot(front_contacts, label="Front contacts")
    plt.plot(rear_contacts, label="Rear contacts")
    plt.grid(linestyle=":")
    plt.legend()
    plt.show()
