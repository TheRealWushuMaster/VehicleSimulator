"""This module defines the internal states of the components."""

from dataclasses import dataclass, field
from typing import Any, Optional
from components.fuel_type import Fuel, LiquidFuel, GaseousFuel
from helpers.functions import assert_type, assert_type_and_range, assert_range, \
    rpm_to_ang_vel, torque_to_power, kelvin_to_celsius, kelvin_to_fahrenheit, \
    electric_power
from helpers.types import ElectricSignalType
from simulation.constants import DEFAULT_TEMPERATURE


#=============================
# BASE STATES
#=============================

@dataclass
class BaseState():
    """
    Base class for all state classes.
    """
    def as_dict(self) -> dict[str, Any]:
        """
        Serializes the state into a dictionary.
        """
        return self.__dict__


@dataclass
class IOState(BaseState):
    """
    Base class for input and output states.
    """
    _is_del: Optional[bool]=field(init=False)

    def __post_init__(self):
        self._is_del = None

    def set_delivering(self) -> None:
        """
        Sets the state as delivering an output.
        """
        self._is_del = True

    def set_receiving(self) -> None:
        """
        Sets the state as receiving an input.
        """
        self._is_del = False

    @property
    def is_delivering(self) -> bool:
        """
        Returns if the state is delivering an output.
        """
        return self._is_del is True

    @property
    def is_receiving(self) -> bool:
        """
        Returns if the state is receiving an input.
        """
        return self._is_del is False

    @property
    def power(self) -> float:
        """
        Returns power exchanged, if applicable.
        """
        raise NotImplementedError

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["is_delivering"] = self.is_delivering
        base["is_receiving"] = self.is_receiving
        return base


@dataclass
class InternalState(BaseState):
    """
    Represents basic internal properties of the component.
    """
    on: bool
    temperature_kelvin: float=DEFAULT_TEMPERATURE

    def __post_init__(self):
        assert_type_and_range(self.temperature_kelvin,
                              more_than=0.0,
                              include_more=False)
        assert_type(self.on,
                    expected_type=bool)

    @property
    def temperature_celsius(self):
        """
        Dynamically calculate the temperature in Celsius.
        """
        return kelvin_to_celsius(t_kelvin=self.temperature_kelvin)

    @property
    def temperature_fahrenheit(self):
        """
        Dynamically calculate the temperature in Fahrenheit.
        """
        return kelvin_to_fahrenheit(t_kelvin=self.temperature_kelvin)

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["temperature_kelvin"] = self.temperature_kelvin
        base["temperature_celsius"] = self.temperature_celsius
        base["temperature_fahrenheit"] = self.temperature_fahrenheit
        base["on"] = self.on
        return base


#=============================
# STORAGE STATES
#=============================


@dataclass
class ElectricEnergyStorageState(BaseState):
    """
    Represents the energy storage state of a component.
    """
    energy: float=0.0

    def __post_init__(self):
        assert_type_and_range(self.energy,
                              more_than=0.0)

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["energy"] = self.energy
        return base


@dataclass
class FuelStorageState(BaseState):
    """
    Represents the state of storing fuel.
    """
    fuel: Fuel

    def __post_init__(self):
        assert_type(self.fuel,
                    expected_type=Fuel)

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["fuel"] = self.fuel
        return base


@dataclass
class LiquidFuelStorageState(FuelStorageState):
    """
    Represents the liquid fuel storage of a fuel tank.
    """
    fuel_liters: float

    def __post_init__(self):
        assert_type_and_range(self.fuel_liters,
                              more_than=0.0)
        super().__post_init__()

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["fuel_liters"] = self.fuel_liters
        return base


@dataclass
class GaseousFuelStorageState(FuelStorageState):
    """
    Represents the gaseous fuel storage of a fuel tank.
    """
    fuel_mass: float

    def __post_init__(self):
        assert_type_and_range(self.fuel_mass,
                              more_than=0.0)
        super().__post_init__()

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["fuel_mass"] = self.fuel_mass
        return base


#=============================
# ENERGY EXCHANGE STATES
#=============================


