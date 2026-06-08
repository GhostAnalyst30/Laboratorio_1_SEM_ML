from dataclasses import dataclass, field
from .tower import TowerConfig


TOWER_CONFIGS: dict[str, TowerConfig] = {
    tid: TowerConfig(tower_id=tid, name=f"Tower {tid}")
    for tid in ["A", "B", "C", "D", "E", "F"]
}


@dataclass
class CommunityConfig:
    towers: dict[str, TowerConfig] = field(default_factory=lambda: TOWER_CONFIGS)
    name: str = "LAB-SEM-ML Smart Community"
    location: str = "Synthetic City"
    timezone: str = "UTC"

    @property
    def total_apartments(self) -> int:
        return sum(t.total_apartments for t in self.towers.values())

    @property
    def all_apartment_ids(self) -> list[str]:
        ids = []
        for t in self.towers.values():
            ids.extend(t.apartment_ids)
        return ids


@dataclass
class CommunityAggregatedState:
    total_occupants: int
    total_water_liters: float
    total_electricity_kwh: float
    total_gas_m3: float
    total_internet_gb: float
    total_solar_generation_kwh: float
    avg_comfort_score: float
    avg_sustainability_score: float
    occupancy_rate: float
    self_sufficiency_rate: float
