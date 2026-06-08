import io
import json
import csv
import pyarrow.parquet as pq
import pyarrow as pa
from pathlib import Path
from typing import Optional
from app.config import settings


class ExportService:
    @staticmethod
    def export_parquet(apartment_id: str = None, tower: str = None,
                       date_from: int = None, date_to: int = None) -> bytes:
        from app.data.query_engine import QueryEngine
        qe = QueryEngine()

        if apartment_id:
            df = qe.query_apartment(apartment_id, date_from=date_from, date_to=date_to)
        elif tower:
            df = qe.query_tower(tower, date_from=date_from, date_to=date_to)
        else:
            df = qe.query_community(date_from=date_from, date_to=date_to)

        table = df.to_arrow()
        buf = io.BytesIO()
        pq.write_table(table, buf, compression="snappy")
        buf.seek(0)
        return buf.getvalue()

    @staticmethod
    def export_csv(apartment_id: str = None, tower: str = None,
                   date_from: int = None, date_to: int = None) -> bytes:
        from app.data.query_engine import QueryEngine
        qe = QueryEngine()

        if apartment_id:
            df = qe.query_apartment(apartment_id, date_from=date_from, date_to=date_to)
        elif tower:
            df = qe.query_tower(tower, date_from=date_from, date_to=date_to)
        else:
            df = qe.query_community(date_from=date_from, date_to=date_to)

        buf = io.StringIO()
        df.write_csv(buf)
        return buf.getvalue().encode("utf-8")

    @staticmethod
    def export_json(apartment_id: str = None, tower: str = None,
                    date_from: int = None, date_to: int = None,
                    limit: int = 10000) -> bytes:
        from app.data.query_engine import QueryEngine
        qe = QueryEngine()

        if apartment_id:
            df = qe.query_apartment(apartment_id, date_from=date_from, date_to=date_to)
        elif tower:
            df = qe.query_tower(tower, date_from=date_from, date_to=date_to)
        else:
            df = qe.query_community(date_from=date_from, date_to=date_to)

        if limit and len(df) > limit:
            df = df.head(limit)

        records = df.to_dicts()
        return json.dumps(records, indent=2).encode("utf-8")
