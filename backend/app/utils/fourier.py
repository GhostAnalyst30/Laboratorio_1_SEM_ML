import numpy as np


def fourier_series(t: np.ndarray, mean: float, amplitudes: list[float],
                   periods: list[float], phases: list[float]) -> np.ndarray:
    result = np.full_like(t, mean, dtype=float)
    for a, p, phi in zip(amplitudes, periods, phases):
        result += a * np.sin(2 * np.pi * t / p + phi)
    return result


def daily_temperature(minute_of_day: np.ndarray,
                      base_temp: float = 25.0,
                      amplitude: float = 8.0) -> np.ndarray:
    t = minute_of_day / 1440.0
    return base_temp - amplitude * np.cos(2 * np.pi * t)


def daily_humidity(minute_of_day: np.ndarray,
                   base_humidity: float = 65.0,
                   amplitude: float = 15.0) -> np.ndarray:
    t = minute_of_day / 1440.0
    return base_humidity + amplitude * np.sin(2 * np.pi * (t - 0.25))


def daily_solar_radiation(minute_of_day: np.ndarray,
                          max_radiation: float = 1000.0) -> np.ndarray:
    t = minute_of_day / 1440.0
    radiation = max_radiation * np.sin(np.pi * t) ** 4
    radiation = np.clip(radiation, 0, max_radiation)
    night_mask = (minute_of_day < 360) | (minute_of_day > 1260)
    radiation[night_mask] = 0.0
    return radiation


def seasonal_temperature_offset(day_of_year: np.ndarray) -> np.ndarray:
    return 8.0 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
