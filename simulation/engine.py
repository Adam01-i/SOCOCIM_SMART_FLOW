"""
SOCOCIM SmartFlow — Global Simulation Engine.

This is the single source of truth for the whole application: every page
and every callback reads from this ONE engine instance so that KPIs stay
consistent across Overview, Maintenance, Logistics, Control Center, Alerts
and Analytics.

Since this Alpha runs as a single-process local demo (no DB, no multi-user
auth), engine state is kept in Python process memory as a module-level
singleton rather than serialized into dcc.Store on every tick — that keeps
the simulation of stateful objects (rolling histories, queues, bay
occupancy) simple and fast. dcc.Store / dcc.Interval are still used on the
frontend purely as tick triggers for callbacks (see callbacks/*).
"""
from __future__ import annotations
import random
import datetime as dt
from collections import deque
from typing import List

from data.equipment import build_initial_fleet as build_equipment_fleet
from data.vehicles import build_initial_fleet as build_vehicle_fleet
from simulation.sensor_simulator import MockSensorService
from simulation.fleet_simulator import MockFleetService
from services.alert_service import AlertService
from services.recommendation_service import RecommendationEngine
from services.maintenance_service import MaintenanceService
from services.logistics_service import LogisticsService
from utils.constants import EquipmentStatus, VehicleStatus, Severity, AlertSource, LOADING_BAYS


