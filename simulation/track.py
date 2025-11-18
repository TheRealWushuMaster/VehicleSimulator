"""This module contains definition for the track where the vehicle rides."""

from __future__ import annotations
from dataclasses import dataclass
from math import tan, atan, cos, sin, asin, sqrt
from typing import Optional
from components.drive_train import Wheel
from components.vehicle import Vehicle
from helpers.functions import degrees_to_radians, radians_to_degrees, \
    estimate_air_density, clamp
from simulation.constants import GRAVITY, MINIMUM_V_STATIC_FRICTION
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

    def angle_radians(self, d: float) -> float:
        """
        Returns the angle (in radians) at the specified point.
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
class AxleLoad():
    """
    Contains loads on each axle.
    """
    rolling_resistance_per_wheel: float=0.0
    gradient_force_per_wheel: float=0.0
    max_friction_force_per_wheel: float=0.0
    _num_wheels: int=0
    _wheel_radius: float=0.0

    @property
    def num_wheels(self) -> int:
        """
        Returns the number of wheels.
        """
        return self._num_wheels

    @property
    def wheel_radius(self) -> float:
        """
        Returns the number of wheels.
        """
        return self._wheel_radius

    @property
    def total_torque(self) -> float:
        """
        Returns the sum of all loads on the axle.
        """
        return (self.rolling_resistance_per_wheel + self.gradient_force_per_wheel) * \
            self._num_wheels * self._wheel_radius


@dataclass
class LoadResult():
    """
    Class used for storing load torque results.
    """
    front_axle: AxleLoad
    rear_axle: AxleLoad
    drag_force: float

    @property
    def total_load_torque(self) -> float:
        """
        Returns the sum of all load torques on the vehicle.
        """
        return self.front_axle.total_torque + self.rear_axle.total_torque


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

    def angle_radians(self, d: float) -> float:
        """
        Returns the angle (in radians) at the specified point.
        """
        section_result = self.find_section(d=d)
        return section_result.section.angle_radians(d=section_result.in_section_d)

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
        alpha = section_result.section.angle_radians(d=section_result.in_section_d)
        next_section = self.next_section(section=section_result.section)
        assert next_section is not None
        beta = next_section.angle_radians(d=0.0)
        assert beta is not None
        if beta >= alpha:
            d_alpha = wheel.radius * tan((beta-alpha)/2) * cos(alpha)
            if section_result.in_section_d + wheel.radius * sin(alpha) + d_alpha <= \
                section_result.section.horizontal_length:
                return section_result.total_d + wheel.radius * sin(alpha)
            #return section_result.total_d + critical_d + wheel.radius * tan((beta-alpha)/2) * cos(beta)
            return section_result.total_d + wheel.radius * sin(beta)
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
        alpha = section_result.section.angle_radians(d=section_result.in_section_d)
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
        beta = next_section.angle_radians(d=d_beta)
        return alt_alpha + d_alpha * tan(alpha) + d_beta * tan(beta) + wheel.radius * cos(beta)

    def in_same_section(self, d1: float,
                        d2: float) -> bool:
        """
        Returns if both distances are
        within the same track section.
        """
        if self.find_section(d=d1).section == self.find_section(d=d2).section:
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
        alpha = front_section.section.angle_radians(d=front_section.in_section_d)
        gamma = asin((front_wheel.radius - rear_wheel.radius) / axle_distance)
        rear_contact = front_contact - axle_distance * cos(alpha + gamma) + \
            sin(alpha) * (front_wheel.radius - rear_wheel.radius)
        if self.in_same_section(d1=front_contact,
                                d2=rear_contact):
            return front_axle_d - axle_distance * cos(alpha + gamma)
        front_section = self.find_section(d=front_contact)
        d_beta = front_section.in_section_d
        beta = front_section.section.angle_radians(d=d_beta)
        rear_section = self.previous_section(section=front_section.section)
        assert rear_section is not None
        alpha = rear_section.angle_radians(d=0.0)
        delta_h_beta = front_section.section.altitude_value(d=d_beta) - \
            front_section.section.altitude_value(d=0.0)
        k1 = d_beta + rear_wheel.radius * sin(alpha) - front_wheel.radius * sin(beta)
        k2 = delta_h_beta + front_wheel.radius * cos(beta) - rear_wheel.radius * cos(alpha)
        a = 1 + tan(alpha)**2
        b = 2 * (k1 + k2 * tan(alpha))
        c = k1**2 + k2**2 - axle_distance**2
        determinant = b**2 - 4 * a * c
        assert determinant >= 0.0
        d_alpha = (-b + sqrt(determinant))/2/a
        return front_section.total_d - d_beta - d_alpha - rear_wheel.radius * sin(alpha)

    def get_wheel_contact_points(self, vehicle: Vehicle,
                                 front_axle_d: Optional[float]=None
                                 ) -> tuple[float, float]:
        """
        Returns front and rear wheel contact
        point horizontal coordinates.
        """
        if front_axle_d is None:
            front_axle_d = vehicle.snapshot.state.position
        front_contact = self.wheel_contact_point(d=front_axle_d,
                                                 wheel=vehicle.drive_train.front_axle.wheel)
        rear_d = self.rear_axle_location(front_axle_d=front_axle_d,
                                         axle_distance=vehicle.body.axle_distance,
                                         front_wheel=vehicle.drive_train.front_axle.wheel,
                                         rear_wheel=vehicle.drive_train.rear_axle.wheel)
        rear_contact = self.wheel_contact_point(d=rear_d,
                                                wheel=vehicle.drive_train.rear_axle.wheel)
        return front_contact, rear_contact

    def load_on_vehicle(self, vehicle: Vehicle,
                        can_slip: bool,
                        front_axle_d: Optional[float]=None) -> LoadResult:
        """
        Returns front and rear load torques.
        """
        if front_axle_d is None:
            front_axle_d = vehicle.snapshot.state.position
        front_contact, rear_contact = self.get_wheel_contact_points(vehicle=vehicle,
                                                                    front_axle_d=front_axle_d)
        vehicle_weight = vehicle.total_mass * GRAVITY
        rear_weight = vehicle_weight * vehicle.body.cg_location
        rear_weight_per_wheel = rear_weight / vehicle.drive_train.rear_axle.num_wheels
        front_weight = vehicle_weight - rear_weight
        front_weight_per_wheel = front_weight / vehicle.drive_train.front_axle.num_wheels
        front_angle = self.angle_radians(d=front_contact)
        rear_angle = self.angle_radians(d=rear_contact)
        front_normal_per_wheel = front_weight_per_wheel * cos(front_angle)
        front_force_gradient_per_wheel = front_weight_per_wheel * sin(front_angle) # Positive means load, negative means assist
        rear_normal_per_wheel = rear_weight_per_wheel * cos(rear_angle)
        rear_force_gradient_per_wheel = rear_weight_per_wheel * sin(rear_angle) # Positive means load, negative means assist
        front_force_rolling_per_wheel = self.rolling_resistance_coefficient(
            d=front_contact) * front_normal_per_wheel
        rear_force_rolling_per_wheel = self.rolling_resistance_coefficient(
            d=rear_contact) * rear_normal_per_wheel
        if abs(vehicle.snapshot.state.velocity) <= MINIMUM_V_STATIC_FRICTION:
            # Assume vehicle is stopped
            mu_front = self.static_friction_coefficient(d=front_contact)
            mu_rear = self.static_friction_coefficient(d=rear_contact)
        else:
            # Assume vehicle is in motion
            mu_front = self.kinetic_friction_coefficient(d=front_contact)
            mu_rear = self.kinetic_friction_coefficient(d=rear_contact)
        front_max_traction_torque = mu_front * front_normal_per_wheel * \
            vehicle.drive_train.front_axle.wheel.radius
        rear_max_traction_torque = mu_rear * rear_normal_per_wheel * \
            vehicle.drive_train.rear_axle.wheel.radius
        drag_force = self.drag_force(vehicle=vehicle,
                                     front_axle_d=front_axle_d)
        if not can_slip:
            # front_load_force_per_wheel = front_force_rolling_per_wheel + \
            #     front_force_gradient_per_wheel
            # front_load_torque_per_wheel = front_load_force_per_wheel * \
            #     vehicle.drive_train.front_axle.wheel.radius
            # rear_load_force_per_wheel = rear_force_rolling_per_wheel + \
            #     rear_force_gradient_per_wheel
            # rear_load_torque_per_wheel = rear_load_force_per_wheel * \
            #     vehicle.drive_train.rear_axle.wheel.radius
            return LoadResult(front_axle=AxleLoad(rolling_resistance_per_wheel=front_force_rolling_per_wheel,
                                                  gradient_force_per_wheel=front_force_gradient_per_wheel,
                                                  max_friction_force_per_wheel=front_max_traction_torque,
                                                  _num_wheels=vehicle.drive_train.front_axle.num_wheels,
                                                  _wheel_radius=vehicle.drive_train.front_axle.wheel.radius),
                              rear_axle=AxleLoad(rolling_resistance_per_wheel=rear_force_rolling_per_wheel,
                                                 gradient_force_per_wheel=rear_force_gradient_per_wheel,
                                                 max_friction_force_per_wheel=rear_max_traction_torque,
                                                 _num_wheels=vehicle.drive_train.rear_axle.num_wheels,
                                                 _wheel_radius=vehicle.drive_train.rear_axle.wheel.radius),
                              drag_force=drag_force)
        # When wheels can slip, must verify tractive torque
        # in relation to the maximum value set by the track.
        return LoadResult(front_axle=AxleLoad(),
                          rear_axle=AxleLoad(),
                          drag_force=0.0)

    def wheels_in_same_section(self, vehicle: Vehicle,
                               front_axle_d: Optional[float]=None,
                               ) -> Optional[bool]:
        """
        Returns if both axles lie within the same track section.
        """
        if front_axle_d is None:
            front_axle_d = vehicle.snapshot.state.position
        section_result = self.find_section(d=front_axle_d)
        section_d_start = section_result.total_d - section_result.in_section_d
        beta = section_result.section.angle_degrees(d=section_result.in_section_d)
        front_contact = self.wheel_contact_point(d=section_result.in_section_d,
                                                 wheel=vehicle.drive_train.front_axle.wheel)
        if front_contact - section_d_start - vehicle.body.axle_distance * cos(beta) >= 0.0:
            return True
        return False

    def vehicle_angle(self, vehicle: Vehicle,
                      front_axle_d: Optional[float]=None,
                      in_radians: bool=True) -> float:
        """
        Returns the angle of the vehicle as the angle between
        the horizontal and the line between both axles.
        """
        if front_axle_d is None:
            front_axle_d = vehicle.snapshot.state.position
        if self.wheels_in_same_section(vehicle=vehicle,
                                       front_axle_d=front_axle_d):
            section_result = self.find_section(
                d=vehicle.snapshot.state.position)
            front_contact = self.wheel_contact_point(d=section_result.in_section_d,
                                                     wheel=vehicle.drive_train.front_axle.wheel)
            rads = section_result.section.angle_radians(d=front_contact)
        else:
            rear_axle_d = self.rear_axle_location(front_axle_d=front_axle_d,
                                                  axle_distance=vehicle.body.axle_distance,
                                                  front_wheel=vehicle.drive_train.front_axle.wheel,
                                                  rear_wheel=vehicle.drive_train.rear_axle.wheel)
            front_h = self.wheel_center_height(d=front_axle_d,
                                               wheel=vehicle.drive_train.front_axle.wheel)
            rear_h = self.wheel_center_height(d=rear_axle_d,
                                              wheel=vehicle.drive_train.rear_axle.wheel)
            assert front_h is not None
            assert rear_h is not None
            rads = atan((front_h - rear_h)/(front_axle_d - rear_axle_d))
        if in_radians:
            return rads
        return radians_to_degrees(angle_radians=rads)

    def drag_force(self, vehicle: Vehicle,
                   front_axle_d: Optional[float]=None) -> float:
        """
        Returns the value of aerodynamic drag force.
        """
        if front_axle_d is None:
            front_axle_d = vehicle.snapshot.state.position
        front_area = vehicle.body.front_area
        density = self.air_density(d=front_axle_d)
        velocity = vehicle.snapshot.state.velocity
        drag_coefficient = vehicle.body.drag_coefficient
        return 0.5 * drag_coefficient * front_area * density * velocity**2

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

    def angle_radians(self, d: float) -> float:
        return degrees_to_radians(angle_degrees=self.angle_degrees(d=d))

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
