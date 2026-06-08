from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.config import settings
from app.data.query_engine import QueryEngine

router = APIRouter(prefix="/apartments", tags=["apartments"])
qe = QueryEngine()


@router.get("")
async def list_apartments(
    tower: Optional[str] = Query(None),
    floor: Optional[int] = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
):
    filtered = []
    for tid in settings.towers:
        if tower and tid != tower:
            continue
        for fl in range(1, settings.floors_per_tower + 1):
            if floor and fl != floor:
                continue
            for apt in range(1, settings.apartments_per_floor + 1):
                filtered.append({
                    "apartment_id": f"{tid}{fl}-{apt}",
                    "tower": tid,
                    "floor": fl,
                    "apartment_number": apt,
                })
    return {
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
        "data": filtered[offset:offset + limit],
    }


@router.get("/{apartment_id}")
async def get_apartment_detail(apartment_id: str):
    parts = apartment_id.replace("-", "").strip()
    if len(parts) < 3:
        raise HTTPException(404, "Invalid apartment ID format")
    tower = parts[0].upper()
    floor = int(parts[1])
    apt_num = int(parts[2]) if len(parts) > 2 else 1
    if tower not in settings.towers:
        raise HTTPException(404, f"Tower {tower} not found")
    return {
        "apartment_id": apartment_id,
        "tower": tower,
        "floor": floor,
        "apartment_number": apt_num,
    }


@router.get("/{apartment_id}/timeseries")
async def get_apartment_timeseries(
    apartment_id: str,
    variable: Optional[str] = Query(None),
    date_from: Optional[int] = Query(None),
    date_to: Optional[int] = Query(None),
    limit: int = Query(1000, le=10000),
):
    try:
        df = qe.query_apartment(apartment_id, variable, date_from, date_to)
        records = df.head(limit).to_dicts()
        return {"apartment_id": apartment_id, "records": len(records), "data": records}
    except Exception as e:
        return {"apartment_id": apartment_id, "records": 0, "data": [], "error": str(e)}


@router.get("/{apartment_id}/realtime")
async def get_apartment_realtime(apartment_id: str):
    try:
        df = qe.query_apartment(apartment_id, date_to=999999999)
        if len(df) == 0:
            return {"apartment_id": apartment_id, "state": None}
        latest = df.tail(1).to_dicts()[0]
        return {"apartment_id": apartment_id, "state": latest}
    except Exception as e:
        return {"apartment_id": apartment_id, "state": None, "error": str(e)}


@router.get("/{apartment_id}/hourly")
async def get_apartment_hourly(apartment_id: str):
    df = qe.query_aggregated("hourly", apartment_id=apartment_id)
    return {"apartment_id": apartment_id, "records": len(df), "data": df.to_dicts()}


@router.get("/{apartment_id}/daily")
async def get_apartment_daily(apartment_id: str):
    df = qe.query_aggregated("daily", apartment_id=apartment_id)
    return {"apartment_id": apartment_id, "records": len(df), "data": df.to_dicts()}
