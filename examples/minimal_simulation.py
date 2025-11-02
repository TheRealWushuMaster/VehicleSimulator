"""
This module carries out a minimalistic
simulation with a simple electric vehicle.
"""

from simulation.results import ResultsManager
from simulation.simulator import Simulator
from examples.battery_and_motor_only import minimalistic_em_vehicle
from examples.example_tracks import return_flat_track

time_steps: int = 200
throttle: list[float] = [0.5] * time_steps
brake: list[float] = [0.0] * time_steps

flat_track = return_flat_track(length=200.0)

simulation = Simulator(name="minimalistic_sim",
                       time_steps=time_steps,
                       delta_t=0.1,
                       throttle_signal=throttle,
                       brake_signal=brake,
                       vehicle=minimalistic_em_vehicle,
                       track=flat_track,
                       precision=8,
                       can_slip=False)
simulation.simulate()

results = ResultsManager(simulation=simulation)

results.plot_all()
results.save_csv()
