"""
This module carries out a minimalistic
simulation with a simple electric vehicle.
"""

import matplotlib.pyplot as plt
from simulation.simulator import Simulator
from examples.battery_and_motor_only import minimalistic_em_vehicle

time_steps: int = 100
control_signal: list[float] = [0.2] * time_steps

simulation = Simulator(time_steps=time_steps,
                       delta_t=0.1,
                       control_signal=control_signal,
                       vehicle=minimalistic_em_vehicle)
motor_id = minimalistic_em_vehicle.converters[0].id
battery_id = minimalistic_em_vehicle.energy_sources[0].id
simulation.simulate(load_torque=300.0)

motor_hist = simulation.history[motor_id]
motor_hist_snapshots = motor_hist["snapshots"]
battery_hist = simulation.history[battery_id]
battery_hist_snapshots = battery_hist["snapshots"]

motor_rpms: list[float] = []
motor_power_in: list[float] = []
motor_power_out: list[float] = []
motor_torque_out: list[float] = []
for snap in motor_hist_snapshots:
    motor_rpms.append(snap.state.output_port.rpm)
    motor_power_in.append(snap.power_in)
    motor_power_out.append(snap.power_out)
    motor_torque_out.append(snap.io.output_port.torque)

battery_power_in: list[float] = []
battery_power_out: list[float] = []
battery_energy: list[float] = []
for snap in battery_hist_snapshots:
    battery_power_in.append(snap.power_in)
    battery_power_out.append(snap.power_out)
    battery_energy.append(snap.state.internal.electric_energy_stored)

fig, axes = plt.subplots(nrows=4, ncols=2,
                         sharex=True)
ax1 = axes[0, 0]
ax2 = axes[1, 0]
ax3 = axes[2, 0]
ax4 = axes[3, 0]
ax5 = axes[0, 1]
ax6 = axes[1, 1]
ax7 = axes[2, 1]

ax1.plot(motor_rpms)
ax1.set_title("Motor RPM Out")
ax1.set_ylabel("RPM")
ax2.plot(motor_power_in)
ax2.set_title("Motor Power In")
ax2.set_ylabel("Power (W)")
ax3.plot(motor_power_out)
ax3.set_title("Motor Power Out")
ax3.set_ylabel("Power (W)")
ax4.plot(motor_torque_out)
ax4.set_xlim(left=0.0, right=time_steps)
ax4.set_title("Motor Torque Out")
ax4.set_xlabel("Time steps")
ax4.set_ylabel("Torque (N.m)")

ax5.plot(battery_energy)
ax5.set_title("Battery Energy")
ax6.plot(battery_power_in)
ax6.set_title("Battery Power In")
ax7.plot(battery_power_out)
ax7.set_title("Battery Power Out")
for ax in ax1, ax2, ax3, ax4, ax5, ax6, ax7:
    ax.set_ylim(bottom=0.0)
    ax.grid()
#for ax in axes:
    #ax.grid()
fig.tight_layout()
plt.show()
