import asyncio
import time
import logging
from typing import Optional

from app.config import settings
from app.agents.environment_agent import EnvironmentAgent
from app.agents.apartment_agent import ApartmentAgent
from app.agents.community_agent import CommunityAgent
from app.agents.base_agent import AgentContext
from app.agents.agent_scheduler import build_context
from app.models.apartment import ApartmentConfig, FamilyProfile, IncomeLevel, ApplianceInventory
from app.models.community import CommunityConfig
from app.models.scenarios import Scenario, get_scenario
from app.models.environment import EnvironmentState
from app.data.storage_manager import StorageManager
from app.utils.distributions import (
    sample_family_size, sample_income_level, sample_ages,
    sample_sustainability_awareness, sample_work_from_home,
)
from app.utils.positional import PositionalEnvironmentModifier

logger = logging.getLogger(__name__)


class SimulationEngine:
    def __init__(self):
        self.env_agent = EnvironmentAgent()
        self.community_config = CommunityConfig()
        self.community_agent = CommunityAgent(self.community_config)

        self.apartment_agents: dict[str, ApartmentAgent] = {}
        self._create_apartment_agents()

        self.storage = StorageManager()
        self.scenario: Optional[Scenario] = None

        self.virtual_minute = 0
        self.current_scenario_name = "baseline"
        self.is_running = False
        self.is_paused = False
        self.speed_multiplier = 1.0
        self._tick_task: Optional[asyncio.Task] = None
        self._state_buffer: list = []
        self._observers: list = []

    def _create_apartment_agents(self):
        rng = __import__('numpy').random.default_rng(42)
        apt_id = 0
        for tower_id in settings.towers:
            base_mult = self.community_agent.get_tower_multiplier(tower_id)
            for floor in range(1, settings.floors_per_tower + 1):
                for apartment_num in range(1, settings.apartments_per_floor + 1):
                    apartment_id = f"{tower_id}{floor}-{apartment_num}"
                    seed = 1000 + apt_id

                    fam_size = sample_family_size(rng)
                    income = sample_income_level(rng)
                    ages = sample_ages(rng, fam_size)
                    awareness = sample_sustainability_awareness(rng, income)
                    wfh = sample_work_from_home(rng, income)

                    has_children = any(a < 14 for a in ages)
                    has_students = any(6 <= a <= 22 for a in ages)

                    family = FamilyProfile(
                        size=fam_size, ages=ages,
                        income_level=IncomeLevel(income),
                        sustainability_awareness=awareness,
                        work_from_home=wfh,
                        has_children=has_children,
                        has_students=has_students,
                    )

                    appliances = ApplianceInventory(
                        ac_units=max(1, 1 if income in ("high", "premium") else 0),
                        dishwasher=income in ("high", "premium"),
                        dryer=income == "premium",
                        gaming_console=income in ("high", "premium") and has_children,
                        computer=max(1, 1 if wfh else 1, 2 if has_students else 1),
                        tv=max(1, 2 if income in ("high", "premium") else 1),
                    )

                    config = ApartmentConfig(
                        apartment_id=apartment_id,
                        tower=tower_id,
                        floor=floor,
                        apartment_number=apartment_num,
                        family=family,
                        appliances=appliances,
                    )

                    agent = ApartmentAgent(config, seed=seed)
                    self.apartment_agents[apartment_id] = agent
                    apt_id += 1

    def register_observer(self, callback):
        self._observers.append(callback)

    def _notify_observers(self, states: list):
        for cb in self._observers:
            try:
                cb(states)
            except Exception as e:
                logger.error(f"Observer error: {e}")

    def set_scenario(self, scenario_name: str):
        self.scenario = get_scenario(scenario_name)
        self.current_scenario_name = scenario_name
        logger.info(f"Scenario set to: {scenario_name}")

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.is_paused = False
        self._tick_task = asyncio.create_task(self._run_loop())
        logger.info("Simulation started")

    def pause(self):
        self.is_paused = True
        logger.info("Simulation paused")

    def resume(self):
        self.is_paused = False
        logger.info("Simulation resumed")

    def stop(self):
        self.is_running = False
        self.is_paused = False
        if self._tick_task:
            self._tick_task.cancel()
        logger.info("Simulation stopped")

    async def _run_loop(self):
        while self.is_running:
            if self.is_paused:
                await asyncio.sleep(0.1)
                continue

            tick_start = time.perf_counter()

            context = build_context(
                self.virtual_minute,
                settings.virtual_minutes_per_day,
                settings.virtual_days_per_month,
                self.current_scenario_name,
            )

            mods = self.scenario.apartment_modifiers if self.scenario else {}
            env_mods = self.scenario.env_modifiers if self.scenario else {}
            events = self.scenario.events if self.scenario else []

            env_state = self.env_agent.step(context, env_mods)

            tower_multipliers = {
                tid: self.community_agent.get_tower_multiplier(tid)
                for tid in settings.towers
            }

            daily_finalized = context.minute_of_day == 1439

            for apt_id, agent in self.apartment_agents.items():
                tower = agent.config.tower
                t_mult = tower_multipliers.get(tower, {})
                apt_mods = dict(mods)
                for k, v in t_mult.items():
                    if k in ("water", "electricity", "gas"):
                        apt_mods[f"{k}_multiplier"] = apt_mods.get(f"{k}_multiplier", 1.0) * v

                for event in events:
                    if event.affected_towers is None or tower in event.affected_towers:
                        event_start = event.start_hour * 60
                        event_end = event_start + event.duration_minutes
                        if event_start <= context.minute_of_day < event_end:
                            if event.event_type == "outage":
                                apt_mods["electricity_multiplier"] = apt_mods.get("electricity_multiplier", 1.0) * 0.05

                pos_mod = PositionalEnvironmentModifier(
                    agent.config.tower,
                    agent.config.floor,
                    agent.config.apartment_number,
                ).compute(env_state)

                local_env = EnvironmentState(
                    timestamp=env_state.timestamp,
                    minute_of_day=env_state.minute_of_day,
                    day_of_year=env_state.day_of_year,
                    temperature=round(env_state.temperature + pos_mod["temperature_offset"], 2),
                    humidity=env_state.humidity,
                    wind_speed=round(env_state.wind_speed * pos_mod["wind_multiplier"], 2),
                    rain=env_state.rain,
                    solar_radiation=round(env_state.solar_radiation * pos_mod["solar_multiplier"], 2),
                    cloud_coverage=env_state.cloud_coverage,
                    air_quality=round(env_state.air_quality + pos_mod["air_quality_offset"], 2),
                    pressure=env_state.pressure,
                    season=env_state.season,
                    weather_condition=env_state.weather_condition,
                )

                state = agent.step(context, local_env, apt_mods)
                self._state_buffer.append(state)

            if len(self._state_buffer) >= settings.parquet_batch_size or daily_finalized:
                batched = self._state_buffer.copy()
                self._state_buffer.clear()
                await self.storage.write_batch_async(batched)

            if self.virtual_minute % 10 == 0:
                self._notify_observers(
                    [s for s in self._state_buffer[-min(168, len(self._state_buffer)):]]
                    if self._state_buffer else []
                )

            self.virtual_minute += settings.simulation_minutes_per_tick

            tick_elapsed = time.perf_counter() - tick_start
            sleep_time = max(0, settings.simulation_tick_seconds / self.speed_multiplier - tick_elapsed)
            await asyncio.sleep(sleep_time)

    def get_status(self) -> dict:
        return {
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "virtual_minute": self.virtual_minute,
            "scenario": self.current_scenario_name,
            "apartment_count": len(self.apartment_agents),
            "speed_multiplier": self.speed_multiplier,
        }

    def reset(self):
        self.stop()
        self.virtual_minute = 0
        self.env_agent.reset()
        self.community_agent.reset()
        for agent in self.apartment_agents.values():
            agent.reset()
        self._state_buffer.clear()
        logger.info("Simulation reset")
