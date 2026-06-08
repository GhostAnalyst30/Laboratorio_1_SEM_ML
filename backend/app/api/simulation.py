from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks
from app.simulation.engine import SimulationEngine
from app.models.scenarios import SCENARIOS
from typing import Optional

router = APIRouter(prefix="/simulation", tags=["simulation"])

engine = SimulationEngine()


@router.post("/start")
async def start_simulation(scenario: Optional[str] = "baseline"):
    if engine.is_running:
        return {"status": "already_running"}
    engine.set_scenario(scenario)
    engine.start()
    return {"status": "started", "scenario": scenario}


@router.post("/pause")
async def pause_simulation():
    engine.pause()
    return {"status": "paused"}


@router.post("/resume")
async def resume_simulation():
    engine.resume()
    return {"status": "resumed"}


@router.post("/stop")
async def stop_simulation():
    engine.stop()
    return {"status": "stopped"}


@router.get("/status")
async def get_simulation_status():
    return engine.get_status()


@router.post("/reset")
async def reset_simulation():
    engine.reset()
    return {"status": "reset"}


@router.get("/scenarios")
async def list_scenarios():
    return {
        "scenarios": [
            {
                "name": name,
                "description": s.description,
                "duration_days": s.duration_days,
            }
            for name, s in SCENARIOS.items()
        ]
    }


@router.post("/speed")
async def set_speed(speed: float = 1.0):
    speed = max(0.1, min(10.0, speed))
    engine.speed_multiplier = speed
    return {"speed": speed}


@router.websocket("/stream")
async def simulation_websocket(websocket: WebSocket):
    await websocket.accept()
    async def send_state(states: list):
        try:
            if states:
                await websocket.send_json({
                    "type": "tick",
                    "virtual_minute": engine.virtual_minute,
                    "states": [
                        {
                            "apartment_id": s.apartment_id,
                            "tower": s.tower,
                            "floor": s.floor,
                            "occupancy_state": s.occupancy_state.value if hasattr(s.occupancy_state, 'value') else s.occupancy_state,
                            "activity_type": s.activity_type.value if hasattr(s.activity_type, 'value') else s.activity_type,
                            "electricity_wh": s.electricity_wh,
                            "water_liters": s.water_liters,
                            "comfort_score": s.comfort_score,
                            "sustainability_score": s.sustainability_score,
                            "temperature": s.temperature,
                        }
                        for s in states[:50]
                    ],
                })
        except Exception:
            pass

    engine.register_observer(send_state)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
