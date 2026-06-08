import numpy as np
from .base_agent import BaseAgent, AgentContext
from app.models.community import CommunityConfig, TOWER_CONFIGS


class CommunityAgent(BaseAgent):
    def __init__(self, config: CommunityConfig, seed: int = 42):
        super().__init__("community")
        self.config = config
        self.rng = np.random.default_rng(seed)

        self.tower_identities: dict[str, str] = {}
        self._assign_tower_identities()

    def _assign_tower_identities(self):
        archetypes = ["efficient", "high_consumption"]
        sorted_towers = sorted(self.config.towers.keys())
        for i, tid in enumerate(sorted_towers):
            idx = min(i, len(archetypes) - 1)
            self.tower_identities[tid] = archetypes[idx]

    def get_tower_multiplier(self, tower_id: str) -> dict:
        identity = self.tower_identities.get(tower_id, "moderate")
        mults = {
            "efficient": {"water": 0.75, "electricity": 0.70, "gas": 0.80, "sustainability": 1.3},
            "moderate": {"water": 1.0, "electricity": 1.0, "gas": 1.0, "sustainability": 1.0},
            "high_consumption": {"water": 1.3, "electricity": 1.4, "gas": 1.2, "sustainability": 0.7},
        }
        return mults.get(identity, mults["moderate"])

    def step(self, context: AgentContext, **kwargs) -> dict:
        return {"tower_identities": self.tower_identities}

    def reset(self):
        pass
