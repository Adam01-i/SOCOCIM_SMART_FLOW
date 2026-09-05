"""
SOCOCIM SmartFlow — Maintenance Service.
Fleet-level aggregations consumed by Overview, Maintenance, Control Center
and Analytics pages, so every page reflects the SAME simulation state.
"""
from __future__ import annotations
from typing import List
from data.equipment import Equipment
from utils.constants import EquipmentStatus


class MaintenanceService:
    def __init__(self, fleet: List[Equipment]):
        self.fleet = fleet

    def equipment_by_id(self, eid: str) -> Equipment | None:
        return next((e for e in self.fleet if e.id == eid), None)

    def counts(self) -> dict:
        online = len([e for e in self.fleet if e.status != EquipmentStatus.OFFLINE])
        warning = len([e for e in self.fleet if e.status == EquipmentStatus.WARNING])
        critical = len([e for e in self.fleet if e.status == EquipmentStatus.CRITICAL])
        offline = len([e for e in self.fleet if e.status == EquipmentStatus.OFFLINE])
        return {
            "total": len(self.fleet),
            "online": online,
            "warning": warning,
            "critical": critical,
            "offline": offline,
        }

    def average_health(self) -> float:
        if not self.fleet:
            return 0.0
        return round(sum(e.health_score for e in self.fleet) / len(self.fleet), 1)

    def average_risk(self) -> float:
        if not self.fleet:
            return 0.0
        return round(sum(e.risk_score for e in self.fleet) / len(self.fleet), 1)

    def critical_equipment(self) -> List[Equipment]:
        return [e for e in self.fleet if e.status == EquipmentStatus.CRITICAL]

    def sorted_by_risk(self) -> List[Equipment]:
        return sorted(self.fleet, key=lambda e: e.risk_score, reverse=True)