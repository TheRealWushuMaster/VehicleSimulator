"""This module contains definition for the track where the vehicle rides."""

from dataclasses import dataclass, field
from math import exp, tan
from typing import Optional
from simulation.constants import AIR_DENSITY_SEA_LEVEL, REF_ALTITUDE


@dataclass
class TrackSection():
    """
    Base class for track sections.
    """
    horizontal_length: float

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
            return AIR_DENSITY_SEA_LEVEL * exp(-altitude/REF_ALTITUDE)
        return None


@dataclass
class Track():
    """
    This class contains the definition of the track where
    the vehicle will move on, defining its height and other
    parameters at each point.
    """
    sections: list[TrackSection]

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


@dataclass
class FlatSection(TrackSection):
    """
    Returns a flat track section.
    """
    _base_altitude: float=field(init=False)

    def altitude_value(self, d: float) -> float:
        return self._base_altitude

    def altitude_derivate(self, d: float) -> float:
        return 0.0


@dataclass
class SlopeSection(TrackSection):
    """
    Returns a sloped track section.
    """
    _slope: float   # In degrees
    _base_altitude: float=field(init=False)

    def altitude_value(self, d: float) -> float:
        return d*tan(self._slope) + self._base_altitude

    def altitude_derivate(self, d: float) -> float:
        return self._slope
