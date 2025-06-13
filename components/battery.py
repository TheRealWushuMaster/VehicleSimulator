"""This module contains definitions for different types of batteries."""

from dataclasses import dataclass

@dataclass
class Battery():
    """
    A generic battery model focusing on tracking energy stored.
    
    Attributes:
        - nominal_energy (float): original max energy when new (Joules)
        - energy (float): current stored energy (Joules)
        - soh (float): state of health (SOH) [0.0-1.0], models degradation
    """
    nominal_energy: float
    energy: float
    soh: float=1.0

    def __post_init__(self) -> None:
        self.energy = min(self.energy, self.max_energy)

    @property
    def soc(self) -> float:
        """
        Returns the battery's current state of charge (SOC).
        """
        return self.energy / self.nominal_energy / self.soh

    @property
    def max_energy(self) -> float:
        """
        Returns the maximum amount of energy
        that can be held by the battery.
        """
        return self.nominal_energy * self.soh

    def recharge(self, power, delta_t) -> None:
        """
        Charges the battery at a defined power over a delta_t duration.
        """
        self.energy = min(self.max_energy, self.energy + abs(power) * delta_t)

    def discharge(self, power, delta_t) -> None:
        """
        Discharges the battery at a defined power over a delta_t duration.
        """
        self.energy = max(0, self.energy - abs(power) * delta_t)
