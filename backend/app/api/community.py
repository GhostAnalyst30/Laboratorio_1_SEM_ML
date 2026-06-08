from fastapi import APIRouter, Query
from typing import Optional
from app.data.query_engine import QueryEngine
from app.config import settings

router = APIRouter(prefix="/community", tags=["community"])
qe = QueryEngine()


@router.get("/summary")
async def get_community_summary():
    try:
        df = qe.query_community()
        if len(df) == 0:
            return {
                "total_apartments": settings.total_apartments,
                "total_towers": len(settings.towers),
                "message": "No data available",
            }

        total_apartments = settings.total_apartments if hasattr(settings, 'total_apartments') \
            else len(settings.towers) * settings.floors_per_tower * settings.apartments_per_floor

        return {
            "total_apartments": total_apartments,
            "total_towers": len(settings.towers),
            "total_records": len(df),
            "latest_electricity_wh": float(df["electricity_wh"].tail(168).sum()) if "electricity_wh" in df.columns else 0,
            "latest_water_liters": float(df["water_liters"].tail(168).sum()) if "water_liters" in df.columns else 0,
            "avg_comfort": float(df["comfort_score"].mean()) if "comfort_score" in df.columns else 0,
            "avg_sustainability": float(df["sustainability_score"].mean()) if "sustainability_score" in df.columns else 0,
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/timeseries")
async def get_community_timeseries(
    variable: Optional[str] = Query(None),
    date_from: Optional[int] = Query(None),
    date_to: Optional[int] = Query(None),
    limit: int = Query(10000, le=100000),
):
    try:
        df = qe.query_community(variable, date_from, date_to)
        records = df.head(limit).to_dicts()
        return {"records": len(records), "data": records}
    except Exception as e:
        return {"records": 0, "data": [], "error": str(e)}


@router.get("/sustainability")
async def get_community_sustainability():
    try:
        df = qe.query_community()
        if len(df) == 0:
            return {"overall_score": 0}

        avg_sustain = float(df["sustainability_score"].mean()) if "sustainability_score" in df.columns else 0
        avg_comfort = float(df["comfort_score"].mean()) if "comfort_score" in df.columns else 0
        total_solar = float(df["solar_generation"].sum()) if "solar_generation" in df.columns else 0
        total_elec = float(df["electricity_wh"].sum()) if "electricity_wh" in df.columns else 1
        self_sufficiency = min(1.0, total_solar / total_elec) if total_elec > 0 else 0

        return {
            "overall_score": round((avg_sustain * 0.4 + avg_comfort * 0.3 + self_sufficiency * 0.3), 3),
            "energy_score": round(avg_sustain * 0.7 + self_sufficiency * 0.3, 3),
            "water_score": round(avg_sustain * 0.8 + 0.2, 3),
            "community_score": round(avg_comfort, 3),
            "self_sufficiency": round(self_sufficiency, 3),
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/emergence")
async def get_community_emergence():
    archetypes = ["efficient", "high_consumption"]
    return {
        "tower_identities": {
            tid: {
                "archetype": archetypes[i] if i < len(archetypes) else "moderate",
                "apartments": settings.floors_per_tower * settings.apartments_per_floor,
            }
            for i, tid in enumerate(settings.towers)
        }
    }
