"""This module contains classes for handling simulation results."""

from collections import defaultdict
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from simulation.simulator import Simulator

NICE_LABELS: dict[str, tuple[str, str, str]] = {
    "rpm_in": ("Speed (%sRPM)", "Input speed", "Input speed (RPM)"),
    "rpm_out": ("Speed (%sRPM)", "Output speed", "Output speed (RPM)"),
    "torque_in": ("Torque (%sN.m)", "Input torque", "Input torque (N.m)"),
    "torque_out": ("Torque (%sN.m)", "Output torque", "Output torque (N.m)"),
    "power_in": ("Power (%sW)", "Input power", "Input power (W)"),
    "power_out": ("Power (%sW)", "Output power", "Output power (W)"),
    "temperature": ("Temperature (K)", "Temperature", "Temperature (K)"),
    "on": ("Status (On/Off)", "Status", "Status (On/Off)"),
    "electric_energy_stored": ("Energy (%sJ)", "Electric energy stored", "Electric energy stored (J)"),
    "fuel_liters_in": ("Fuel flow (liters)", "Input fuel flow", "Input fuel flow (liters)"),
    "fuel_liters_out": ("Fuel flow (liters)", "Output fuel flow", "Output fuel flow (liters)"),
    "fuel_liters_stored": ("Fuel stored (liters)", "Fuel stored", "Fuel stored (liters)"),
    "fuel_mass_in": ("Fuel flow (kg)", "Input fuel flow", "Input fuel flow (kg)"),
    "fuel_mass_out": ("Fuel flow (kg)", "Output fuel flow", "Output fuel flow (kg)"),
    "fuel_mass_stored": ("Fuel stored (kg)", "Fuel stored", "Fuel stored (kg)"),
    "time_step": ("Time step", "Time step", "Time step"),
    "sim_time": ("Time (s)", "Time", "Time (s)"),
    "comp_name": ("Component name", "Component name", "Component name"),
    "comp_id": ("Component Id", "Component Id", "Component Id"),
    "throttle": ("Throttle", "Throttle", "Throttle"),
    "brake": ("Brake", "Brake", "Brake"),
    "load_torque": ("Torque (%sN.m)", "Load torque", "Load torque (N.m)"),
    "tractive_torque": ("Torque (%sN.m)", "Tractive torque", "Tractive torque (N.m)"),
    "position": ("Position (%sm)", "Position", "Position (m)"),
    "velocity": ("Velocity (%sm/s)", "Velocity", "Velocity (m/s)")}
eng_formatter = ticker.EngFormatter()


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
            for i, snap in enumerate(comp_hist["snapshots"]):
                row = snap.to_dict
                row["time_step"] = i
                row["sim_time"] = i * self.simulation.delta_t
                row["comp_name"] = comp_name
                row["comp_id"] = comp_id
                if self.simulation.precision > -1:
                    for key, value in row.items():
                        if isinstance(value, float):
                            row[key] = round(value, self.simulation.precision)
                grouped[comp_type].append(row)
        for comp_type, rows in grouped.items():
            self.dataframes[comp_type] = pd.DataFrame(rows)

    def get_df(self, comp_type: str) -> pd.DataFrame:
        """
        Returns Dataframes for a given type of component.
        """
        return self.dataframes.get(comp_type, pd.DataFrame())

    def plot_all(self, num_cols: int=1,
                 adjust_scale: bool=True,
                 folder: str="examples/results",
                 dpi: int=250):
        """
        Plots all DataFrames with subplots per variable.
        """
        folder = f"{folder}/{self.simulation.name}"
        os.makedirs(folder, exist_ok=True)
        num_cols = max(num_cols, 1)
        for comp_type, df in self.dataframes.items():
            if df.empty:
                continue
            t_min = df.sim_time.min()
            t_max = df.sim_time.max()
            for name in df.comp_name.unique().tolist():
                df_temp = df[df.comp_name==name].set_index("sim_time").drop(
                    columns=["comp_id",
                             "time_step",
                             "comp_name"])
                assert df_temp.empty is False
                for col in df_temp.columns:
                    if df_temp[col].dtype==bool:
                        df_temp[col] = df_temp[col].astype(int)
                axes = df_temp.plot(subplots=True,
                                    layout=(-1, num_cols),
                                    figsize=(6, 10),
                                    legend=False,
                                    sharex=True,
                                    xlim=(t_min, t_max),
                                    title=f"Simulation data for '{name}'\nType = '{comp_type}'")
                axes = axes.flatten()
                fig = axes[0].get_figure()
                fig.canvas.manager.set_window_title(f"{name} - Simulation results")
                for ax, col in zip(axes, df_temp.columns):
                    y_label = NICE_LABELS.get(col, col.replace("_", " "))[0]  # type: ignore
                    title = NICE_LABELS.get(col, col.replace("_", " "))[1]  # type: ignore
                    if "%s" in y_label:
                        if adjust_scale:
                            def format_func(x, p):
                                formatted = eng_formatter(x, p)
                                return formatted.split()[0] if formatted else ""
                            ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_func))
                            max_val = max(abs(df[col].max()), abs(df[col].min()))
                            sample_label = eng_formatter(max_val, None)
                            scale = sample_label.split()[1] if len(sample_label.split()) > 1 else ""
                            y_label = y_label % scale
                        else:
                            y_label = y_label % ""
                    ax.set_title(title)
                    ax.set_xlabel("Time (s)")
                    ax.set_ylabel(y_label)
                    ax.grid(True)
                plt.tight_layout()
                plt.savefig(f"{folder}/{self.simulation.name}-{comp_type}-{name.replace(" ", "_")}.png",
                            dpi=dpi)
        plt.show()

    def save_csv(self, folder: str="examples/results"):
        """
        Save each component type DataFrame to a CSV file.
        """
        folder = f"{folder}/{self.simulation.name}"
        os.makedirs(folder, exist_ok=True)
        for comp_type, df in self.dataframes.items():
            if not df.empty:
                column_names = {col: NICE_LABELS[col][2] if col in NICE_LABELS else col
                                for col in df.columns}
                df = df.rename(columns=column_names)
                df.to_csv(f"{folder}/{self.simulation.name}-{comp_type}-data.csv", index=False)
