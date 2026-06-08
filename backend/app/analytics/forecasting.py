import numpy as np
from typing import Optional
from app.models.analytics import ForecastResult, ForecastPoint


class Forecaster:
    def __init__(self):
        self.models = {}

    def forecast(self, df, variable: str, horizon: int = 72) -> ForecastResult:
        if variable not in df.columns:
            values = df["electricity_wh"].values if "electricity_wh" in df.columns else df["water_liters"].values
        else:
            values = df[variable].values

        if len(values) < horizon:
            values = np.pad(values, (horizon - len(values) + 1, 0), mode='edge')

        recent = values[-horizon * 2:]

        n = len(recent)
        if n < 10:
            return ForecastResult(
                apartment_id="",
                variable=variable,
                horizon_steps=horizon,
                forecasts=[],
                model_used="none",
            )

        x = np.arange(n)
        coeffs = np.polyfit(x, recent, 2)
        trend = np.polyval(coeffs, x)

        residuals = recent - trend
        noise_std = float(np.std(residuals)) if len(residuals) > 1 else float(np.mean(np.abs(residuals)) * 0.5)

        last_timestamp = int(df["timestamp"].values[-1]) if "timestamp" in df.columns else 0
        minute_step = 1

        forecasts = []
        for i in range(horizon):
            x_future = n + i
            pred = float(np.polyval(coeffs, x_future))
            noise = float(np.random.normal(0, noise_std * 0.5))
            forecast_val = pred + noise
            uncertainty = noise_std * (1.0 + 0.1 * i)
            ts = last_timestamp + minute_step * (i + 1)

            forecasts.append(ForecastPoint(
                timestamp=ts,
                predicted_value=round(max(0, forecast_val), 3),
                lower_bound=round(max(0, forecast_val - 1.96 * uncertainty), 3),
                upper_bound=round(max(0, forecast_val + 1.96 * uncertainty), 3),
            ))

        return ForecastResult(
            apartment_id="",
            variable=variable,
            horizon_steps=horizon,
            forecasts=forecasts,
            model_used="polynomial_trend",
        )
