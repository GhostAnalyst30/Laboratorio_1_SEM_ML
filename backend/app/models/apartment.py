from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import numpy as np
from dataclasses import dataclass, field


class OccupancyState(str, Enum):
    EMPTY = "empty"
    PARTIAL = "partial"
    FULL = "full"


class ActivityType(str, Enum):
    SLEEPING = "sleeping"
    WAKING = "waking"
    MORNING_ROUTINE = "morning_routine"
    AWAY = "away"
    WORKING = "working"
    STUDYING = "studying"
    COOKING = "cooking"
    EATING = "eating"
    LEISURE = "leisure"
    CLEANING = "cleaning"
    NIGHT_ROUTINE = "night_routine"
    ENTERTAINMENT = "entertainment"


class IncomeLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    PREMIUM = "premium"


@dataclass
class FamilyProfile:
    size: int
    ages: list[int]
    income_level: IncomeLevel
    sustainability_awareness: float
    work_from_home: bool
    has_children: bool
    has_students: bool


@dataclass
class ApplianceInventory:
    refrigerator: bool = True
    stove: bool = True
    microwave: bool = True
    dishwasher: bool = False
    washing_machine: bool = True
    dryer: bool = False
    tv: int = 1
    computer: int = 1
    ac_units: int = 1
    water_heater: bool = True
    electric_heater: bool = False
    gaming_console: bool = False


@dataclass
class ApartmentConfig:
    apartment_id: str
    tower: str
    floor: int
    apartment_number: int
    family: FamilyProfile
    appliances: ApplianceInventory = field(default_factory=ApplianceInventory)
    has_solar: bool = False
    solar_capacity_w: float = 0.0
    has_battery: bool = False
    battery_capacity_wh: float = 0.0
    has_electric_vehicle: bool = False


@dataclass
class ApartmentState:
    timestamp: int
    apartment_id: str
    tower: str
    floor: int
    apartment_number: int

    temperature: float
    humidity: float
    wind_speed: float
    rain: float
    solar_radiation: float
    air_quality: float
    pressure: float

    num_people_present: int
    occupancy_state: OccupancyState
    activity_type: ActivityType

    water_liters: float
    water_cost: float
    electricity_wh: float
    electricity_cost: float
    gas_m3: float
    gas_cost: float
    internet_gb: float
    internet_cost: float

    battery_charge: float
    solar_generation: float

    comfort_score: float
    sustainability_score: float
    scenario: str


@dataclass
class ApartmentMemory:
    daily_water: list[float] = field(default_factory=list)
    daily_electricity: list[float] = field(default_factory=list)
    daily_gas: list[float] = field(default_factory=list)
    monthly_bills: list[dict] = field(default_factory=list)
    comfort_history: list[float] = field(default_factory=list)

    def add_daily_consumption(self, water: float, electricity: float, gas: float):
        self.daily_water.append(water)
        self.daily_electricity.append(electricity)
        self.daily_gas.append(gas)
        if len(self.daily_water) > 90:
            self.daily_water.pop(0)
            self.daily_electricity.pop(0)
            self.daily_gas.pop(0)

    @property
    def avg_daily_electricity(self) -> float:
        return float(np.mean(self.daily_electricity[-30:])) if self.daily_electricity else 10000.0

    @property
    def avg_daily_water(self) -> float:
        return float(np.mean(self.daily_water[-30:])) if self.daily_water else 300.0

    @property
    def avg_daily_gas(self) -> float:
        return float(np.mean(self.daily_gas[-30:])) if self.daily_gas else 1.5
