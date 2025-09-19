"""This module contains classes for handling simulation results."""

from collections import defaultdict
import os
import matplotlib.pyplot as plt
import pandas as pd
from simulation.simulator import Simulator


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
            comp_type = comp_hist["comp_type"]
            #comp_snap_type = comp_hist["snap_type"]
            for i, snap in enumerate(comp_hist["snapshots"]):
                row = snap.to_dict
                row["time_step"] = i
                row["sim_time"] = i * self.simulation.delta_t
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
                df = df.set_index("time_step").drop(columns=["comp_id", "sim_time"])
                axes = df.plot(subplots=True,
                               layout=(-1, 2),
                               figsize=(10, 6),
                               legend=True,
                               sharex=True)
                axes = axes.flatten()
            for ax, col in zip(axes, df.columns):  # type: ignore
                ax.set_title(f"{comp_type} - {col}")
                ax.set_xlabel("Time [s]")
                ax.set_ylabel(col.replace("_", " ").title())
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
