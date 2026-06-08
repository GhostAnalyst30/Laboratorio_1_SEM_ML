from dataclasses import dataclass, field
import numpy as np


@dataclass
class EnvironmentState:
    timestamp: int
    minute_of_day: int
    day_of_year: int

    temperature: float
    humidity: float
    wind_speed: float
    rain: float
    solar_radiation: float
    cloud_coverage: float
    air_quality: float
    pressure: float

    season: str
    weather_condition: str


@dataclass
class WeatherPattern:
    base_temp: float = 25.0
    temp_amplitude: float = 8.0
    base_humidity: float = 65.0
    humidity_amplitude: float = 15.0

    fourier_coeffs: list = field(default_factory=lambda: [
        (1, 0.5),
        (2, 0.3),
        (3, 0.15),
        (4, 0.08),
    ])

    markov_transition: np.ndarray = field(default_factory=lambda: np.array([
        [0.85, 0.10, 0.03, 0.02],
        [0.15, 0.70, 0.10, 0.05],
        [0.05, 0.15, 0.70, 0.10],
        [0.02, 0.05, 0.15, 0.78],
    ]))

    perlin_scale: float = 1.5
    seasonal_temp_offset: np.ndarray = field(default_factory=lambda: np.array([
        0.0, 0.0, 2.0, 5.0, 8.0, 10.0, 12.0, 11.0, 8.0, 5.0, 2.0, 0.0
    ]))
