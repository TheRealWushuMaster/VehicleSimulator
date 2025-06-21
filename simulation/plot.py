"""This module contains functions for plotting data."""

from typing import Callable
import matplotlib.pyplot as plt
import numpy as np

def plot_power_curve_and_efficiency(min_rpm: float,
                                    max_rpm: float,
                                    num_points: int,
                                    power_max: float,
                                    power_func: Callable[[float], float],
                                    eff_func: Callable[[float, float], float]
                                    ) -> None:
    rpm_vals = np.linspace(min_rpm, max_rpm, num_points)
    power_vals = np.array([power_func(rpm) for rpm in rpm_vals])

    power_grid = np.linspace(0, power_max, num_points)
    rpm_grid = np.linspace(min_rpm, max_rpm, num_points)
    p, r = np.meshgrid(power_grid, rpm_grid)
    eff = np.vectorize(eff_func)(p, r)

    # Prepare plots
    fig = plt.figure(figsize=(14, 6))

    # Power vs RPM plot
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(rpm_vals, power_vals, label="Power Curve", color="tab:blue")
    ax1.set_xlabel("RPM")
    ax1.set_ylabel("Power (kW)")
    ax1.set_title("Power vs RPM")
    ax1.grid(True)
    ax1.legend()
    ax1.set_ylim(bottom=0)
    ax1.set_xlim(left=min_rpm, right=max_rpm)

    # Efficiency heatmap
    ax2 = fig.add_subplot(1, 2, 2)
    c = ax2.contourf(r, p, eff, levels=100, cmap="plasma")
    fig.colorbar(c, ax=ax2, label="Efficiency")
    ax2.set_xlabel("RPM")
    ax2.set_ylabel("Power (kW)")
    ax2.set_title("Efficiency Map (Power vs RPM)")
    ax2.set_ylim(bottom=0)
    ax2.set_xlim(left=min_rpm, right=max_rpm)

    plt.tight_layout()
    plt.show()
