import numpy as np
from app.models.analytics import AnomalyDetectionResult, AnomalyPoint


class AnomalyDetector:
    def detect(self, df, variable: str, window: int = 24) -> AnomalyDetectionResult:
        if variable not in df.columns:
            values = df["electricity_wh"].values if "electricity_wh" in df.columns else df["water_liters"].values
        else:
            values = df[variable].values

        timestamps = df["timestamp"].values if "timestamp" in df.columns else np.arange(len(values))

        if len(values) < window:
            return AnomalyDetectionResult(apartment_id="", variable=variable, anomalies=[])

        anomalies = []
        for i in range(window, len(values)):
            window_data = values[i - window:i]
            mu = np.mean(window_data)
            sigma = np.std(window_data) + 1e-10
            z_score = (values[i] - mu) / sigma

            if abs(z_score) > 2.5:
                severity = "critical" if abs(z_score) > 4.0 else "warning" if abs(z_score) > 3.0 else "minor"
                anomalies.append(AnomalyPoint(
                    timestamp=int(timestamps[i]),
                    actual_value=float(values[i]),
                    expected_value=float(mu),
                    anomaly_score=float(abs(z_score)),
                    severity=severity,
                    description=f"{variable} deviated {abs(z_score):.1f} sigma from rolling mean",
                ))

        return AnomalyDetectionResult(
            apartment_id="",
            variable=variable,
            anomalies=anomalies[:50],
        )
