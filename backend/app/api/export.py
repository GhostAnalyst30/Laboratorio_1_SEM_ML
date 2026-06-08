from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from typing import Optional
from app.data.export_service import ExportService

router = APIRouter(prefix="/export", tags=["export"])
exporter = ExportService()


@router.get("/apartment/{apartment_id}")
async def export_apartment(
    apartment_id: str,
    format: str = Query("csv", regex="^(csv|json|parquet)$"),
    date_from: Optional[int] = Query(None),
    date_to: Optional[int] = Query(None),
):
    content_type_map = {
        "csv": "text/csv",
        "json": "application/json",
        "parquet": "application/octet-stream",
    }
    filename_map = {
        "csv": f"{apartment_id}.csv",
        "json": f"{apartment_id}.json",
        "parquet": f"{apartment_id}.parquet",
    }

    if format == "parquet":
        data = exporter.export_parquet(apartment_id=apartment_id, date_from=date_from, date_to=date_to)
    elif format == "csv":
        data = exporter.export_csv(apartment_id=apartment_id, date_from=date_from, date_to=date_to)
    else:
        data = exporter.export_json(apartment_id=apartment_id, date_from=date_from, date_to=date_to)

    return Response(
        content=data,
        media_type=content_type_map[format],
        headers={"Content-Disposition": f'attachment; filename="{filename_map[format]}"'},
    )


@router.get("/tower/{tower_id}")
async def export_tower(
    tower_id: str,
    format: str = Query("csv", regex="^(csv|json|parquet)$"),
    date_from: Optional[int] = Query(None),
    date_to: Optional[int] = Query(None),
):
    content_type_map = {
        "csv": "text/csv",
        "json": "application/json",
        "parquet": "application/octet-stream",
    }
    filename_map = {
        "csv": f"tower_{tower_id}.csv",
        "json": f"tower_{tower_id}.json",
        "parquet": f"tower_{tower_id}.parquet",
    }

    if format == "parquet":
        data = exporter.export_parquet(tower=tower_id.upper(), date_from=date_from, date_to=date_to)
    elif format == "csv":
        data = exporter.export_csv(tower=tower_id.upper(), date_from=date_from, date_to=date_to)
    else:
        data = exporter.export_json(tower=tower_id.upper(), date_from=date_from, date_to=date_to)

    return Response(
        content=data,
        media_type=content_type_map[format],
        headers={"Content-Disposition": f'attachment; filename="{filename_map[format]}"'},
    )


@router.get("/community")
async def export_community(
    format: str = Query("csv", regex="^(csv|json|parquet)$"),
    date_from: Optional[int] = Query(None),
    date_to: Optional[int] = Query(None),
):
    content_type_map = {
        "csv": "text/csv",
        "json": "application/json",
        "parquet": "application/octet-stream",
    }
    filename_map = {
        "csv": "community_data.csv",
        "json": "community_data.json",
        "parquet": "community_data.parquet",
    }

    if format == "parquet":
        data = exporter.export_parquet(date_from=date_from, date_to=date_to)
    elif format == "csv":
        data = exporter.export_csv(date_from=date_from, date_to=date_to)
    else:
        data = exporter.export_json(date_from=date_from, date_to=date_to)

    return Response(
        content=data,
        media_type=content_type_map[format],
        headers={"Content-Disposition": f'attachment; filename="{filename_map[format]}"'},
    )