class SmartFlowSimulationEngine:
    def __init__(self):
        self.equipment = build_equipment_fleet()
        self.vehicles = build_vehicle_fleet(18)

        self.sensor_service = MockSensorService(self.equipment)
        self.fleet_service = MockFleetService(self.vehicles)
        self.alert_service = AlertService()

        self.simulation_time = dt.datetime.now()
        self.speed = 1
        self.running = True
        self.demo_mode = False
        self.demo_started_at = None

        self.events: deque = deque(maxlen=40)
        self.tick_count = 0
        self.congestion_history: deque = deque(maxlen=60)
        self.queue_length_history: deque = deque(maxlen=60)

        self._seed_initial_events()

    # ------------------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------------------
    def update(self) -> None:
        if not self.running:
            return
        self.tick_count += 1
        self.simulation_time = dt.datetime.now()

        # advance sub-simulations
        self.sensor_service.tick()
        for _ in range(1):  # fleet speed handled via multiplier below
            self.fleet_service.tick(speed_multiplier=self.speed)

        self._evaluate_maintenance_alerts()
        self._evaluate_logistics_alerts()

        if self.demo_mode:
            self._run_demo_script()

    # ------------------------------------------------------------------
    # SERVICES (fresh aggregation views bound to current state)
    # ------------------------------------------------------------------
    @property
    def maintenance(self) -> MaintenanceService:
        return MaintenanceService(self.equipment)

    @property
    def logistics(self) -> LogisticsService:
        return LogisticsService(self.fleet_service.fleet, self.fleet_service.bay_occupancy)

    # ------------------------------------------------------------------
    # EVENT FEED
    # ------------------------------------------------------------------
    def _seed_initial_events(self):
        base_events = [
            "TRUCK-004 entered Gate A",
            "MIXER-01 temperature stabilized",
            "TRUCK-011 assigned Loading Bay 3",
            "Queue congestion decreased",
            "CONVEYOR-02 operating normally",
        ]
        now = dt.datetime.now()
        for i, msg in enumerate(base_events):
            ts = (now - dt.timedelta(seconds=(len(base_events) - i) * 40)).strftime("%H:%M:%S")
            self.events.appendleft((ts, msg))

    def push_event(self, message: str) -> None:
        ts = self.simulation_time.strftime("%H:%M:%S")
        self.events.appendleft((ts, message))

    # ------------------------------------------------------------------
    # MAINTENANCE ALERT EVALUATION
    # ------------------------------------------------------------------
    def _evaluate_maintenance_alerts(self):
        for eq in self.equipment:
            if eq.status == EquipmentStatus.CRITICAL:
                title, message, rec = RecommendationEngine.for_equipment(eq)
                alert = self.alert_service.raise_alert(
                    Severity.CRITICAL, AlertSource.MAINTENANCE, eq.name, message, rec
                )
                if alert:
                    self.push_event(f"CRITICAL alert: {eq.name} — {title.lower()}")
            elif eq.status == EquipmentStatus.WARNING:
                title, message, rec = RecommendationEngine.for_equipment(eq)
                alert = self.alert_service.raise_alert(
                    Severity.WARNING, AlertSource.MAINTENANCE, eq.name, message, rec
                )
                if alert:
                    self.push_event(f"Warning: {eq.name} — {title.lower()}")
            else:
                self.alert_service.clear_subject(AlertSource.MAINTENANCE, eq.name)

    # ------------------------------------------------------------------
    # LOGISTICS ALERT EVALUATION
    # ------------------------------------------------------------------
    def _evaluate_logistics_alerts(self):
        log = self.logistics
        idx, level = log.congestion()
        queue = log.waiting_queue()
        self.congestion_history.append(idx)
        self.queue_length_history.append(len(queue))
        gate_b_available = not self.fleet_service.gate_b_redirect_active

        rec = RecommendationEngine.for_congestion(idx, len(queue), log.average_wait(), gate_b_available)
        subject = "Gate A / Waiting Zone"
        if rec:
            title, message, recommendation = rec
            severity = Severity.CRITICAL if idx >= 60 else Severity.WARNING
            alert = self.alert_service.raise_alert(severity, AlertSource.LOGISTICS, subject, message, recommendation)
            if alert:
                self.push_event(f"{level} congestion detected near {subject}")
        else:
            self.alert_service.clear_subject(AlertSource.LOGISTICS, subject)

        # bay assignment events
        for v in self.fleet_service.fleet:
            if v.status == VehicleStatus.LOADING and getattr(v, "_event_logged", False) is False:
                self.push_event(f"{v.id} assigned {v.assigned_bay.replace('_',' ').title()}")
                v._event_logged = True
            if v.status != VehicleStatus.LOADING and getattr(v, "_event_logged", False):
                v._event_logged = False

    # ------------------------------------------------------------------
    # MANUAL CONTROLS — Maintenance
    # ------------------------------------------------------------------
    def inject_temperature_anomaly(self, equipment_id: str):
        self.sensor_service.inject_temperature_anomaly(equipment_id)
        self.push_event(f"Temperature anomaly injected on {equipment_id}")

    def inject_vibration_anomaly(self, equipment_id: str):
        self.sensor_service.inject_vibration_anomaly(equipment_id)
        self.push_event(f"Vibration anomaly injected on {equipment_id}")

    def simulate_equipment_failure(self, equipment_id: str):
        self.sensor_service.simulate_failure(equipment_id)
        self.push_event(f"Equipment failure simulated on {equipment_id}")

    def set_equipment_offline(self, equipment_id: str, offline: bool = True):
        self.sensor_service.set_offline(equipment_id, offline)
        self.push_event(f"{equipment_id} marked {'OFFLINE' if offline else 'back ONLINE'}")

    def restore_normal_state(self, equipment_id: str = None):
        self.sensor_service.restore_normal(equipment_id)
        target = equipment_id or "all equipment"
        self.push_event(f"Normal state restored for {target}")

    # ------------------------------------------------------------------
    # MANUAL CONTROLS — Logistics
    # ------------------------------------------------------------------
    def trigger_arrival_rush(self, count: int = 6):
        self.fleet_service.trigger_arrival_rush(count)
        self.push_event(f"Arrival rush triggered: +{count} trucks incoming")

    def trigger_gate_congestion(self):
        self.fleet_service.trigger_arrival_rush(8)
        self.push_event("Gate congestion scenario triggered")

    def trigger_bay_failure(self, bay: str = "BAY_2"):
        self.fleet_service.bay_occupancy[bay] = "BLOCKED"
        self.push_event(f"{bay.replace('_',' ').title()} reported unavailable")

    def restore_bay(self, bay: str = "BAY_2"):
        self.fleet_service.bay_occupancy[bay] = None
        self.push_event(f"{bay.replace('_',' ').title()} restored to service")

    def resolve_congestion(self):
        for v in self.fleet_service.waiting_vehicles():
            v.waiting_time_min = max(0, v.waiting_time_min * 0.3)
        self.fleet_service.redirect_to_gate_b(False)
        self.push_event("Congestion resolution actions applied")

    def redirect_gate_b(self, active: bool = True):
        self.fleet_service.redirect_to_gate_b(active)
        self.push_event("Incoming trucks redirected to Gate B" if active else "Gate B redirection lifted")

    def restore_traffic(self):
        for bay in LOADING_BAYS:
            if self.fleet_service.bay_occupancy.get(bay) == "BLOCKED":
                self.fleet_service.bay_occupancy[bay] = None
        self.resolve_congestion()
        self.push_event("Traffic conditions restored to normal")

    # ------------------------------------------------------------------
    # GLOBAL CONTROLS
    # ------------------------------------------------------------------
    def set_speed(self, speed: int):
        self.speed = speed
        self.push_event(f"Simulation speed set to {speed}x")

    def toggle_demo_mode(self, active: bool):
        self.demo_mode = active
        self.demo_started_at = self.tick_count if active else None
        self.push_event("DEMO MODE activated" if active else "DEMO MODE stopped")

    def _run_demo_script(self):
        elapsed_ticks = self.tick_count - (self.demo_started_at or self.tick_count)
        # ~1 tick every TICK_INTERVAL_MS(2.5s); scripted around simple tick thresholds
        script = {
            2: lambda: None,  # normal operations baseline (nothing to do)
            5: lambda: self.inject_vibration_anomaly("EQ-MOT-07"),
            14: lambda: self.trigger_arrival_rush(7),
        }
        action = script.get(elapsed_ticks)
        if action:
            action()

    # ------------------------------------------------------------------
    def system_status_label(self) -> str:
        m = self.maintenance.counts()
        idx, level = self.logistics.congestion()
        if m["critical"] > 0 or level == "CRITICAL":
            return "CRITICAL ATTENTION REQUIRED"
        if m["warning"] > 0 or level in ("HIGH", "MODERATE"):
            return "SYSTEM MONITORING"
        return "SYSTEM OPERATIONAL"


# ---------------------------------------------------------------------------
# Module-level singleton — the single shared engine instance for this process
# ---------------------------------------------------------------------------
ENGINE = SmartFlowSimulationEngine()