@dataclass
class RotatingIOState(IOState):
    """
    Represents the state of a rotating component (motor, engine, etc).
    """
    torque: float=0.0
    rpm: float=0.0

    def __post_init__(self):
        assert_range(self.torque, self.rpm,
                     more_than=0.0)
        super().__post_init__()

    @property
    def power(self) -> float:
        """
        Dynamically calculate power.
        """
        return torque_to_power(torque=self.torque,
                               rpm=self.rpm)

    @property
    def ang_vel(self) -> float:
        """
        Dynamically calculate angular velocity.
        """
        return rpm_to_ang_vel(rpm=self.rpm)

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["torque"] = self.torque
        base["ang_vel"] = self.ang_vel
        base["power"] = self.power
        base["rpm"] = self.rpm
        return base


@dataclass
class ElectricIOState(IOState):
    """
    Represents the state of an electrical condition (voltage and current).
    """
    signal_type: ElectricSignalType
    voltage: float=0.0
    current: float=0.0

    def __post_init__(self):
        assert_range(self.power,
                     more_than=0.0)
        assert_type(self.signal_type,
                    expected_type=ElectricSignalType)
        super().__post_init__()

    @property
    def power(self) -> float:
        """
        Dynamically calculates the electric power being transfered.
        """
        return electric_power(voltage=self.voltage,
                              current=self.current)

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["power"] = self.power
        base["voltage"] = self.voltage
        base["current"] = self.current
        return base


#=============================
# FUEL EXCHANGE STATES
#=============================


@dataclass
class FuelIOState(IOState):
    """
    Represents the state of a fuel transfer.
    """
    fuel: Fuel

    def __post_init__(self):
        assert_type(self.fuel,
                    expected_type=Fuel)
        super().__post_init__()

    @property
    def energy(self):
        """
        Must implement a property to calculate the energy transfered.
        """
        raise NotImplementedError

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["fuel"] = self.fuel
        return base


@dataclass
class LiquidFuelIOState(FuelIOState):
    """
    Represents the state of liquid fuel transfer.
    """
    fuel_liters: float=0.0

    def __post_init__(self):
        assert_type_and_range(self.fuel_liters,
                              more_than=0.0)
        super().__post_init__()
        assert_type(self.fuel,
                    expected_type=LiquidFuel)

    @property
    def energy(self) -> float:
        """
        Dynamically calculates the amount
        of equivalent energy transfered.
        """
        assert isinstance(self.fuel, LiquidFuel)
        return self.fuel.energy_per_liter(liters=self.fuel_liters)  # pylint: disable=no-member

    @property
    def power(self) -> float:
        return 0.0

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["energy"] = self.energy
        return base


@dataclass
class GaseousFuelIOState(FuelIOState):
    """
    Represents the state of gaseous fuel transfer.
    """
    fuel_mass: float=0.0

    def __post_init__(self):
        assert_type_and_range(self.fuel_mass,
                              more_than=0.0)
        super().__post_init__()
        assert_type(self.fuel,
                    expected_type=GaseousFuel)

    @property
    def energy(self) -> float:
        """
        Dynamically calculates the amount of energy transfered.
        """
        return self.fuel_mass * self.fuel.energy_density

    @property
    def power(self) -> float:
        return 0.0

    def as_dict(self) -> dict[str, Any]:
        base = super().as_dict()
        base["energy"] = self.energy
        return base


#=============================
# FULL STATE CONFIG
#=============================


@dataclass
class FullStateNoInput():
    """
    Base class for the full state of a component.
    """
    output: IOState
    internal: Optional[InternalState]

    def __post_init__(self):
        assert_type(self.output,
                    expected_type=IOState)
        assert_type(self.internal,
                    expected_type=InternalState,
                    allow_none=True)
        if self.internal is None:
            self.internal = InternalState(temperature_kelvin=DEFAULT_TEMPERATURE,
                                          on=True)


@dataclass
class FullStateWithInput(FullStateNoInput):
    """
    Base class for a full state of a component with input.
    """
    input: IOState

    def __post_init__(self):
        assert_type(self.input,
                    expected_type=IOState)

    @property
    def efficiency(self) -> float:
        """
        Returns the power efficiency in the
        input-output exchange, if applicable.
        """
        if self.input.is_delivering == self.output.is_delivering:
            return 0.0
        if self.input.is_delivering:
            return self.output.power / self.input.power if self.input.power > 0.0 else 0.0
        return self.input.power / self.output.power if self.output.power > 0.0 else 0.0


