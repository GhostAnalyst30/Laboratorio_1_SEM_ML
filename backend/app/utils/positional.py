import numpy as np
from app.models.environment import EnvironmentState
from app.config import settings


TOWER_ANGLES_DEG: dict[str, float] = {
    "A": 0.0,
    "B": 180.0,
}

TOWER_POSITION: dict[str, tuple[float, float]] = {
    "A": (-6.0, 0.0),
    "B": (6.0, 0.0),
}

APARTMENT_FACING: dict[int, float] = {
    1: 45.0,
    2: 135.0,
    3: 225.0,
    4: 315.0,
}


class PositionalEnvironmentModifier:
    def __init__(self, tower: str, floor: int, apartment_number: int):
        self.tower = tower
        self.floor = floor
        self.apartment_number = apartment_number
        self.tower_angle = np.radians(TOWER_ANGLES_DEG.get(tower, 0.0))
        self.facing_angle = np.radians(APARTMENT_FACING.get(apartment_number, 0.0))
        self.absolute_facing = self.tower_angle + self.facing_angle
        self.floor_ratio = floor / settings.floors_per_tower

    def compute(self, env: EnvironmentState) -> dict:
        minute = env.minute_of_day

        sun_angle_rad = np.radians((minute / 1440.0) * 360.0 - 90.0)
        sun_direction = np.array([np.cos(sun_angle_rad), np.sin(sun_angle_rad)], dtype=float)

        apt_direction = np.array([
            np.cos(self.absolute_facing),
            np.sin(self.absolute_facing),
        ], dtype=float)

        cos_angle = float(np.dot(sun_direction, apt_direction))
        sun_exposure = max(0.0, cos_angle) ** 2

        tower_x, tower_z = TOWER_POSITION.get(self.tower, (0.0, 0.0))
        tower_pos = np.array([tower_x, tower_z], dtype=float)
        sun_to_tower = tower_pos / (np.linalg.norm(tower_pos) + 1e-8)

        shadow_factor = max(0.0, -float(np.dot(sun_to_tower, sun_direction)))
        shadow_shading = 1.0 - 0.3 * shadow_factor

        wind_log_profile = np.log(self.floor + 1) / np.log(settings.floors_per_tower + 1)
        wind_mult = 0.3 + 0.7 * wind_log_profile

        temp_height_offset = -0.8 * self.floor_ratio + 0.5 * (1 - self.floor_ratio)

        air_quality_offset = 8.0 * wind_log_profile

        solar_mult = 0.5 + 0.5 * sun_exposure
        solar_mult *= shadow_shading

        is_daytime = 360 < minute < 1260
        if not is_daytime:
            solar_mult *= 0.2
        else:
            if 360 < minute < 720:
                east_weight = max(0.0, 1.0 - abs(minute - 540) / 180)
                facing_eastness = max(0.0, np.cos(self.absolute_facing - np.radians(90)))
                solar_mult += 0.5 * east_weight * facing_eastness
            elif 1080 <= minute < 1260:
                west_weight = max(0.0, 1.0 - abs(minute - 1170) / 180)
                facing_westness = max(0.0, np.cos(self.absolute_facing - np.radians(270)))
                solar_mult += 0.5 * west_weight * facing_westness

            zenith_angle = abs(minute / 1440.0 - 0.5) * 2
            solar_mult *= (1.0 - 0.3 * zenith_angle)

        solar_mult = max(0.0, min(1.5, solar_mult))

        return {
            "temperature_offset": round(temp_height_offset, 2),
            "wind_multiplier": round(wind_mult, 3),
            "solar_multiplier": round(solar_mult, 3),
            "air_quality_offset": round(air_quality_offset, 2),
            "sun_exposure": round(sun_exposure, 3),
        }
