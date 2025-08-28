"""
This module carries out a minimalistic
simulation with a simple electric vehicle.
"""

import matplotlib.pyplot as plt
from simulation.simulator import Simulator
from examples.battery_and_motor_only import minimalistic_em_vehicle

time_steps: int = 800
control_signal: list[float] = [1.0] * time_steps

simulation = Simulator(time_steps=time_steps,
                       delta_t=0.1,
                       control_signal=control_signal,
                       vehicle=minimalistic_em_vehicle)
motor_id = minimalistic_em_vehicle.converters[0].id
simulation.simulate(load_torque=100.0)


motor_hist = simulation.history[motor_id]
motor_hist_states = motor_hist["states"]

motor_rpms: list[float] = []
motor_power_in: list[float] = []
motor_power_out: list[float] = []
motor_torque_out: list[float] = []
for state in motor_hist_states:
    motor_rpms.append(state.output.rpm)
    motor_power_in.append(state.input.power)
    motor_power_out.append(state.output.power)
    motor_torque_out.append(state.output.torque)

fig, axes = plt.subplots(nrows=4, ncols=1,
                         sharex=True)
ax1 = axes[0]
ax2 = axes[1]
ax3 = axes[2]
ax4 = axes[3]

ax1.plot(motor_rpms)
ax1.set_title("RPM")
ax2.plot(motor_power_in)
ax2.set_title("Power In")
ax3.plot(motor_power_out)
ax3.set_title("Power Out")
ax4.plot(motor_torque_out)
ax4.set_title("Torque Out")
for ax in axes:
    ax.grid()
fig.tight_layout()
plt.show()
