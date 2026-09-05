"""
SOCOCIM SmartFlow — Logistics Service.
Fleet-level aggregations: queue metrics, congestion index, bay utilization.
"""
from __future__ import annotations
from typing import List
from data.vehicles import Vehicle
from utils.constants import VehicleStatus, LOADING_BAYS
from utils.calculations import congestion_index, congestion_level


class LogisticsService:
    def __init__(self, fleet: List[Vehicle], bay_occupancy: dict):
        self.fleet = fleet
        self.bay_occupancy = bay_occupancy

    def active(self) -> List[Vehicle]:
        return [v for v in self.fleet if not v.completed]

    def counts(self) -> dict:
        active = self.active()
        return {
            "on_site": len(active),
            "waiting": len([v for v in active if v.status == VehicleStatus.WAITING]),
            "loading": len([v for v in active if v.status == VehicleStatus.LOADING]),
            "exiting": len([v for v in active if v.status == VehicleStatus.EXITING]),
            "moving": len([v for v in active if v.status == VehicleStatus.MOVING]),
        }

    def waiting_queue(self) -> List[Vehicle]:
        waiting = [v for v in self.active() if v.status == VehicleStatus.WAITING]
        return sorted(waiting, key=lambda v: v.waiting_time_min, reverse=True)

    def average_wait(self) -> float:
        q = self.waiting_queue()
        if not q:
            return 0.0
        return round(sum(v.waiting_time_min for v in q) / len(q), 1)

    def max_wait(self) -> float:
        q = self.waiting_queue()
        return round(max((v.waiting_time_min for v in q), default=0.0), 1)

    def bay_utilization_pct(self) -> float:
        occupied = len([b for b, v in self.bay_occupancy.items() if v is not None])
        total = len(LOADING_BAYS) or 1
        return round(occupied / total * 100, 1)

    def congestion(self) -> tuple[float, str]:
        q = self.waiting_queue()
        idx = congestion_index(
            vehicles_waiting=len(q),
            avg_wait_min=self.average_wait(),
            bay_occupancy_pct=self.bay_utilization_pct(),
        )
        return idx, congestion_level(idx)

    def throughput_last_hour_estimate(self) -> int:
        # Approximation: completed vehicles are pruned, so estimate via exiting+loading turnover
        active = self.active()
        return max(4, len([v for v in active if v.status in (VehicleStatus.EXITING, VehicleStatus.LOADING)]) * 3)

    def free_bay(self) -> str | None:
        return next((b for b, occ in self.bay_occupancy.items() if occ is None), None)