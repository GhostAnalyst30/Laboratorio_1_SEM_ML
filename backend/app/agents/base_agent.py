from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AgentContext:
    virtual_minute: int
    minute_of_day: int
    day_of_month: int
    day_of_week: int
    day_of_year: int
    month: int
    year: int
    scenario_name: str


class BaseAgent(ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    @abstractmethod
    def step(self, context: AgentContext, **kwargs) -> dict:
        pass

    @abstractmethod
    def reset(self):
        pass
