from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.config import settings
from app.data.query_engine import QueryEngine

router = APIRouter(prefix="/towers", tags=["towers"])
qe = QueryEngine()


@router.get("")
async def list_towers():
    return {
        "towers": [
            {
                "id": tid,
                "name": f"Tower {tid}",
                "floors": settings.floors_per_tower,
                "apartments_per_floor": settings.apartments_per_floor,
                "total_apartments": settings.floors_per_tower * settings.apartments_per_floor,
            }
            for tid in settings.towers
        ]
    }


@router.get("/{tower_id}")
async def get_tower_detail(tower_id: str):
    if tower_id.upper() not in settings.towers:
        raise HTTPException(404, f"Tower {tower_id} not found")
    tid = tower_id.upper()
    return {
        "id": tid,
        "name": f"Tower {tid}",
        "floors": settings.floors_per_tower,
        "apartments_per_floor": settings.apartments_per_floor,
        "total_apartments": settings.floors_per_tower * settings.apartments_per_floor,
        "floors": [
            {
                "floor": f,
                "apartments": [f"{tid}{f}-{a}" for a in range(1, settings.apartments_per_floor + 1)],
            }
            for f in range(1, settings.floors_per_tower + 1)
        ],
    }


@router.get("/{tower_id}/timeseries")
async def get_tower_timeseries(
    tower_id: str,
    variable: Optional[str] = Query(None),
    date_from: Optional[int] = Query(None),
    date_to: Optional[int] = Query(None),
    limit: int = Query(5000, le=50000),
):
    try:
        df = qe.query_tower(tower_id.upper(), variable, date_from, date_to)
        records = df.head(limit).to_dicts()
        return {"tower": tower_id.upper(), "records": len(records), "data": records}
    except Exception as e:
        return {"tower": tower_id.upper(), "records": 0, "data": [], "error": str(e)}


@router.get("/{tower_id}/floors")
async def get_tower_floors(tower_id: str):
    tid = tower_id.upper()
    if tid not in settings.towers:
        raise HTTPException(404, f"Tower {tid} not found")
    return {
        "tower": tid,
        "floors": [
            {
                "floor": f,
                "apartments": [f"{tid}{f}-{a}" for a in range(1, settings.apartments_per_floor + 1)],
            }
            for f in range(1, settings.floors_per_tower + 1)
        ],
    }
