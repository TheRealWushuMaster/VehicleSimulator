"""This module contains functions for plotting data."""

from typing import Callable
import matplotlib.pyplot as plt
import numpy as np
from components.state import MechanicalState

def plot_power_curve_and_efficiency(min_rpm: float,
                                    max_rpm: float,
                                    num_points: int,
                                    power_max: float,
                                    power_func: Callable[[MechanicalState], float],
                                    eff_func: Callable[[MechanicalState], float]
                                    ) -> None:
    rpm_vals = np.linspace(min_rpm, max_rpm, num_points)
    power_vals = np.array([power_func(MechanicalState(power=0.0,
                                                      efficiency=1.0,
                                                      delivering=False,
                                                      receiving=False,
                                                      rpm=rpm,
                                                      on=True)) for rpm in rpm_vals])
    power_grid = np.linspace(0, power_max, num_points)
    power_mesh, rpm_mesh = np.meshgrid(power_grid, rpm_vals)
    eff_grid = np.zeros_like(rpm_mesh)
    for i, p in enumerate(power_grid):
        for j, r in enumerate(rpm_vals):
            if p <= power_vals[j]:
                state = MechanicalState(power=p,
                                        efficiency=1.0,
                                        delivering=False,
                                        receiving=False,
                                        rpm=r,
                                        on=True)
                eff_grid[j, i] = eff_func(state)
            else:
                eff_grid[j, i] = None
    fig = plt.figure(figsize=(14, 6))
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(rpm_vals, power_vals, label="Power Curve", color="tab:blue")
    ax1.set_xlabel("RPM")
    ax1.set_ylabel("Power (kW)")
    ax1.set_title("Power vs RPM")
    ax1.grid(True)
    ax1.legend()
    ax1.set_ylim(bottom=0)
    ax1.set_xlim(left=min_rpm, right=max_rpm)
    ax2 = fig.add_subplot(1, 2, 2)
    c = ax2.contourf(rpm_mesh, power_mesh, eff_grid, levels=100, cmap="plasma")
    fig.colorbar(c, ax=ax2, label="Efficiency")
    ax2.set_xlabel("RPM")
    ax2.set_ylabel("Power (kW)")
    ax2.set_title("Efficiency Map (Power vs RPM)")
    ax2.set_ylim(bottom=0)
    ax2.set_xlim(left=min_rpm, right=max_rpm)
    plt.tight_layout()
    plt.show()
