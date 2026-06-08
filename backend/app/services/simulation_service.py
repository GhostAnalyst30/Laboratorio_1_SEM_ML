from app.simulation.engine import SimulationEngine

_engine: SimulationEngine = None


def get_simulation_engine() -> SimulationEngine:
    global _engine
    if _engine is None:
        _engine = SimulationEngine()
    return _engine
