"""This module contains definition for the track where the vehicle rides."""

from __future__ import annotations
from dataclasses import dataclass
from math import tan, cos, sin
from typing import Optional
from components.drive_train import Wheel
from helpers.functions import degrees_to_radians, estimate_air_density, clamp
from simulation.materials import TrackMaterial


@dataclass
class TrackSection():
    """
    Base class for track sections.
    """
    horizontal_length: float
    material: TrackMaterial
    _base_altitude: float=0.0

    def altitude_value(self, d: float) -> float:
        """
        Returns the altitude at the specified distance.
        """
        raise NotImplementedError

    def altitude_derivate(self, d: float) -> float:
        """
        Returns the altitude derivate at the specified distance.
        """
        raise NotImplementedError

    def angle_degrees(self, d: float) -> float:
        """
        Returns the angle (in degrees) at the specified point.
        """
        raise NotImplementedError

    def air_density(self, d: float) -> float:
        """
        Returns the air density at the specified altitude.
        """
        altitude = self.altitude_value(d=d)
        return estimate_air_density(altitude=altitude)

    def advance_distance(self, d: float,
                         distance: float) -> Optional[SectionResult]:
        """
        Returns the new horizontal coordinate after
        advancing a certain distance over the track.
        """
        raise NotImplementedError

    def set_base_altitude(self, base_altitude: float) -> None:
        """
        Sets a new base altitude for the track section.
        """
        self._base_altitude = base_altitude

    @property
    def base_altitude(self) -> float:
        """
        Returns the base altitude of the track section.
        """
        return self._base_altitude

    @property
    def static_friction_coefficient(self) -> float:
        """
        Returns the static friction coefficient value.
        """
        return self.material.value[1]

    @property
    def kinetic_friction_coefficient(self) -> float:
        """
        Returns the kinetic friction coefficient value.
        """
        return self.material.value[2]

    @property
    def rolling_resistance_coefficient(self) -> float:
        """
            Returns the rolling resistance coefficient value.
            """
        return self.material.value[3]


@dataclass
class SectionResult():
    """
    Class used for storing results.
    """
    section: TrackSection
    in_section_d: float
    total_d: float
    remainder: float=0.0


