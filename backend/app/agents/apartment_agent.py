import numpy as np
from .base_agent import BaseAgent, AgentContext
from app.models.apartment import (
    ApartmentConfig, ApartmentState, ApartmentMemory, FamilyProfile,
    ApplianceInventory, OccupancyState, ActivityType, IncomeLevel,
)
from app.models.environment import EnvironmentState
from app.models.appliances import APPLIANCE_POWER_WATTS, WATER_FLOW_RATES, GAS_CONSUMPTION


class ApartmentAgent(BaseAgent):
    def __init__(self, config: ApartmentConfig, seed: int = 42):
        super().__init__(config.apartment_id)
        self.config = config
        self.memory = ApartmentMemory()
        self.rng = np.random.default_rng(seed + hash(config.apartment_id) % 10000)
        self.state = self._create_initial_state()

        self.current_activity = ActivityType.SLEEPING
        self.occupants_present = config.family.size
        self.last_adaptation_day = -1
        self.eco_mode = False

        self._precompute_schedules()

    def _precompute_schedules(self):
        family = self.config.family
        self.weekday_schedule = self._build_daily_schedule(family, is_weekend=False)
        self.weekend_schedule = self._build_daily_schedule(family, is_weekend=True)

    def _build_daily_schedule(self, family: FamilyProfile, is_weekend: bool) -> list[tuple[int, int, ActivityType]]:
        schedule = []

        sleep_start = 22 if not is_weekend else 23
        sleep_end = 6 if not is_weekend else 8

        schedule.append((0, sleep_end * 60, ActivityType.SLEEPING))
        schedule.append((sleep_end * 60, sleep_end * 60 + 30, ActivityType.WAKING))

        morning_start = sleep_end * 60 + 30
        schedule.append((morning_start, morning_start + 45, ActivityType.MORNING_ROUTINE))

        breakfast_start = morning_start + 45
        schedule.append((breakfast_start, breakfast_start + 30, ActivityType.EATING))

        if is_weekend:
            day_start = breakfast_start + 30
            schedule.append((day_start, day_start + 120, ActivityType.LEISURE))
            schedule.append((day_start + 120, day_start + 180, ActivityType.CLEANING))
            schedule.append((day_start + 180, day_start + 300, ActivityType.LEISURE))
            schedule.append((day_start + 300, day_start + 360, ActivityType.COOKING))
            schedule.append((day_start + 360, day_start + 390, ActivityType.EATING))
            schedule.append((day_start + 390, sleep_start * 60, ActivityType.ENTERTAINMENT))
        else:
            morning_clean = breakfast_start + 15
            schedule.append((morning_clean, morning_clean + 15, ActivityType.CLEANING))

            if family.work_from_home:
                work_start = morning_clean + 15
                schedule.append((work_start, work_start + 480, ActivityType.WORKING))
                lunch_start = work_start + 480
                schedule.append((lunch_start, lunch_start + 60, ActivityType.EATING))
                schedule.append((lunch_start + 60, lunch_start + 60 + 240, ActivityType.WORKING))
            else:
                away_start = morning_clean + 15
                schedule.append((away_start, away_start + 540, ActivityType.AWAY))
                return_start = away_start + 540
                schedule.append((return_start, return_start + 30, ActivityType.LEISURE))
                schedule.append((return_start + 30, return_start + 90, ActivityType.COOKING))
                schedule.append((return_start + 90, return_start + 120, ActivityType.EATING))

            if family.has_children or family.has_students:
                study_start = 17 * 60
                schedule.append((study_start, study_start + 120, ActivityType.STUDYING))

            family_dinner = 19 * 60 if not family.work_from_home else 18 * 60
            schedule.append((family_dinner - 30, family_dinner, ActivityType.COOKING))
            schedule.append((family_dinner, family_dinner + 30, ActivityType.EATING))
            schedule.append((family_dinner + 30, sleep_start * 60, ActivityType.ENTERTAINMENT))

        schedule.append((sleep_start * 60, 1440, ActivityType.SLEEPING))
        return schedule

    def _get_current_activity(self, minute_of_day: int, is_weekend: bool) -> ActivityType:
        schedule = self.weekend_schedule if is_weekend else self.weekday_schedule
        for start, end, activity in schedule:
            if start <= minute_of_day < end:
                return activity
        return ActivityType.SLEEPING

    def step(self, context: AgentContext, env_state: EnvironmentState, scenario_modifiers: dict = None) -> ApartmentState:
        if scenario_modifiers is None:
            scenario_modifiers = {}

        is_weekend = context.day_of_week >= 5
        minute_of_day = context.minute_of_day
        virtual_minute = context.virtual_minute
        day_of_month = context.day_of_month

        self.current_activity = self._get_current_activity(minute_of_day, is_weekend)
        self.occupants_present = self._compute_occupancy(self.current_activity, is_weekend)

        self._check_adaptation(context)

        consumption = self._compute_consumption(env_state, scenario_modifiers)

        battery_charge = 0.0
        solar_generation = 0.0
        if self.config.has_solar or scenario_modifiers.get("has_solar", False):
            solar_cap = scenario_modifiers.get("solar_capacity_w", self.config.solar_capacity_w)
            solar_generation = self._compute_solar_generation(env_state, solar_cap)

        if self.config.has_battery or scenario_modifiers.get("has_battery", False):
            batt_cap = scenario_modifiers.get("battery_capacity_wh", self.config.battery_capacity_wh)
            battery_charge = self._compute_battery(batt_cap, solar_generation, consumption["electricity_wh"],
                                                    virtual_minute)

        comfort = self._compute_comfort(env_state)
        sustainability = self._compute_sustainability(consumption, solar_generation, battery_charge)

        prices = self._get_prices(scenario_modifiers)

        state = ApartmentState(
            timestamp=virtual_minute,
            apartment_id=self.config.apartment_id,
            tower=self.config.tower,
            floor=self.config.floor,
            apartment_number=self.config.apartment_number,
            temperature=round(env_state.temperature, 2),
            humidity=round(env_state.humidity, 2),
            wind_speed=round(env_state.wind_speed, 2),
            rain=round(env_state.rain, 2),
            solar_radiation=round(env_state.solar_radiation, 2),
            air_quality=round(env_state.air_quality, 2),
            pressure=round(env_state.pressure, 2),
            num_people_present=self.occupants_present,
            occupancy_state=self._get_occupancy_state(),
            activity_type=self.current_activity,
            water_liters=round(consumption["water_liters"], 2),
            water_cost=round(consumption["water_liters"] * prices["water"], 4),
            electricity_wh=round(consumption["electricity_wh"], 2),
            electricity_cost=round(consumption["electricity_wh"] / 1000 * prices["electricity"], 4),
            gas_m3=round(consumption["gas_m3"], 4),
            gas_cost=round(consumption["gas_m3"] * prices["gas"], 4),
            internet_gb=round(consumption["internet_gb"], 4),
            internet_cost=round(consumption["internet_gb"] * prices["internet"], 4),
            battery_charge=round(battery_charge, 2),
            solar_generation=round(solar_generation, 2),
            comfort_score=round(comfort, 3),
            sustainability_score=round(sustainability, 3),
            scenario=context.scenario_name,
        )

        if minute_of_day == 1439:
            day_water = sum(self._daily_water_buffer)
            day_elec = sum(self._daily_elec_buffer)
            day_gas = sum(self._daily_gas_buffer)
            self.memory.add_daily_consumption(day_water, day_elec, day_gas)

        return state

    def _compute_occupancy(self, activity: ActivityType, is_weekend: bool) -> int:
        family_size = self.config.family.size
        if activity in (ActivityType.SLEEPING, ActivityType.WAKING, ActivityType.NIGHT_ROUTINE):
            return family_size
        elif activity == ActivityType.AWAY:
            if is_weekend:
                return max(1, family_size - 2)
            if self.config.family.work_from_home:
                return max(1, family_size - family_size // 2)
            return max(0, family_size - family_size // 2 - 1)
        elif activity in (ActivityType.WORKING, ActivityType.STUDYING):
            if self.config.family.work_from_home:
                return max(1, family_size - family_size // 3)
            return max(1, family_size // 3)
        else:
            return family_size

    def _compute_consumption(self, env_state: EnvironmentState, mods: dict) -> dict:
        activity = self.current_activity
        temp = env_state.temperature
        family = self.config.family
        appliances = self.config.appliances
        base = {"water_liters": 0.0, "electricity_wh": 0.0, "gas_m3": 0.0, "internet_gb": 0.0}

        h, m = divmod(env_state.minute_of_day, 60)
        is_night = h < 6 or h >= 22
        is_daytime = 8 <= h <= 18

        base["electricity_wh"] += appliances.refrigerator * APPLIANCE_POWER_WATTS["refrigerator"]["wattage"] / 60.0

        base["electricity_wh"] += APPLIANCE_POWER_WATTS["router"]["wattage"] / 60.0

        if activity == ActivityType.SLEEPING:
            pass

        elif activity == ActivityType.WAKING:
            pass

        elif activity == ActivityType.MORNING_ROUTINE:
            num_showers = self.occupants_present
            shower_water = num_showers * WATER_FLOW_RATES["shower"] * 5
            base["water_liters"] += shower_water
            base["gas_m3"] += GAS_CONSUMPTION["water_heater_per_min"] * 5 * num_showers
            base["electricity_wh"] += APPLIANCE_POWER_WATTS["water_heater"]["wattage"] / 60.0 * 2 * num_showers

        elif activity == ActivityType.COOKING:
            stove_min = 15 + 10 * (family.size / 3)
            base["gas_m3"] += GAS_CONSUMPTION["stove_burner_per_min"] * stove_min
            base["water_liters"] += WATER_FLOW_RATES["faucet"] * 5
            base["electricity_wh"] += APPLIANCE_POWER_WATTS["stove"]["wattage"] / 60.0 * 0.3

        elif activity == ActivityType.EATING:
            base["water_liters"] += WATER_FLOW_RATES["faucet"] * 2
            if self.rng.random() < 0.3:
                base["electricity_wh"] += APPLIANCE_POWER_WATTS["microwave"]["wattage"] / 60.0 * 2

        elif activity == ActivityType.WORKING:
            num_workers = max(1, self.occupants_present)
            for _ in range(num_workers):
                base["electricity_wh"] += APPLIANCE_POWER_WATTS["computer"]["wattage"] / 60.0
                base["internet_gb"] += 0.08
            base["water_liters"] += WATER_FLOW_RATES["faucet"] * 0.5 * num_workers

        elif activity == ActivityType.STUDYING:
            num_students = max(1, self.occupants_present // 2)
            for _ in range(num_students):
                base["electricity_wh"] += APPLIANCE_POWER_WATTS["laptop"]["wattage"] / 60.0
                base["internet_gb"] += 0.05

        elif activity == ActivityType.LEISURE:
            base["electricity_wh"] += APPLIANCE_POWER_WATTS["tv"]["wattage"] / 60.0
            base["internet_gb"] += 0.01

        elif activity == ActivityType.ENTERTAINMENT:
            tv_hours = 1
            base["electricity_wh"] += APPLIANCE_POWER_WATTS["tv"]["wattage"] / 60.0 * tv_hours
            base["internet_gb"] += 0.15 * tv_hours
            if appliances.gaming_console:
                base["electricity_wh"] += APPLIANCE_POWER_WATTS["gaming_console"]["wattage"] / 60.0
                base["internet_gb"] += 0.3

        elif activity == ActivityType.CLEANING:
            if self.rng.random() < 0.3:
                base["electricity_wh"] += APPLIANCE_POWER_WATTS["vacuum_cleaner"]["wattage"] / 60.0 * 15 \
                    if "vacuum_cleaner" in APPLIANCE_POWER_WATTS else 50
            if self.rng.random() < 0.1:
                base["water_liters"] += WATER_FLOW_RATES["washing_machine"]
                base["electricity_wh"] += APPLIANCE_POWER_WATTS["washing_machine"]["wattage"] / 60.0 * 60

        elif activity == ActivityType.NIGHT_ROUTINE:
            base["water_liters"] += WATER_FLOW_RATES["faucet"] * 2 * self.occupants_present
            base["electricity_wh"] += APPLIANCE_POWER_WATTS["lighting"]["wattage"] / 60.0 * 10 * self.occupants_present

        if is_night and activity != ActivityType.SLEEPING:
            base["electricity_wh"] += APPLIANCE_POWER_WATTS["lighting"]["wattage"] / 60.0 * 2 * self.occupants_present

        if temp > 30:
            ac_minutes = 30 + (temp - 30) * 5
            if self.eco_mode:
                ac_minutes *= 0.5
            ac_power = APPLIANCE_POWER_WATTS["ac_unit"]["wattage"]
            base["electricity_wh"] += ac_power * ac_minutes / 60.0

        if temp < 15 and appliances.electric_heater:
            heater_minutes = 30 + (15 - temp) * 3
            if self.eco_mode:
                heater_minutes *= 0.5
            base["electricity_wh"] += APPLIANCE_POWER_WATTS["heater"]["wattage"] * heater_minutes / 60.0

        w_mult = mods.get("water_multiplier", 1.0)
        e_mult = mods.get("electricity_multiplier", 1.0)
        g_mult = mods.get("gas_multiplier", 1.0)
        i_mult = mods.get("internet_multiplier", 1.0)

        base["water_liters"] *= w_mult
        base["electricity_wh"] *= e_mult
        base["gas_m3"] *= g_mult
        base["internet_gb"] *= i_mult

        return base

    def _compute_solar_generation(self, env_state: EnvironmentState, capacity_w: float) -> float:
        radiation_ratio = env_state.solar_radiation / 1000.0
        efficiency = 0.20
        return capacity_w * radiation_ratio * efficiency / 60.0

    def _compute_battery(self, capacity_wh: float, solar_gen: float,
                         consumption_wh: float, minute: int) -> float:
        if not hasattr(self, '_battery_level'):
            self._battery_level = capacity_wh * 0.5
        if solar_gen > consumption_wh:
            excess = solar_gen - consumption_wh
            self._battery_level = min(capacity_wh, self._battery_level + excess * 0.9)
        else:
            deficit = consumption_wh - solar_gen
            self._battery_level = max(0, self._battery_level - deficit * 0.9)
        return self._battery_level

    def _compute_comfort(self, env_state: EnvironmentState) -> float:
        temp = env_state.temperature
        ideal_temp = 22.0
        temp_comfort = max(0, 1.0 - abs(temp - ideal_temp) / 20.0)

        if self.current_activity == ActivityType.SLEEPING:
            comfort = temp_comfort * 0.8 + 0.2
        elif self.current_activity in (ActivityType.AWAY, ActivityType.WORKING):
            comfort = 0.5 + 0.3 * self.rng.random()
        else:
            comfort = temp_comfort * 0.6 + 0.4

        return float(np.clip(comfort, 0, 1))

    def _compute_sustainability(self, consumption: dict, solar_gen: float, battery: float) -> float:
        awareness = self.config.family.sustainability_awareness
        if self.eco_mode:
            awareness = min(1.0, awareness + 0.2)
        base_score = awareness * 0.4 + 0.2
        solar_bonus = min(0.3, solar_gen * 0.001)
        battery_bonus = min(0.1, battery * 0.00001)
        consumption_penalty = min(0.3, consumption["electricity_wh"] * 0.00005)
        return float(np.clip(base_score + solar_bonus + battery_bonus - consumption_penalty, 0, 1))

    def _get_occupancy_state(self) -> OccupancyState:
        family_size = self.config.family.size
        if self.occupants_present == 0:
            return OccupancyState.EMPTY
        elif self.occupants_present < family_size:
            return OccupancyState.PARTIAL
        return OccupancyState.FULL

    def _get_prices(self, mods: dict) -> dict:
        return {
            "water": mods.get("price_water_per_liter", 0.005),
            "electricity": mods.get("price_electricity_per_kwh", 0.15),
            "gas": mods.get("price_gas_per_m3", 1.20),
            "internet": mods.get("price_internet_per_gb", 0.05),
        }

    def _check_adaptation(self, context: AgentContext):
        if context.day_of_month != self.last_adaptation_day and context.minute_of_day == 0:
            self.last_adaptation_day = context.day_of_month
            avg_bill = self.memory.avg_daily_electricity * 0.15 / 1000 * 30
            threshold = 150.0 * (1.5 if self.config.family.income_level in ("low", "medium") else 1.0)
            if avg_bill > threshold:
                self.eco_mode = True
            elif avg_bill < threshold * 0.6:
                self.eco_mode = False

    def _create_initial_state(self) -> ApartmentState:
        return ApartmentState(
            timestamp=0, apartment_id=self.config.apartment_id,
            tower=self.config.tower, floor=self.config.floor,
            apartment_number=self.config.apartment_number,
            temperature=22.0, humidity=60.0, wind_speed=2.0, rain=0.0,
            solar_radiation=0.0, air_quality=80.0, pressure=1013.0,
            num_people_present=self.config.family.size,
            occupancy_state=OccupancyState.FULL,
            activity_type=ActivityType.SLEEPING,
            water_liters=0.0, water_cost=0.0,
            electricity_wh=0.0, electricity_cost=0.0,
            gas_m3=0.0, gas_cost=0.0,
            internet_gb=0.0, internet_cost=0.0,
            battery_charge=0.0, solar_generation=0.0,
            comfort_score=0.8, sustainability_score=0.5,
            scenario="baseline",
        )

    def reset(self):
        self.memory = ApartmentMemory()
        self.current_activity = ActivityType.SLEEPING
        self.occupants_present = self.config.family.size
        self.eco_mode = False
        self._battery_level = 0.0
