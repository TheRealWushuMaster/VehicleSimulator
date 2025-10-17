"""This module contains definition for the track where the vehicle rides."""

from __future__ import annotations
from dataclasses import dataclass
from math import tan, cos
from typing import Optional
from helpers.functions import degrees_to_radians, estimate_air_density
from simulation.materials import TrackMaterial


@dataclass
class TrackSection():
    """
    Base class for track sections.
    """
    horizontal_length: float
    material: TrackMaterial
    _base_altitude: float=0.0

    def altitude_value(self, d: float) -> Optional[float]:
        """
        Returns the altitude at the specified distance.
        """
        raise NotImplementedError

    def altitude_derivate(self, d: float) -> Optional[float]:
        """
        Returns the altitude derivate at the specified distance.
        """
        raise NotImplementedError

    def angle_degrees(self, d: float) -> Optional[float]:
        """
        Returns the angle (in degrees) at the specified point.
        """
        raise NotImplementedError

    def air_density(self, d: float) -> Optional[float]:
        """
        Returns the air density at the specified altitude.
        """
        altitude = self.altitude_value(d=d)
        if altitude is not None:
            return estimate_air_density(altitude=altitude)
        return None

    @property
    def base_altitude(self) -> float:
        """
        Returns the base altitude of the track section.
        """
        return self._base_altitude

    def set_base_altitude(self, base_altitude: float) -> None:
        """
        Sets a new base altitude for the track section.
        """
        self._base_altitude = base_altitude

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

    def advance_distance(self, d: float,
                         distance: float) -> Optional[SectionResult]:
        """
        Returns the new horizontal coordinate after
        advancing a certain distance over the track.
        """
        raise NotImplementedError


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
            base_alt = self.sections[i-1].altitude_value(d=self.sections[i-1].horizontal_length) - self.sections[i].altitude_value(d=0)  # type: ignore
            self.sections[i].set_base_altitude(base_altitude=base_alt)

    def find_section(self, d: float) -> Optional[SectionResult]:
        """
        Returns the section of the track corresponding
        to the distance passed as argument.
        """
        if not 0 <= d <= self.total_length:
            return None
        dist: float = 0.0
        for section in self.sections:
            if d <= dist + section.horizontal_length:
                return SectionResult(section=section,
                                     in_section_d=d-dist,
                                     total_d=d)
            dist += section.horizontal_length
        return None

    def altitude_value(self, d: float) -> Optional[float]:
        """
        Returns the altitude at the specified distance.
        """
        section_result = self.find_section(d=d)
        if section_result is not None:
            return section_result.section.altitude_value(d=section_result.in_section_d)
        return None

    def altitude_derivate(self, d: float) -> Optional[float]:
        """
        Returns the altitude derivate at the specified distance.
        """
        section_result = self.find_section(d=d)
        if section_result is not None:
            return section_result.section.altitude_derivate(d=section_result.in_section_d)
        return None

    def angle_degrees(self, d: float) -> Optional[float]:
        """
        Returns the angle (in degrees) at the specified point.
        """
        section_result = self.find_section(d=d)
        if section_result is not None:
            return section_result.section.angle_degrees(d=section_result.in_section_d)
        return None

    def air_density(self, d: float) -> Optional[float]:
        """
        Returns the air density at the specified distance.
        """
        section_result = self.find_section(d=d)
        if section_result is not None:
            return section_result.section.air_density(d=section_result.in_section_d)
        return None

    @property
    def total_length(self) -> float:
        """
        Returns the total length of the track.
        """
        return sum(section.horizontal_length for section in self.sections)

    def static_friction_coefficient(self, d: float) -> Optional[float]:
        """
        Returns the static friction coefficient
        at the specified distance.
        """
        section_result = self.find_section(d=d)
        if section_result is not None:
            return section_result.section.static_friction_coefficient
        return None

    def kinetic_friction_coefficient(self, d: float) -> Optional[float]:
        """
        Returns the kinetic friction coefficient
        at the specified distance.
        """
        section_result = self.find_section(d=d)
        if section_result is not None:
            return section_result.section.kinetic_friction_coefficient
        return None

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
                return None
            if index > 0:
                return self.sections[index - 1]
            return None
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
        return d * self.altitude_derivate(d=d) + self.base_altitude

    def altitude_derivate(self, d: float) -> float:
        return tan(degrees_to_radians(self._slope_degrees))

    def angle_degrees(self, d: float) -> Optional[float]:
        return self._slope_degrees

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
