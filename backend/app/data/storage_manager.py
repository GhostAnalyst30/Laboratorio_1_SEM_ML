import asyncio
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import logging

from app.config import settings
from app.data.schema import APARTMENT_STATE_SCHEMA
from app.models.apartment import ApartmentState, OccupancyState, ActivityType

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(self):
        self.data_root = settings.data_root
        self.data_root.mkdir(parents=True, exist_ok=True)

        self._write_queue: asyncio.Queue = asyncio.Queue()
        self._writer_task: asyncio.Task = None
        self._start_writer()

    def _start_writer(self):
        loop = asyncio.get_event_loop()
        self._writer_task = loop.create_task(self._writer_loop())

    async def _writer_loop(self):
        while True:
            batch = await self._write_queue.get()
            try:
                await self._write_parquet(batch)
            except Exception as e:
                logger.error(f"Parquet write error: {e}")
            self._write_queue.task_done()

    async def write_batch_async(self, states: list[ApartmentState]):
        if not states:
            return
        await self._write_queue.put(states)

    async def write_aggregated_async(self, states: list[ApartmentState], period: str):
        if not states:
            return
        batch_id = f"{states[0].timestamp}_{period}"
        path = self.data_root / "aggregated"
        path.mkdir(parents=True, exist_ok=True)
        filepath = path / f"{batch_id}.parquet"

    async def _write_parquet(self, states: list[ApartmentState]):
        if not states:
            return

        first = states[0]
        year = "2026"
        month = f"{first.timestamp // (1440 * 30) % 12 + 1:02d}"
        day = f"{first.timestamp // 1440 % 30 + 1:02d}"

        partition_path = self.data_root / f"year={year}" / f"month={month}" / f"day={day}"
        partition_path.mkdir(parents=True, exist_ok=True)

        arrays = {field.name: [] for field in APARTMENT_STATE_SCHEMA}

        for s in states:
            arrays["timestamp"].append(s.timestamp)
            arrays["apartment_id"].append(s.apartment_id)
            arrays["tower"].append(s.tower)
            arrays["floor"].append(s.floor)
            arrays["apartment_number"].append(s.apartment_number)
            arrays["temperature"].append(s.temperature)
            arrays["humidity"].append(s.humidity)
            arrays["wind_speed"].append(s.wind_speed)
            arrays["rain"].append(s.rain)
            arrays["solar_radiation"].append(s.solar_radiation)
            arrays["air_quality"].append(s.air_quality)
            arrays["pressure"].append(s.pressure)
            arrays["num_people_present"].append(s.num_people_present)
            arrays["occupancy_state"].append(s.occupancy_state.value if isinstance(s.occupancy_state, OccupancyState) else s.occupancy_state)
            arrays["activity_type"].append(s.activity_type.value if isinstance(s.activity_type, ActivityType) else s.activity_type)
            arrays["water_liters"].append(s.water_liters)
            arrays["water_cost"].append(s.water_cost)
            arrays["electricity_wh"].append(s.electricity_wh)
            arrays["electricity_cost"].append(s.electricity_cost)
            arrays["gas_m3"].append(s.gas_m3)
            arrays["gas_cost"].append(s.gas_cost)
            arrays["internet_gb"].append(s.internet_gb)
            arrays["internet_cost"].append(s.internet_cost)
            arrays["battery_charge"].append(s.battery_charge)
            arrays["solar_generation"].append(s.solar_generation)
            arrays["comfort_score"].append(s.comfort_score)
            arrays["sustainability_score"].append(s.sustainability_score)
            arrays["scenario"].append(s.scenario)

        pa_arrays = [pa.array(arrays[field.name], type=field.type) for field in APARTMENT_STATE_SCHEMA]
        table = pa.table(pa_arrays, schema=APARTMENT_STATE_SCHEMA)

        batch_index = (first.timestamp // 1000) % 1000
        filepath = partition_path / f"batch_{batch_index:04d}.parquet"

        pq.write_table(
            table,
            filepath,
            compression=settings.parquet_compression,
            row_group_size=1000,
        )

    def get_apartment_path(self, apartment_id: str) -> Path:
        return self.data_root / f"apartment_id={apartment_id}"

    def get_parquet_paths(self, tower: str = None, date_from: int = None, date_to: int = None) -> list[Path]:
        paths = []
        for year_dir in sorted(self.data_root.glob("year=*")):
            for month_dir in sorted(year_dir.glob("month=*")):
                for day_dir in sorted(month_dir.glob("day=*")):
                    for f in day_dir.glob("*.parquet"):
                        paths.append(f)
        return paths
