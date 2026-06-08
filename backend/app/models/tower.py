from dataclasses import dataclass


@dataclass
class TowerConfig:
    tower_id: str
    name: str
    num_floors: int = 7
    apartments_per_floor: int = 4

    @property
    def total_apartments(self) -> int:
        return self.num_floors * self.apartments_per_floor

    @property
    def apartment_ids(self) -> list[str]:
        ids = []
        for floor in range(1, self.num_floors + 1):
            for apt in range(1, self.apartments_per_floor + 1):
                ids.append(f"{self.tower_id}{floor}-{apt}")
        return ids


@dataclass
class TowerAggregatedState:
    tower_id: str
    total_occupants: int
    total_water_liters: float
    total_electricity_wh: float
    total_gas_m3: float
    total_internet_gb: float
    total_solar_generation: float
    avg_comfort_score: float
    avg_sustainability_score: float
    occupancy_rate: float
