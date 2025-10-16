# V-Lab
*A modular vehicle simulator.*

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-in%20development-orange)

---

## 🧭 Overview
**V-Lab** is a modular simulation framework built in Python to model and analyze vehicle systems of various architectures, from conventional internal combustion configurations to hybrid and fully electric drivetrains.

The simulator emphasizes **component modularity**, **energy conversion tracking**, and **system-level interactions** between mechanical and electrical subsystems.  
It is intended mainly for developers, engineers, and researchers interested in exploring vehicle dynamics, power management, and energy efficiency.

---

## ⚙️ Key Features
1. **Fully modular architecture**  
&nbsp;Each subsystem (energy source, converter, drivetrain, brakes, etc.) operates independently
2. **Multiple energy sources**  
&nbsp;Supports batteries and fuel tanks for liquid and gaseous fuels
3. **Converters for realistic transformations**  
&nbsp;Engines, motors, gearboxes, differentials, fuel cells, and more
4. **Dynamic energy flow simulation**  
&nbsp;Models torque, speed, power, and efficiency across linked components
5. **Extensible design**  
&nbsp;Straightforward to implement new converters, energy sources, or control logic modules
6. **Visualization tools**  
&nbsp;Integrates with `matplotlib` and `pandas` for plotting and data analysis

---

## 🏗️ Project Architecture
At its core, **V-Lab** is structured around a `Vehicle` class that integrates several modular components:

| Component | Role |
|------------|------|
| **EnergySource** | Provides energy (e.g., battery, fuel tank) |
| **Converter** | Transforms energy between domains (e.g., motor, engine, fuel cell, gearbox, differential) |
| **Body** | Represents the vehicle’s physical and aerodynamic properties |
| **Brakes** | Models dissipative braking (regenerative braking handled by reversible converters) |
| **DriveTrain** | Connects converters and mechanical links between axles and wheels |
| **Links** | Connect elements via torque and angular velocity relationships |
| **ECU** | Electronic Control Unit that manages control logic and coordination between components |
| **Simulator** | Manages time steps, updates component states, and stores results |

---

## 🚀 Getting Started

### Requirements
- Python 3.11+  
- `matplotlib`  
- `pandas`

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚦 Running a basic simulation

Example (_examples\minimal_simulation.py_):

```python
"""
This module carries out a minimalistic
simulation with a simple electric vehicle.
"""

from simulation.results import ResultsManager
from simulation.simulator import Simulator
from examples.battery_and_motor_only import minimalistic_em_vehicle
from examples.example_tracks import return_flat_track

time_steps: int = 300
control_signal: list[float] = [1.0] * time_steps

flat_track = return_flat_track(length=100.0)

simulation = Simulator(name="minimalistic_sim",
                       time_steps=time_steps,
                       delta_t=0.1,
                       control_signal=control_signal,
                       vehicle=minimalistic_em_vehicle,
                       track=flat_track,
                       precision=8)
simulation.simulate(load_torque=100.0)

results = ResultsManager(simulation=simulation)

results.plot_all()
results.save_csv()
```

---

## 🛣️ Roadmap

✅ Core vehicle structure and component integration  
✅ Energy flow logic (mechanical and electrical)  
✅ Inertia reflection and rotational dynamics  
🟡 Track interaction (rolling resistance, slip, terrain modeling)  
🟡 ECU control strategies (PID, energy management)  
🟡 Multi-energy hybrid vehicle configurations  
🟢 Visualization and reporting improvements  

---

## 🤝 Contributing

Contributions are welcome!  
Please fork the repository and submit pull requests with new features, bug fixes, or documentation improvements.

---

## ⚖️ License

This project is licensed under the MIT License; see the LICENSE file for details.