@dataclass
class Track():
    """
    This class contains the full definition of a track where
    the vehicle will move on, defining its height and other
    parameters at each point.
    """
    sections: list[TrackSection]

    def __init__(self, sections: list[TrackSection],
                 base_altitude: float=0.0) -> None:
        self.sections = sections
        self._adjust_base_altitudes(base_altitude=base_altitude)

    def _adjust_base_altitudes(self, base_altitude: float) -> None:
        self.sections[0].set_base_altitude(base_altitude=base_altitude)
        for i in range(1, len(self.sections)):
            base_alt = self.sections[i-1].altitude_value(d=self.sections[i-1].horizontal_length) - self.sections[i].altitude_value(d=0)
            self.sections[i].set_base_altitude(base_altitude=base_alt)

    def find_section(self, d: float) -> SectionResult:
        """
        Returns the section of the track corresponding
        to the distance passed as argument.
        """
        if d < 0.0:
            return SectionResult(section=self.sections[0],
                                 in_section_d=d,
                                 total_d=d)
        if d > self.total_length:
            d_temp: float = sum(section.horizontal_length
                                for section in self.sections[:-1])
            return SectionResult(section=self.sections[-1],
                                 in_section_d=d - d_temp,
                                 total_d=d)
        dist: float = 0.0
        for section in self.sections:
            if d <= dist + section.horizontal_length:
                return SectionResult(section=section,
                                     in_section_d=d - dist,
                                     total_d=d)
            dist += section.horizontal_length
        return SectionResult(section=self.sections[-1],
                             in_section_d=d,
                             total_d=d)

    def altitude_value(self, d: float) -> float:
        """
        Returns the altitude at the specified distance.
        """
        section_result = self.find_section(d=d)
        return section_result.section.altitude_value(d=section_result.in_section_d)

    def altitude_derivate(self, d: float) -> float:
        """
        Returns the altitude derivate at the specified distance.
        """
        section_result = self.find_section(d=d)
        return section_result.section.altitude_derivate(d=section_result.in_section_d)

    def angle_degrees(self, d: float) -> float:
        """
        Returns the angle (in degrees) at the specified point.
        """
        section_result = self.find_section(d=d)
        return section_result.section.angle_degrees(d=section_result.in_section_d)

    def air_density(self, d: float) -> float:
        """
        Returns the air density at the specified distance.
        """
        section_result = self.find_section(d=d)
        return section_result.section.air_density(d=section_result.in_section_d)

    def static_friction_coefficient(self, d: float) -> float:
        """
        Returns the static friction coefficient
        at the specified distance.
        """
        section_result = self.find_section(d=d)
        return section_result.section.static_friction_coefficient

    def kinetic_friction_coefficient(self, d: float) -> float:
        """
        Returns the kinetic friction coefficient
        at the specified distance.
        """
        section_result = self.find_section(d=d)
        return section_result.section.kinetic_friction_coefficient

    def rolling_resistance_coefficient(self, d: float) -> float:
        """
        Returns the rolling resistance
        coefficient at the specified distance.
        """
        section_result = self.find_section(d=d)
        return section_result.section.rolling_resistance_coefficient

    def _which_section(self, section: TrackSection,
                       next_one: bool) -> Optional[TrackSection]:
        """
        Returns the next or previous track section.
        """
        try:
            index = self.sections.index(section)
            if next_one:
                if index < len(self.sections) - 1:
                    return self.sections[index + 1]
                return self.sections[-1]
            if index > 0:
                return self.sections[index - 1]
            return self.sections[0]
        except ValueError:
            return None

    def next_section(self, section: TrackSection) -> Optional[TrackSection]:
        """
        Returns the next track section.
        """
        return self._which_section(section=section,
                                   next_one=True)

    def previous_section(self, section: TrackSection) -> Optional[TrackSection]:
        """
        Returns the previous track section.
        """
        return self._which_section(section=section,
                                   next_one=False)

    def advance_distance(self, d: float,
                         distance: float) -> Optional[float]:
        """
        Calculates new positions after advancing
        a certain distance over the track.
        """
        section_result = self.find_section(d=d)
        if section_result is None:
            return None
        base_distance = section_result.total_d - section_result.in_section_d
        new_section_result = section_result.section.advance_distance(d=section_result.in_section_d,
                                                                     distance=distance)
        if new_section_result is None:
            return None
        if new_section_result.remainder == 0.0:
            return new_section_result.total_d + base_distance
        while new_section_result.remainder > 0.0:
            if distance > 0.0:
                new_section = self.next_section(section=new_section_result.section)
                base_distance += new_section_result.section.horizontal_length
            else:
                new_section = self.previous_section(section=new_section_result.section)
                base_distance -= new_section_result.section.horizontal_length
            if new_section is None:
                return None
            start_dist = 0.0 if distance > 0.0 else new_section.horizontal_length
            new_section_result = new_section.advance_distance(d=start_dist,
                                                              distance=new_section_result.remainder)
            if new_section_result is None:
                return None
        return new_section_result.in_section_d + base_distance

    def wheel_contact_point(self, d: float,
                            wheel: Wheel) -> float:
        """
        Returns the location of the contact point
        for a wheel whose center is located in `d`.
        """
        section_result = self.find_section(d=d)
        alpha = section_result.section.angle_degrees(d=section_result.in_section_d)
        next_section = self.next_section(section=section_result.section)
        assert next_section is not None
        beta = next_section.angle_degrees(d=0.0)
        assert beta is not None
        if beta >= alpha:
            critical_d = wheel.radius * (sin(alpha) + tan((beta-alpha)/2) * cos(alpha))
            if d + critical_d < section_result.section.horizontal_length:
                return section_result.total_d + wheel.radius * sin(alpha)
            return section_result.total_d + critical_d + wheel.radius * tan((beta-alpha)/2) * cos(beta)
        # If next section slope is less than the previous',
        # must define if the wheels stay in contact at all
        # times or if there is any jumping involved.
        return 0.0

    def wheel_center_height(self, d: float,
                            wheel: Wheel) -> Optional[float]:
        """
        Returns the height of the wheel's center when it's
        located at the horizontal coordinate `d`.
        """
        section_result = self.find_section(d=d)
        alt_alpha = section_result.section.altitude_value(d=d)
        alpha = section_result.section.angle_degrees(d=section_result.in_section_d)
        contact_point_d = section_result.in_section_d + wheel.radius * sin(alpha)
        if contact_point_d <= section_result.section.horizontal_length:
            # Contact point on same section
            alt = section_result.section.altitude_value(d=section_result.in_section_d)
            return alt + wheel.radius / cos(alpha)
        # Contact point on the next section
        next_section = self.next_section(section=section_result.section)
        if next_section is None:
            return None
        d_alpha = section_result.section.horizontal_length - d
        d_beta = section_result.section.horizontal_length - contact_point_d
        beta = next_section.angle_degrees(d=d_beta)
        return alt_alpha + d_alpha * tan(alpha) + d_beta * tan(beta) + wheel.radius * cos(beta)

    def in_same_section(self, d1: float,
                        d2: float) -> bool:
        """
        Returns if both distances are
        within the same track section.
        """
        
        if d1 < 0.0 and d2 < 0.0 or \
            d1 > self.total_length and d2 > self.total_length:
            return True
        # if (not 0.0 <= d1 <= self.total_length) or (not 0.0 <= d2 <= self.total_length):
        #     raise ValueError("Distances must both be within the total range of the track.")
        if self.find_section(d=d1) == self.find_section(d=d2):
            return True
        return False

    def rear_axle_location(self, front_axle_d: float,
                           axle_distance: float,
                           front_wheel: Wheel,
                           rear_wheel: Wheel) -> float:
        """
        Returns the horizontal coordinate of the rear axle
        as a function of the location of the front axle.
        """
        front_contact = self.wheel_contact_point(d=front_axle_d,
                                                 wheel=front_wheel)
        front_section = self.find_section(d=front_axle_d)
        angle = front_section.section.angle_degrees(d=front_section.in_section_d)
        rear_axle_d = front_section.in_section_d - axle_distance * cos(angle)
        rear_contact = self.wheel_contact_point(d=rear_axle_d,
                                                wheel=rear_wheel)
        if self.in_same_section(d1=front_contact,
                                d2=rear_contact):
            return front_axle_d - axle_distance * cos(angle)
        # Must add calculation when axles are in different sections
        return 0.0

    @property
    def total_length(self) -> float:
        """
        Returns the total length of the track.
        """
        return sum(section.horizontal_length for section in self.sections)


