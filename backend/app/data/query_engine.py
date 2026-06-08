import duckdb
import polars as pl
from pathlib import Path
from typing import Optional

from app.config import settings


class QueryEngine:
    def __init__(self):
        self.db_path = settings.data_root / "analytics.duckdb"
        self._conn: Optional[duckdb.DuckDBPyConnection] = None

    @property
    def conn(self) -> duckdb.DuckDBPyConnection:
        if self._conn is None:
            self._conn = duckdb.connect(str(self.db_path))
            self._conn.execute("SET threads = ?", [settings.duckdb_threads])
            self._conn.execute("SET memory_limit = '2GB'")
        return self._conn

    def query_apartment(self, apartment_id: str, variable: str = None,
                        date_from: int = None, date_to: int = None) -> pl.DataFrame:
        sql = f"""
            SELECT * FROM read_parquet('{settings.data_root}/**/*.parquet',
                hive_partitioning=true)
            WHERE apartment_id = '{apartment_id}'
        """
        if date_from is not None:
            sql += f" AND timestamp >= {date_from}"
        if date_to is not None:
            sql += f" AND timestamp <= {date_to}"
        if variable:
            sql += f" ORDER BY timestamp ASC"
        result = self.conn.execute(sql)
        return pl.from_arrow(result.fetch_arrow_table())

    def query_tower(self, tower: str, variable: str = None,
                    date_from: int = None, date_to: int = None) -> pl.DataFrame:
        sql = f"""
            SELECT * FROM read_parquet('{settings.data_root}/**/*.parquet',
                hive_partitioning=true)
            WHERE tower = '{tower}'
        """
        if date_from is not None:
            sql += f" AND timestamp >= {date_from}"
        if date_to is not None:
            sql += f" AND timestamp <= {date_to}"
        sql += " ORDER BY timestamp ASC"
        result = self.conn.execute(sql)
        return pl.from_arrow(result.fetch_arrow_table())

    def query_community(self, variable: str = None,
                        date_from: int = None, date_to: int = None) -> pl.DataFrame:
        sql = f"""
            SELECT * FROM read_parquet('{settings.data_root}/**/*.parquet',
                hive_partitioning=true)
            WHERE 1=1
        """
        if date_from is not None:
            sql += f" AND timestamp >= {date_from}"
        if date_to is not None:
            sql += f" AND timestamp <= {date_to}"
        sql += " ORDER BY timestamp ASC"
        result = self.conn.execute(sql)
        return pl.from_arrow(result.fetch_arrow_table())

    def query_aggregated(self, level: str = "hourly", tower: str = None,
                         apartment_id: str = None) -> pl.DataFrame:
        group_cols = {
            "hourly": "timestamp / 60 AS hour_group",
            "daily": "timestamp / 1440 AS day_group",
            "monthly": "timestamp / 43200 AS month_group",
        }
        group_col = group_cols.get(level, group_cols["hourly"])

        wheres = []
        if tower:
            wheres.append(f"tower = '{tower}'")
        if apartment_id:
            wheres.append(f"apartment_id = '{apartment_id}'")

        where_clause = " AND ".join(wheres) if wheres else "1=1"

        sql = f"""
            SELECT
                {group_col} AS period,
                tower,
                apartment_id,
                SUM(water_liters) AS total_water,
                SUM(electricity_wh) AS total_electricity,
                SUM(gas_m3) AS total_gas,
                SUM(internet_gb) AS total_internet,
                AVG(comfort_score) AS avg_comfort,
                AVG(sustainability_score) AS avg_sustainability,
                AVG(temperature) AS avg_temperature
            FROM read_parquet('{settings.data_root}/**/*.parquet',
                hive_partitioning=true)
            WHERE {where_clause}
            GROUP BY period, tower, apartment_id
            ORDER BY period ASC
        """
        result = self.conn.execute(sql)
        return pl.from_arrow(result.fetch_arrow_table())

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
