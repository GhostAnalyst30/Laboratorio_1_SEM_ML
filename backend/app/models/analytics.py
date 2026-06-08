from pydantic import BaseModel
from typing import Optional


class ForecastPoint(BaseModel):
    timestamp: int
    predicted_value: float
    lower_bound: float
    upper_bound: float


class ForecastResult(BaseModel):
    apartment_id: str
    variable: str
    horizon_steps: int
    forecasts: list[ForecastPoint]
    model_used: str


class AnomalyPoint(BaseModel):
    timestamp: int
    actual_value: float
    expected_value: float
    anomaly_score: float
    severity: str
    description: str


class AnomalyDetectionResult(BaseModel):
    apartment_id: str
    variable: str
    anomalies: list[AnomalyPoint]


class ClusterProfile(BaseModel):
    cluster_id: int
    label: str
    size: int
    avg_electricity_kwh: float
    avg_water_liters: float
    avg_gas_m3: float
    avg_sustainability: float
    description: str


class Recommendation(BaseModel):
    category: str
    priority: str
    title: str
    description: str
    potential_savings: str
    estimated_impact: float


class AIInsight(BaseModel):
    apartment_id: str
    summary: str
    efficiency_grade: str
    forecast: Optional[ForecastResult] = None
    anomalies: list[AnomalyPoint] = []
    recommendations: list[Recommendation] = []
    peer_comparison: Optional[dict] = None


class SustainabilityMetrics(BaseModel):
    overall_score: float
    energy_score: float
    water_score: float
    waste_score: float
    community_score: float
    self_sufficiency: float
    carbon_footprint_kg: float