@dataclass
class SlopeSection(TrackSection):
    """
    Returns a sloped track section.
    """
    _slope_degrees: float=0.0

    def __init__(self, slope_degrees: float,
                 horizontal_length: float,
                 material: TrackMaterial) -> None:
        assert -90.0 < slope_degrees < 90.0
        super().__init__(horizontal_length=horizontal_length,
                         material=material)
        self._slope_degrees = slope_degrees

    def altitude_value(self, d: float) -> float:
        d = clamp(val=d,
                  min_val=0.0,
                  max_val=self.horizontal_length)
        return d * self.altitude_derivate(d=d) + self.base_altitude

    def altitude_derivate(self, d: float) -> float:
        if 0.0 <= d <= self.horizontal_length:
            return tan(degrees_to_radians(self._slope_degrees))
        return 0.0

    def angle_degrees(self, d: float) -> float:
        if 0.0 <= d <= self.horizontal_length:
            return self._slope_degrees
        return 0.0

    def advance_distance(self, d: float,
                         distance: float) -> Optional[SectionResult]:
        angle = self.angle_degrees(d=d)
        if angle is not None:
            distance_projected = abs(distance) * cos(degrees_to_radians(angle))
            if distance >= 0.0:
                d_max = (self.horizontal_length - d) / cos(degrees_to_radians(angle))
                if distance <= d_max:
                    return SectionResult(section=self,
                                         in_section_d=d+distance_projected,
                                         total_d=d+distance_projected)
                return SectionResult(section=self,
                                     in_section_d=-1.0,
                                     total_d=d,
                                     remainder=distance-d_max)
            d_max = d / cos(degrees_to_radians(angle))
            if abs(distance) <= d_max:
                return SectionResult(section=self,
                                     in_section_d=d-distance_projected,
                                     total_d=d-distance_projected)
            remaining_d = abs(distance) - d_max
            return SectionResult(section=self,
                                 in_section_d=-2.0,
                                 total_d=d,
                                 remainder=remaining_d)
        return None


@dataclass
class FlatSection(SlopeSection):
    """
    Returns a flat track section.
    """
    def __init__(self, horizontal_length: float,
                 material: TrackMaterial) -> None:
        super().__init__(slope_degrees=0.0,
                         horizontal_length=horizontal_length,
                         material=material)
