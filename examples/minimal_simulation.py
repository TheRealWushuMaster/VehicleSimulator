"""
This module carries out a minimalistic
simulation with a simple electric vehicle.
"""

import matplotlib.pyplot as plt
from simulation.simulator import Simulator
from examples.battery_and_motor_only import minimalistic_em_vehicle

time_steps: int = 2_000
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
ax1.set_ylim(bottom=0.0)
ax1.set_title("RPM Out")
ax1.set_ylabel("RPM")
ax2.plot(motor_power_in)
ax2.set_ylim(bottom=0.0)
ax2.set_title("Power In")
ax2.set_ylabel("Power (W)")
ax3.plot(motor_power_out)
ax3.set_ylim(bottom=0.0)
ax3.set_title("Power Out")
ax3.set_ylabel("Power (W)")
ax4.plot(motor_torque_out)
ax4.set_xlim(left=0.0, right=time_steps)
ax4.set_ylim(bottom=0.0)
ax4.set_title("Torque Out")
ax4.set_xlabel("Time steps")
for ax in axes:
    ax.grid()
fig.tight_layout()
plt.show()