@dataclass
class FullStateElectricEnergyStorageNoInput(FullStateNoInput):
    """
    Represents the state of a component with electric
    energy storage and no input (non rechargeable).
    """
    electric_energy_storage: ElectricEnergyStorageState

    def __post_init__(self):
        assert_type(self.electric_energy_storage,
                    expected_type=ElectricEnergyStorageState)


@dataclass
class FullStateElectricEnergyStorageWithInput(FullStateWithInput):
    """
    Represents the state of a component with electric
    energy storage with an input (rechargeable).
    """
    electric_energy_storage: ElectricEnergyStorageState

    def __post_init__(self):
        assert_type(self.electric_energy_storage,
                    expected_type=ElectricEnergyStorageState)


@dataclass
class FullStateFuelStorageNoInput(FullStateNoInput):
    """
    Represents the stage of a component with
    fuel storage but no input (not rechargeable)
    """
    fuel_storage: FuelStorageState

    def __post_init__(self):
        assert_type(self.fuel_storage,
                    expected_type=FuelStorageState)


#=============================
# COMPONENTS' STATES
#=============================

def return_rechargeable_battery_state(energy: float=0.0,
                                      voltage_in: float=0.0,
                                      current_in: float=0.0,
                                      voltage_out: float=0.0,
                                      current_out: float=0.0) -> FullStateElectricEnergyStorageWithInput:
    return FullStateElectricEnergyStorageWithInput(
        input=ElectricIOState(signal_type=ElectricSignalType.DC,
                              voltage=voltage_in,
                              current=current_in),
        output=ElectricIOState(signal_type=ElectricSignalType.DC,
                               voltage=voltage_out,
                               current=current_out),
        electric_energy_storage=ElectricEnergyStorageState(energy=energy),
        internal=zero_internal_state()
    )

def return_non_rechargeable_battery_state(energy: float=0.0,
                                          voltage_out: float=0.0,
                                          current_out: float=0.0) -> FullStateElectricEnergyStorageNoInput:
    return FullStateElectricEnergyStorageNoInput(
        output=ElectricIOState(signal_type=ElectricSignalType.DC,
                               voltage=voltage_out,
                               current=current_out),
        electric_energy_storage=ElectricEnergyStorageState(energy=energy),
        internal=zero_internal_state()
    )

def return_electric_generator_state(torque_in: float=0.0,
                                    rpm_in: float=0.0,
                                    voltage_out: float=0.0,
                                    current_out: float=0.0) -> FullStateWithInput:
    return FullStateWithInput(
        input=RotatingIOState(torque=torque_in,
                              rpm=rpm_in),
        output=ElectricIOState(signal_type=ElectricSignalType.AC,
                               voltage=voltage_out,
                               current=current_out),
        internal=zero_internal_state()
    )

def return_electric_motor_state(signal_type: ElectricSignalType,
                                voltage_in: float=0.0,
                                current_in: float=0.0,
                                torque_out: float=0.0,
                                rpm_out: float=0.0) -> FullStateWithInput:
    return FullStateWithInput(
        input=ElectricIOState(signal_type=signal_type,
                              voltage=voltage_in,
                              current=current_in),
        output=RotatingIOState(torque=torque_out,
                               rpm=rpm_out),
        internal=zero_internal_state()
    )

def return_liquid_combustion_engine_state(fuel: LiquidFuel,
                                          fuel_liters_in: float=0.0,
                                          torque_out: float=0.0,
                                          rpm_out: float=0.0) -> FullStateWithInput:
    return FullStateWithInput(
        input=LiquidFuelIOState(fuel=fuel,
                                fuel_liters=fuel_liters_in),
        output=RotatingIOState(torque=torque_out,
                               rpm=rpm_out),
        internal=zero_internal_state()
    )

