"""
This module carries out a minimalistic
simulation with a simple electric vehicle.
"""

from simulation.simulator import Simulator
from examples.battery_and_motor_only import minimalistic_em_vehicle

simulation = Simulator(time_steps=3,
                       delta_t=0.1,
                       control_signal=[1.0, 0.0, 1.0],
                       vehicle=minimalistic_em_vehicle)
simulation.simulate(load_torque=0.0)

print(simulation.history)
