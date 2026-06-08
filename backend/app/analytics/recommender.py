from app.models.analytics import Recommendation


class RecommenderEngine:
    def generate(self, df, apartment_id: str) -> list[Recommendation]:
        recommendations = []

        if "electricity_wh" in df.columns:
            avg_elec = float(df["electricity_wh"].mean())
            if avg_elec > 15.0:
                recommendations.append(Recommendation(
                    category="energy",
                    priority="high",
                    title="Reduce AC Usage",
                    description="Your AC consumption is high. Consider setting thermostat to 24°C and using fans.",
                    potential_savings=f"~{avg_elec * 0.2:.0f} Wh/day",
                    estimated_impact=0.2,
                ))

        if "water_liters" in df.columns:
            avg_water = float(df["water_liters"].mean())
            if avg_water > 3.0:
                recommendations.append(Recommendation(
                    category="water",
                    priority="medium",
                    title="Install Low-Flow Fixtures",
                    description="Reduce shower and faucet flow rates to save water without sacrificing comfort.",
                    potential_savings=f"~{avg_water * 0.3:.0f} L/day",
                    estimated_impact=0.3,
                ))

        if "internet_gb" in df.columns:
            avg_internet = float(df["internet_gb"].mean())
            if avg_internet > 0.05:
                recommendations.append(Recommendation(
                    category="internet",
                    priority="low",
                    title="Optimize Streaming Quality",
                    description="Reduce video streaming quality from 4K to 1080p to lower data usage.",
                    potential_savings=f"~{avg_internet * 0.4:.3f} GB/day",
                    estimated_impact=0.1,
                ))

        if "solar_generation" in df.columns:
            avg_solar = float(df["solar_generation"].mean())
            if avg_solar < 1.0:
                recommendations.append(Recommendation(
                    category="energy",
                    priority="high",
                    title="Install Solar Panels",
                    description="Generate your own clean energy and reduce grid dependence.",
                    potential_savings="Up to 70% on electricity bills",
                    estimated_impact=0.7,
                ))

        if "battery_charge" in df.columns:
            recommendations.append(Recommendation(
                category="energy",
                priority="medium",
                title="Add Battery Storage",
                description="Store excess solar energy for use during peak hours or outages.",
                potential_savings="Increase self-sufficiency by 40%",
                estimated_impact=0.4,
            ))

        return recommendations