def return_gaseous_combustion_engine_state(fuel: GaseousFuel,
                                           fuel_mass_in: float=0.0,
                                           torque_out: float=0.0,
                                           rpm_out: float=0.0) -> FullStateWithInput:
    return FullStateWithInput(
        input=GaseousFuelIOState(fuel=fuel,
                                 fuel_mass=fuel_mass_in),
        output=RotatingIOState(torque=torque_out,
                               rpm=rpm_out),
        internal=zero_internal_state()
    )

def return_fuel_cell_state(fuel: GaseousFuel,
                           fuel_mass_in: float=0.0,
                           voltage_out: float=0.0,
                           current_out: float=0.0) -> FullStateWithInput:
    return FullStateWithInput(
        input=GaseousFuelIOState(fuel=fuel,
                                 fuel_mass=fuel_mass_in),
        output=ElectricIOState(signal_type=ElectricSignalType.DC,
                               voltage=voltage_out,
                               current=current_out),
        internal=zero_internal_state()
    )

def return_pure_mechanical_state(torque_in: float=0.0,
                                 rpm_in: float=0.0,
                                 torque_out: float=0.0,
                                 rpm_out: float=0.0) -> FullStateWithInput:
    return FullStateWithInput(
        input=RotatingIOState(torque=torque_in,
                              rpm=rpm_in),
        output=RotatingIOState(torque=torque_out,
                               rpm=rpm_out),
        internal=zero_internal_state()
    )

def return_pure_electric_state(signal_type_in: ElectricSignalType,
                               signal_type_out: ElectricSignalType,
                               voltage_in: float=0.0,
                               current_in: float=0.0,
                               voltage_out: float=0.0,
                               current_out: float=0.0
                               ) -> FullStateWithInput:
    return FullStateWithInput(
        input=ElectricIOState(signal_type=signal_type_in,
                              voltage=voltage_in,
                              current=current_in),
        output=ElectricIOState(signal_type=signal_type_out,
                               voltage=voltage_out,
                               current=current_out),
        internal=zero_internal_state()
    )

def return_liquid_fuel_tank_state(fuel: LiquidFuel,
                                  fuel_liters_stored: float=0.0,
                                  fuel_liters_out: float=0.0) -> FullStateFuelStorageNoInput:
    return FullStateFuelStorageNoInput(
        output=LiquidFuelIOState(fuel=fuel,
                                 fuel_liters=fuel_liters_out),
        fuel_storage=LiquidFuelStorageState(fuel=fuel,
                                            fuel_liters=fuel_liters_stored),
        internal=zero_internal_state()
    )

def return_gaseous_fuel_tank_state(fuel: GaseousFuel,
                                   fuel_mass_stored: float=0.0,
                                   fuel_mass_out: float=0.0) -> FullStateFuelStorageNoInput:
    return FullStateFuelStorageNoInput(
        output=GaseousFuelIOState(fuel=fuel,
                                  fuel_mass=fuel_mass_out),
        fuel_storage=GaseousFuelStorageState(fuel=fuel,
                                            fuel_mass=fuel_mass_stored),
        internal=zero_internal_state()
    )

# =============================

def zero_rotating_io_state() -> RotatingIOState:
    """
    Returns a mechanical rotating state with values set to zero.
    """
    return RotatingIOState(torque=0.0,
                           rpm=0.0)

def zero_electric_io_state(signal_type: ElectricSignalType) -> ElectricIOState:
    """
    Returns an electric state with values set to zero.
    """
    return ElectricIOState(signal_type=signal_type,
                           voltage=0.0,
                           current=0.0)

def zero_liquid_fuel_io_state(fuel: Fuel) -> LiquidFuelIOState:
    """
    Returns a liquid fuel state with values set to zero.
    """
    return LiquidFuelIOState(fuel=fuel,
                             fuel_liters=0.0)

def zero_gaseous_fuel_io_state(fuel: Fuel) -> GaseousFuelIOState:
    """
    Returns a liquid fuel state with values set to zero.
    """
    return GaseousFuelIOState(fuel=fuel,
                              fuel_mass=0.0)

def zero_internal_state(temperature: float=DEFAULT_TEMPERATURE,
                        on: bool=False) -> InternalState:
    """
    Returns an internal state with values set to zero.
    """
    assert_type_and_range(temperature,
                          more_than=0.0)
    return InternalState(temperature_kelvin=temperature,
                         on=on)
