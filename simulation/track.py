"""This module contains definition for the track where the vehicle rides."""

from dataclasses import dataclass
from math import tan
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

    def find_section(self, d: float) -> Optional[tuple[TrackSection, float]]:
        """
        Returns the section of the track corresponding
        to the distance passed as argument.
        """
        if not 0 <= d <= self.total_length:
            return None
        dist: float = 0.0
        for section in self.sections:
            if d <= dist + section.horizontal_length:
                return section, dist
            dist += section.horizontal_length
        return None

    def altitude_value(self, d: float) -> Optional[float]:
        """
        Returns the altitude at the specified distance.
        """
        section_dist = self.find_section(d=d)
        if section_dist is not None:
            return section_dist[0].altitude_value(d=d-section_dist[1])
        return None

    def altitude_derivate(self, d: float) -> Optional[float]:
        """
        Returns the altitude derivate at the specified distance.
        """
        section_dist = self.find_section(d=d)
        if section_dist is not None:
            return section_dist[0].altitude_derivate(d=d-section_dist[1])
        return None

    def air_density(self, d: float) -> Optional[float]:
        """
        Returns the air density at the specified distance.
        """
        section_dist = self.find_section(d=d)
        if section_dist is not None:
            return section_dist[0].air_density(d=d-section_dist[1])
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
        section_dist = self.find_section(d=d)
        if section_dist is not None:
            return section_dist[0].static_friction_coefficient
        return None

    def kinetic_friction_coefficient(self, d: float) -> Optional[float]:
        """
        Returns the kinetic friction coefficient
        at the specified distance.
        """
        section_dist = self.find_section(d=d)
        if section_dist is not None:
            return section_dist[0].kinetic_friction_coefficient
        return None


@dataclass
class SlopeSection(TrackSection):
    """
    Returns a sloped track section.
    """
    _slope: float=0.0

    def __init__(self, slope_degrees: float,
                 horizontal_length: float,
                 material: TrackMaterial) -> None:
        assert -90.0 < slope_degrees < 90.0
        super().__init__(horizontal_length=horizontal_length,
                         material=material)
        self._slope = tan(degrees_to_radians(slope_degrees))

    def altitude_value(self, d: float) -> float:
        return d*self._slope + self.base_altitude

    def altitude_derivate(self, d: float) -> float:
        return self._slope


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
