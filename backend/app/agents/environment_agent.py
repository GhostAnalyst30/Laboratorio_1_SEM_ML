import numpy as np
from .base_agent import BaseAgent, AgentContext
from app.models.environment import EnvironmentState, WeatherPattern
from app.utils.fourier import daily_temperature, daily_humidity, daily_solar_radiation, seasonal_temperature_offset
from app.utils.noise import perlin_noise_1d
from app.utils.markov import MarkovChain


class EnvironmentAgent(BaseAgent):
    def __init__(self, agent_id: str = "environment", seed: int = 42):
        super().__init__(agent_id)
        self.pattern = WeatherPattern()
        self.rng = np.random.default_rng(seed)
        self.perlin_offset = int(self.rng.integers(0, 10000))

        weather_states = ["clear", "partly_cloudy", "cloudy", "rainy"]
        self.weather_chain = MarkovChain(
            transition_matrix=self.pattern.markov_transition,
            states=weather_states,
            initial_state=0,
            seed=seed,
        )

        self.cache: dict[int, EnvironmentState] = {}

    def step(self, context: AgentContext, scenario_modifiers: dict = None) -> EnvironmentState:
        if scenario_modifiers is None:
            scenario_modifiers = {}

        virtual_minute = context.virtual_minute
        if virtual_minute in self.cache:
            return self.cache[virtual_minute]

        minute_of_day = context.minute_of_day
        day_of_year = context.day_of_year

        mods = scenario_modifiers
        temp_offset = mods.get("temperature_offset", 0.0)
        humidity_mult = mods.get("humidity_multiplier", 1.0)
        rain_mult = mods.get("rain_multiplier", 1.0)
        solar_mult = mods.get("solar_multiplier", 1.0)

        weather_idx = self.weather_chain.step()
        weather_mult = {"clear": 0.0, "partly_cloudy": 0.3, "cloudy": 0.7, "rainy": 1.0}

        minute_arr = np.array([minute_of_day], dtype=float)
        base_temp = self.pattern.base_temp + seasonal_temperature_offset(np.array([day_of_year]))[0]
        temp_cycle = daily_temperature(minute_arr, base_temp, self.pattern.temp_amplitude)[0]
        perlin_t = perlin_noise_1d(1, self.pattern.perlin_scale, self.perlin_offset + virtual_minute)[0]
        temperature = float(temp_cycle + temp_offset + perlin_t)

        base_hum = daily_humidity(minute_arr, self.pattern.base_humidity, self.pattern.humidity_amplitude)[0]
        rain_factor = weather_mult[self.weather_chain.current_state_name]
        humidity = float(np.clip(base_hum * humidity_mult + rain_factor * 10, 20, 100))

        solar_base = daily_solar_radiation(minute_arr, max_radiation=1000.0)[0]
        cloud_factor = 1.0 - weather_mult[self.weather_chain.current_state_name] * 0.7
        solar_radiation = float(max(0, solar_base * solar_mult * cloud_factor))

        wind_base = 2.0 + 4.0 * np.sin(2 * np.pi * minute_of_day / 1440 + 1.5)[0]
        wind_gust = perlin_noise_1d(1, scale=3.0, seed=self.perlin_offset + virtual_minute + 1000)[0]
        wind_speed = float(max(0, wind_base + wind_gust))

        rain = float(0.0)
        if self.weather_chain.current_state_name == "rainy":
            rain_intensity = 0.5 + 0.5 * np.sin(np.pi * (minute_of_day % 240) / 240)[0]
            rain = float(max(0, rain_intensity * rain_mult * 5.0))
        elif self.weather_chain.current_state_name == "cloudy":
            rain = float(max(0, self.rng.random() * 0.5 * rain_mult))

        air_quality = float(np.clip(
            80 + 20 * np.sin(2 * np.pi * minute_of_day / 1440)
            - rain_factor * 10
            + perlin_noise_1d(1, scale=5, seed=self.perlin_offset + virtual_minute + 2000)[0],
            20, 100
        ))

        pressure = float(1013 + 5 * np.sin(2 * np.pi * day_of_year / 365)
                         - rain_factor * 8
                         + perlin_noise_1d(1, scale=2, seed=self.perlin_offset + virtual_minute + 3000)[0])

        state = EnvironmentState(
            timestamp=virtual_minute,
            minute_of_day=minute_of_day,
            day_of_year=day_of_year,
            temperature=round(temperature, 2),
            humidity=round(humidity, 2),
            wind_speed=round(wind_speed, 2),
            rain=round(rain, 2),
            solar_radiation=round(solar_radiation, 2),
            cloud_coverage=weather_mult[self.weather_chain.current_state_name],
            air_quality=round(air_quality, 2),
            pressure=round(pressure, 2),
            season=["winter", "winter", "spring", "spring", "spring", "summer",
                    "summer", "summer", "autumn", "autumn", "autumn", "winter"][context.month - 1],
            weather_condition=self.weather_chain.current_state_name,
        )

        self.cache[virtual_minute] = state
        return state

    def reset(self):
        self.cache.clear()
        self.weather_chain.reset(0)
