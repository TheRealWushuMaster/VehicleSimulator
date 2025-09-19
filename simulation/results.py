"""This module contains classes for handling simulation results."""

from collections import defaultdict
import os
import matplotlib.pyplot as plt
import pandas as pd
from simulation.simulator import Simulator

NICE_LABELS: dict[str, tuple[str, str]] = {"rpm_in": ("Speed (RPM)", "Input axis rotation"),
                                           "rpm_out": ("Speed (RPM)", "Output axis rotation"),
                                           "torque_in": ("Torque (N.m)", "Input torque"),
                                           "torque_out": ("Torque (N.m)", "Output torque"),
                                           "power_in": ("Power (W)", "Input power"),
                                           "power_out": ("Power (W)", "Output power"),
                                           "temperature": ("Temperature (K)", "Temperature"),
                                           "on": ("On/Off", "On/Off status"),
                                           "electric_energy_stored": ("Energy (J)", "Electric energy stored"),
                                           "fuel_liters_in": ("Fuel flow (liters)", "Input fuel flow"),
                                           "fuel_liters_out": ("Fuel flow (liters)", "Output fuel flow"),
                                           "fuel_liters_stored": ("Fuel stored (liters)", "Fuel stored"),
                                           "fuel_mass_in": ("Fuel flow (kg)", "Input fuel flow"),
                                           "fuel_mass_out": ("Fuel flow (kg)", "Output fuel flow"),
                                           "fuel_mass_stored": ("Fuel stored (kg)", "Fuel stored")}


class ResultsManager():
    """
    Automatically extracts results from the simulation object
    and creates pandas DataFrame objects for easy visualization.
    """
    def __init__(self, simulation: Simulator) -> None:
        self.simulation = simulation
        self.dataframes: dict[str, pd.DataFrame] = {}
        self._create_dfs()

    def _create_dfs(self) -> None:
        """
        Reads the simulation data from the simulation
        history and creates the appropriate DataFrames.
        """
        grouped = defaultdict(list)
        for comp_id, comp_hist in self.simulation.history.items():
            comp_name = comp_hist["comp_name"]
            comp_type = comp_hist["comp_type"]
            #comp_snap_type = comp_hist["snap_type"]
            for i, snap in enumerate(comp_hist["snapshots"]):
                row = snap.to_dict
                row["time_step"] = i
                row["sim_time"] = i * self.simulation.delta_t
                row["comp_name"] = comp_name
                row["comp_id"] = comp_id
                grouped[comp_type].append(row)
        for comp_type, rows in grouped.items():
            self.dataframes[comp_type] = pd.DataFrame(rows)

    def get_df(self, comp_type: str) -> pd.DataFrame:
        """
        Returns Dataframes for a given type of component.
        """
        return self.dataframes.get(comp_type, pd.DataFrame())

    def plot_all(self):
        """
        Plots all DataFrames with subplots per variable.
        """
        for comp_type, df in self.dataframes.items():
            if not df.empty:
                df = df.set_index("sim_time").drop(columns=["comp_id", "time_step"])
                axes = df.plot(subplots=True,
                               layout=(-1, 2),
                               figsize=(10, 6),
                               legend=True,
                               sharex=True)
                axes = axes.flatten()
            for ax, col in zip(axes, df.columns):  # type: ignore
                y_label = NICE_LABELS.get(col, col.replace("_", " "))[0].title()
                title = NICE_LABELS.get(col, col.replace("_", " "))[1].title()
                ax.set_title(f"{comp_type} - {title}")
                ax.set_xlabel("Time (s)")
                ax.set_ylabel(y_label)
                ax.grid(True)
            plt.tight_layout()
        plt.show()

    def save_csv(self, folder="examples/results"):
        """
        Save each component type DataFrame to a CSV file.
        """
        os.makedirs(folder, exist_ok=True)
        for comp_type, df in self.dataframes.items():
            df.to_csv(f"{folder}/{self.simulation.name}_{comp_type}.csv", index=False)
