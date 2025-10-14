"""
This module carries out a minimalistic
simulation with a simple electric vehicle.
"""

from simulation.results import ResultsManager
from simulation.simulator import Simulator
from examples.battery_and_motor_only import minimalistic_em_vehicle

time_steps: int = 300
control_signal: list[float] = [1.0] * time_steps

simulation = Simulator(name="minimalistic_sim",
                       time_steps=time_steps,
                       delta_t=0.1,
                       control_signal=control_signal,
                       vehicle=minimalistic_em_vehicle,
                       precision=8)
simulation.simulate(load_torque=100.0)

results = ResultsManager(simulation=simulation)

results.plot_all()
results.save_csv()
