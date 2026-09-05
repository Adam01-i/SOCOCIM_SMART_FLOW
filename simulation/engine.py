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

IMPORTANT (i18n): the engine ticks independently of any browser session's
language setting, so events are stored as (timestamp, event_key, params)
tuples — never as final English text. Translation only happens when a
callback renders an event via utils.i18n.t_event(key, params, language).
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
from utils.constants import EquipmentStatus, VehicleStatus, Severity, AlertSource, LOADING_BAYS, SITE_POINTS


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

        self.events: deque = deque(maxlen=40)  # each item: (timestamp, event_key, params)
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

        self.sensor_service.tick()
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
    @staticmethod
    def _bay_name(bay_key: str) -> str:
        return SITE_POINTS.get(bay_key, {}).get("name", bay_key)

    def _seed_initial_events(self):
        seed = [
            ("event_truck_entered_gate", {"vehicle": "TRUCK-004", "gate": self._bay_name("GATE_A")}),
            ("event_temp_stabilized", {"name": "MIXER-01"}),
            ("event_assigned_bay", {"vehicle": "TRUCK-011", "bay": self._bay_name("BAY_3")}),
            ("event_congestion_decreased", {}),
            ("event_operating_normally", {"name": "CONVEYOR-02"}),
        ]
        now = dt.datetime.now()
        for i, (key, params) in enumerate(seed):
            ts = (now - dt.timedelta(seconds=(len(seed) - i) * 40)).strftime("%H:%M:%S")
            self.events.appendleft((ts, key, params))

    def push_event(self, key: str, **params) -> None:
        ts = self.simulation_time.strftime("%H:%M:%S")
        self.events.appendleft((ts, key, params))

    # ------------------------------------------------------------------
    # MAINTENANCE ALERT EVALUATION
    # ------------------------------------------------------------------
    def _evaluate_maintenance_alerts(self):
        for eq in self.equipment:
            if eq.status == EquipmentStatus.CRITICAL:
                rec = RecommendationEngine.for_equipment(eq)
                alert = self.alert_service.raise_alert(Severity.CRITICAL, AlertSource.MAINTENANCE, eq.name, rec)
                if alert:
                    self.push_event("event_critical_alert", name=eq.name, title_key=rec.title_key)
            elif eq.status == EquipmentStatus.WARNING:
                rec = RecommendationEngine.for_equipment(eq)
                alert = self.alert_service.raise_alert(Severity.WARNING, AlertSource.MAINTENANCE, eq.name, rec)
                if alert:
                    self.push_event("event_warning_alert", name=eq.name, title_key=rec.title_key)
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
            severity = Severity.CRITICAL if idx >= 60 else Severity.WARNING
            alert = self.alert_service.raise_alert(severity, AlertSource.LOGISTICS, subject, rec)
            if alert:
                self.push_event("event_congestion_detected", level_key=level, subject_key=subject)
        else:
            self.alert_service.clear_subject(AlertSource.LOGISTICS, subject)

        # bay assignment events
        for v in self.fleet_service.fleet:
            if v.status == VehicleStatus.LOADING and getattr(v, "_event_logged", False) is False:
                self.push_event("event_assigned_bay", vehicle=v.id, bay=self._bay_name(v.assigned_bay))
                v._event_logged = True
            if v.status != VehicleStatus.LOADING and getattr(v, "_event_logged", False):
                v._event_logged = False

    # ------------------------------------------------------------------
    # MANUAL CONTROLS — Maintenance
    # ------------------------------------------------------------------
    def inject_temperature_anomaly(self, equipment_id: str):
        self.sensor_service.inject_temperature_anomaly(equipment_id)
        self.push_event("event_temp_anomaly_injected", name=equipment_id)

    def inject_vibration_anomaly(self, equipment_id: str):
        self.sensor_service.inject_vibration_anomaly(equipment_id)
        self.push_event("event_vib_anomaly_injected", name=equipment_id)

    def simulate_equipment_failure(self, equipment_id: str):
        self.sensor_service.simulate_failure(equipment_id)
        self.push_event("event_failure_simulated", name=equipment_id)

    def set_equipment_offline(self, equipment_id: str, offline: bool = True):
        self.sensor_service.set_offline(equipment_id, offline)
        self.push_event("event_marked_offline" if offline else "event_marked_online", name=equipment_id)

    def restore_normal_state(self, equipment_id: str = None):
        self.sensor_service.restore_normal(equipment_id)
        if equipment_id:
            self.push_event("event_normal_restored_target", name=equipment_id)
        else:
            self.push_event("event_normal_restored_all")

    # ------------------------------------------------------------------
    # MANUAL CONTROLS — Logistics
    # ------------------------------------------------------------------
    def trigger_arrival_rush(self, count: int = 6):
        self.fleet_service.trigger_arrival_rush(count)
        self.push_event("event_arrival_rush", count=count)

    def trigger_gate_congestion(self):
        self.fleet_service.trigger_arrival_rush(8)
        self.push_event("event_gate_congestion_triggered")

    def trigger_bay_failure(self, bay: str = "BAY_2"):
        self.fleet_service.bay_occupancy[bay] = "BLOCKED"
        self.push_event("event_bay_unavailable", bay=self._bay_name(bay))

    def restore_bay(self, bay: str = "BAY_2"):
        self.fleet_service.bay_occupancy[bay] = None
        self.push_event("event_bay_restored", bay=self._bay_name(bay))

    def resolve_congestion(self):
        for v in self.fleet_service.waiting_vehicles():
            v.waiting_time_min = max(0, v.waiting_time_min * 0.3)
        self.fleet_service.redirect_to_gate_b(False)
        self.push_event("event_congestion_resolved")

    def redirect_gate_b(self, active: bool = True):
        self.fleet_service.redirect_to_gate_b(active)
        self.push_event("event_redirect_gate_b_on" if active else "event_redirect_gate_b_off")

    def restore_traffic(self):
        for bay in LOADING_BAYS:
            if self.fleet_service.bay_occupancy.get(bay) == "BLOCKED":
                self.fleet_service.bay_occupancy[bay] = None
        self.resolve_congestion()
        self.push_event("event_traffic_restored")

    # ------------------------------------------------------------------
    # GLOBAL CONTROLS
    # ------------------------------------------------------------------
    def set_speed(self, speed: int):
        self.speed = speed
        self.push_event("event_speed_set", speed=speed)

    def toggle_demo_mode(self, active: bool):
        self.demo_mode = active
        self.demo_started_at = self.tick_count if active else None
        self.push_event("event_demo_on" if active else "event_demo_off")

    def _run_demo_script(self):
        elapsed_ticks = self.tick_count - (self.demo_started_at or self.tick_count)
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