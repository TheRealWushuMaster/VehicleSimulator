"""This module contains routines for testing creation of the vehicle's body."""

from components.body import Body

def test_body():
    body = Body(mass=1_500.0,
                occupants_mass=160.0,
                height=1.6,
                length=3.5,
                front_area=2.4,
                rear_area=2.4,
                axle_distance=1.5)
    assert isinstance(body, Body)
