from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.data.query_engine import QueryEngine
from app.analytics.forecasting import Forecaster
from app.analytics.anomaly_detection import AnomalyDetector
from app.analytics.clustering import ClusterAnalyzer
from app.analytics.recommender import RecommenderEngine

router = APIRouter(prefix="/analytics", tags=["analytics"])
qe = QueryEngine()
forecaster = Forecaster()
anomaly_detector = AnomalyDetector()
cluster_analyzer = ClusterAnalyzer()
recommender = RecommenderEngine()


@router.get("/forecast/{apartment_id}")
async def forecast_apartment(
    apartment_id: str,
    variable: str = Query("electricity_wh"),
    horizon: int = Query(72, le=168),
):
    try:
        df = qe.query_apartment(apartment_id, variable)
        if len(df) < 24:
            return {"apartment_id": apartment_id, "error": "Insufficient data"}
        result = forecaster.forecast(df, variable, horizon)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/anomalies/{apartment_id}")
async def detect_anomalies(
    apartment_id: str,
    variable: str = Query("electricity_wh"),
    window: int = Query(24, le=168),
):
    try:
        df = qe.query_apartment(apartment_id, variable)
        if len(df) < window:
            return {"apartment_id": apartment_id, "anomalies": []}
        result = anomaly_detector.detect(df, variable, window)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/clusters")
async def get_clusters(
    tower: Optional[str] = Query(None),
    n_clusters: int = Query(4, le=10),
):
    try:
        df = qe.query_community()
        result = cluster_analyzer.analyze(df, n_clusters)
        return {"clusters": result}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/recommendations/{apartment_id}")
async def get_recommendations(apartment_id: str):
    try:
        df = qe.query_apartment(apartment_id)
        if len(df) < 60:
            return {"apartment_id": apartment_id, "recommendations": []}
        result = recommender.generate(df, apartment_id)
        return {"apartment_id": apartment_id, "recommendations": result}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/insights/{apartment_id}")
async def get_insights(apartment_id: str):
    try:
        df = qe.query_apartment(apartment_id)

        if len(df) < 60:
            return {"apartment_id": apartment_id, "summary": "Insufficient data for insights"}

        avg_elec = df["electricity_wh"].mean() if "electricity_wh" in df.columns else 0
        avg_water = df["water_liters"].mean() if "water_liters" in df.columns else 0
        avg_comfort = df["comfort_score"].mean() if "comfort_score" in df.columns else 0
        avg_sustain = df["sustainability_score"].mean() if "sustainability_score" in df.columns else 0

        grade = "A" if avg_sustain > 0.7 else "B" if avg_sustain > 0.5 else "C" if avg_sustain > 0.3 else "D"

        return {
            "apartment_id": apartment_id,
            "summary": f"Average daily electricity: {avg_elec * 1440:.0f} Wh, "
                       f"Water: {avg_water * 1440:.0f} L, "
                       f"Comfort: {avg_comfort:.2f}, Sustainability: {avg_sustain:.2f}",
            "efficiency_grade": grade,
            "recommendations": recommender.generate(df, apartment_id),
        }
    except Exception as e:
        raise HTTPException(500, str(e))
