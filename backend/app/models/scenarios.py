from dataclasses import dataclass, field
from typing import Optional


@dataclass
class InfrastructureEvent:
    event_type: str
    description: str
    start_hour: int
    duration_minutes: int
    affected_towers: Optional[list[str]] = None
    severity: float = 1.0


@dataclass
class Scenario:
    name: str
    description: str
    duration_days: int = 30

    env_modifiers: dict = field(default_factory=lambda: {
        "temperature_offset": 0.0,
        "humidity_multiplier": 1.0,
        "rain_multiplier": 1.0,
        "solar_multiplier": 1.0,
    })

    apartment_modifiers: dict = field(default_factory=lambda: {
        "has_solar": False,
        "solar_capacity_w": 0.0,
        "has_battery": False,
        "battery_capacity_wh": 0.0,
        "water_multiplier": 1.0,
        "electricity_multiplier": 1.0,
        "gas_multiplier": 1.0,
        "internet_multiplier": 1.0,
        "price_water_per_liter": 0.005,
        "price_electricity_per_kwh": 0.15,
        "price_gas_per_m3": 1.20,
        "price_internet_per_gb": 0.05,
    })

    events: list[InfrastructureEvent] = field(default_factory=list)


SCENARIOS: dict[str, Scenario] = {
    "baseline": Scenario(
        name="baseline",
        description="Month 1: Baseline behavior. Normal conditions, no interventions.",
        duration_days=30,
    ),
    "solar_panels": Scenario(
        name="solar_panels",
        description="Month 2: Solar panels installed on all apartments. Grid consumption reduction measured.",
        duration_days=30,
        apartment_modifiers={"has_solar": True, "solar_capacity_w": 5000},
    ),
    "battery_storage": Scenario(
        name="battery_storage",
        description="Month 3: Battery systems added alongside solar panels. Self-sufficiency measured.",
        duration_days=30,
        apartment_modifiers={
            "has_solar": True, "solar_capacity_w": 5000,
            "has_battery": True, "battery_capacity_wh": 13500,
        },
    ),
    "power_outages": Scenario(
        name="power_outages",
        description="Month 4: Scheduled electricity outages. Community resilience measured.",
        duration_days=30,
        events=[
            InfrastructureEvent("outage", "Scheduled 2h outage", 14, 120, severity=1.0),
            InfrastructureEvent("outage", "Scheduled 1h outage", 20, 60, severity=0.7),
        ],
    ),
    "water_restriction": Scenario(
        name="water_restriction",
        description="Month 5: Water supply restricted to 70%. Adaptation strategies measured.",
        duration_days=30,
        apartment_modifiers={"water_multiplier": 0.7},
    ),
    "heat_wave": Scenario(
        name="heat_wave",
        description="Month 6: Extreme heat wave. Increased cooling demand measured.",
        duration_days=30,
        env_modifiers={"temperature_offset": 8.0, "humidity_multiplier": 0.8},
        apartment_modifiers={"electricity_multiplier": 1.4},
    ),
    "price_increase": Scenario(
        name="price_increase",
        description="Month 7: Utility prices tripled. Consumption elasticity measured.",
        duration_days=30,
        apartment_modifiers={
            "price_water_per_liter": 0.015,
            "price_electricity_per_kwh": 0.45,
            "price_gas_per_m3": 3.60,
            "price_internet_per_gb": 0.15,
        },
    ),
}


def get_scenario(name: str) -> Scenario:
    if name in SCENARIOS:
        return SCENARIOS[name]
    return Scenario(name=name, description="Custom scenario")
