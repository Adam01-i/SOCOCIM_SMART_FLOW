"""
SOCOCIM SmartFlow — Sensor simulation.

MockSensorService: generates credible sensor readings (noise + drift +
occasional anomalies + optional injected anomaly) for each equipment.

Designed so it can later be swapped for a RealIoTSensorService that reads
from actual ESP32 / MQTT sensors, without changing the rest of the app —
both expose the same `tick(equipment)` contract.
"""
from __future__ import annotations
import random
import datetime as dt
from typing import List

from data.equipment import Equipment
from utils.constants import EquipmentStatus
from utils.calculations import (
    metric_subscore, health_score, health_classification,
    rolling_stability_score, trend_factor, risk_score, anomaly_confidence,
)


class MockSensorService:
    """Simulates IoT sensor readings for a fleet of equipment."""

    def __init__(self, fleet: List[Equipment]):
        self.fleet = fleet
        # small persistent random walk offset per-equipment for organic drift
        self._drift = {eq.id: 0.0 for eq in fleet}

    # ------------------------------------------------------------------
    # Public API — this is the contract a RealIoTSensorService must honor
    # ------------------------------------------------------------------
    def tick(self) -> None:
        now = dt.datetime.now().strftime("%H:%M:%S")
        for eq in self.fleet:
            if eq.forced_offline:
                eq.status = EquipmentStatus.OFFLINE
                eq.last_update = now
                continue

            self._advance_temperature(eq)
            self._advance_vibration(eq)
            self._advance_humidity(eq)

            eq.temperature_history.append(eq.temperature)
            eq.vibration_history.append(eq.vibration)
            eq.timestamp_history.append(now)

            self._recompute_scores(eq)
            eq.operating_hours = round(eq.operating_hours + 0.03, 2)
            eq.last_update = now

    def inject_temperature_anomaly(self, equipment_id: str, target_delta: float = 28.0) -> None:
        eq = self._get(equipment_id)
        if eq:
            eq.anomaly_active = True
            eq.anomaly_target_temp = eq.temperature_baseline + target_delta

    def inject_vibration_anomaly(self, equipment_id: str, target_delta: float = 6.5) -> None:
        eq = self._get(equipment_id)
        if eq:
            eq.anomaly_active = True
            eq.anomaly_target_vib = eq.vibration_baseline + target_delta

    def simulate_failure(self, equipment_id: str) -> None:
        eq = self._get(equipment_id)
        if eq:
            eq.anomaly_active = True
            eq.anomaly_target_temp = eq.temperature_baseline + 34
            eq.anomaly_target_vib = eq.vibration_baseline + 9

    def set_offline(self, equipment_id: str, offline: bool) -> None:
        eq = self._get(equipment_id)
        if eq:
            eq.forced_offline = offline
            if not offline:
                eq.status = EquipmentStatus.NORMAL

    def restore_normal(self, equipment_id: str = None) -> None:
        targets = self.fleet if equipment_id is None else [e for e in self.fleet if e.id == equipment_id]
        for eq in targets:
            eq.anomaly_active = False
            eq.anomaly_target_temp = None
            eq.anomaly_target_vib = None
            eq.forced_offline = False

    # ------------------------------------------------------------------
    # Internal mechanics
    # ------------------------------------------------------------------
    def _get(self, equipment_id: str) -> Equipment | None:
        return next((e for e in self.fleet if e.id == equipment_id), None)

    def _advance_temperature(self, eq: Equipment) -> None:
        if eq.anomaly_active and eq.anomaly_target_temp:
            # progressive rise towards the injected target, with noise
            gap = eq.anomaly_target_temp - eq.temperature
            step = gap * 0.18 + random.uniform(-0.3, 0.3)
            eq.temperature = round(eq.temperature + step, 2)
            if abs(gap) < 0.5:
                # hold near target with light jitter, simulating a sustained fault
                eq.temperature = round(eq.anomaly_target_temp + random.uniform(-1.2, 1.2), 2)
        else:
            self._drift[eq.id] += random.uniform(-0.05, 0.05)
            self._drift[eq.id] = max(-2.0, min(2.0, self._drift[eq.id]))
            noise = random.uniform(-0.35, 0.35)
            target = eq.temperature_baseline + self._drift[eq.id]
            eq.temperature = round(eq.temperature + (target - eq.temperature) * 0.3 + noise, 2)
            # rare spontaneous micro-anomaly for realism
            if random.random() < 0.004:
                eq.temperature = round(eq.temperature + random.uniform(3, 7), 2)

    def _advance_vibration(self, eq: Equipment) -> None:
        if eq.anomaly_active and eq.anomaly_target_vib:
            gap = eq.anomaly_target_vib - eq.vibration
            step = gap * 0.20 + random.uniform(-0.08, 0.08)
            eq.vibration = round(max(0, eq.vibration + step), 2)
            if abs(gap) < 0.15:
                eq.vibration = round(max(0, eq.anomaly_target_vib + random.uniform(-0.3, 0.3)), 2)
        else:
            noise = random.uniform(-0.12, 0.12)
            eq.vibration = round(max(0, eq.vibration + (eq.vibration_baseline - eq.vibration) * 0.25 + noise), 2)
            if random.random() < 0.004:
                eq.vibration = round(eq.vibration + random.uniform(1, 2.5), 2)

    def _advance_humidity(self, eq: Equipment) -> None:
        noise = random.uniform(-0.5, 0.5)
        eq.humidity = round(max(0, eq.humidity + (eq.humidity_baseline - eq.humidity) * 0.2 + noise), 1)

    def _recompute_scores(self, eq: Equipment) -> None:
        th = eq.thresholds()
        temp_sub = metric_subscore(eq.temperature, th["temperature"]["normal"], th["temperature"]["warning"])
        vib_sub = metric_subscore(eq.vibration, th["vibration"]["normal"], th["vibration"]["warning"])
        stability_sub = rolling_stability_score(list(eq.vibration_history))

        h_score = health_score(temp_sub, vib_sub, stability_sub)
        eq.health_score = h_score
        eq.health_history.append(h_score)

        temp_trend = trend_factor(list(eq.temperature_history))
        vib_trend = trend_factor(list(eq.vibration_history))
        combined_trend = max(temp_trend, vib_trend)

        r_score = risk_score(temp_sub, vib_sub, combined_trend)
        eq.risk_score = r_score
        eq.risk_history.append(r_score)
        eq.anomaly_confidence = anomaly_confidence(r_score, combined_trend)

        classification = health_classification(h_score)
        if classification == "CRITICAL":
            eq.status = EquipmentStatus.CRITICAL
        elif classification == "WARNING":
            eq.status = EquipmentStatus.WARNING
        else:
            eq.status = EquipmentStatus.NORMAL

        if eq.status in (EquipmentStatus.WARNING, EquipmentStatus.CRITICAL) and eq.estimated_maintenance == "—":
            hours = 4 if eq.status == EquipmentStatus.CRITICAL else 24
            eq.estimated_maintenance = f"< {hours}h"
        elif eq.status == EquipmentStatus.NORMAL:
            eq.estimated_maintenance = "—"