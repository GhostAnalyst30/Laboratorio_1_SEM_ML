from .base_agent import AgentContext


def build_context(virtual_minute: int, minutes_per_day: int = 1440,
                  days_per_month: int = 30, scenario_name: str = "baseline") -> AgentContext:
    total_minutes = virtual_minute
    minute_of_day = total_minutes % minutes_per_day
    day_of_month = (total_minutes // minutes_per_day) % days_per_month + 1
    day_of_year = total_minutes // minutes_per_day + 1
    month = ((day_of_year - 1) // days_per_month) % 12 + 1
    year = 2026 + ((day_of_year - 1) // 365)
    day_of_week = (day_of_year - 1) % 7

    return AgentContext(
        virtual_minute=virtual_minute,
        minute_of_day=minute_of_day,
        day_of_month=day_of_month,
        day_of_week=day_of_week,
        day_of_year=day_of_year,
        month=month,
        year=year,
        scenario_name=scenario_name,
    )
