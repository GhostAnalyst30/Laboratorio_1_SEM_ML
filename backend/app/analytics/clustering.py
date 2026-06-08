import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from app.models.analytics import ClusterProfile


class ClusterAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None

    def analyze(self, df, n_clusters: int = 4) -> list[ClusterProfile]:
        agg = df.group_by("apartment_id").agg([
            df["electricity_wh"].mean().alias("avg_elec"),
            df["water_liters"].mean().alias("avg_water"),
            df["gas_m3"].mean().alias("avg_gas"),
            df["sustainability_score"].mean().alias("avg_sustain"),
            df["comfort_score"].mean().alias("avg_comfort"),
        ]).to_pandas()

        if len(agg) < n_clusters:
            return []

        features = agg[["avg_elec", "avg_water", "avg_gas", "avg_sustain", "avg_comfort"]].values
        scaled = self.scaler.fit_transform(features)

        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = self.model.fit_predict(scaled)

        profiles = []
        for c in range(n_clusters):
            mask = labels == c
            if mask.sum() == 0:
                continue
            cluster_data = agg[mask]
            avg_elec = float(cluster_data["avg_elec"].mean())
            avg_water = float(cluster_data["avg_water"].mean())
            avg_gas = float(cluster_data["avg_gas"].mean())
            avg_sustain = float(cluster_data["avg_sustain"].mean())

            if avg_sustain > 0.6 and avg_elec < np.median(agg["avg_elec"].values):
                label = "Eco-Conscious"
                desc = "Low consumption, high sustainability awareness"
            elif avg_elec > np.percentile(agg["avg_elec"].values, 75):
                label = "High Consumers"
                desc = "Above-average energy and water usage"
            elif avg_water > np.percentile(agg["avg_water"].values, 75):
                label = "High Water Users"
                desc = "Disproportionate water consumption"
            else:
                label = "Moderate Residents"
                desc = "Average consumption patterns"

            profiles.append(ClusterProfile(
                cluster_id=c,
                label=label,
                size=int(mask.sum()),
                avg_electricity_kwh=round(avg_elec * 1440 / 1000, 2),
                avg_water_liters=round(avg_water * 1440, 2),
                avg_gas_m3=round(avg_gas * 1440, 4),
                avg_sustainability=round(avg_sustain, 3),
                description=desc,
            ))

        return sorted(profiles, key=lambda p: p.size, reverse=True)
