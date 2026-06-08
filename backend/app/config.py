from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "LAB-SEM-ML - Digital Twin Smart Community"
    app_version: str = "1.0.0"
    debug: bool = True

    data_root: Path = Path(__file__).parent.parent / "data"
    models_root: Path = Path(__file__).parent.parent / "models"

    simulation_tick_seconds: float = 0.5
    simulation_minutes_per_tick: int = 1
    virtual_minutes_per_day: int = 1440
    virtual_days_per_month: int = 30

    towers: list[str] = ["A", "B"]
    floors_per_tower: int = 4
    apartments_per_floor: int = 4

    duckdb_threads: int = 4
    parquet_compression: str = "snappy"
    parquet_batch_size: int = 1000

    analytics_forecast_horizon: int = 72
    analytics_anomaly_window: int = 24

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
