"""
SOCOCIM SmartFlow — Fleet / GPS simulation.

MockFleetService: moves trucks along their route waypoints, manages the
waiting queue and loading bay assignment. Exposes the same `tick()` contract
a future RealGPSFleetService would need to implement.
"""
from __future__ import annotations
import random
from typing import List, Dict
import datetime as dt

from data.vehicles import Vehicle, build_initial_fleet, _plate
from utils.constants import (
    VehicleStatus, SITE_POINTS, ROUTE_GATE_A, ROUTE_GATE_B, LOADING_BAYS, CARGO_TYPES,
)
from utils.calculations import interpolate, clamp


class MockFleetService:
    def __init__(self, fleet: List[Vehicle] | None = None):
        self.fleet: List[Vehicle] = fleet if fleet is not None else build_initial_fleet()
        self.tick_count = 0
        self.next_truck_number = len(self.fleet) + 1
        self.bay_occupancy: Dict[str, str | None] = {b: None for b in LOADING_BAYS}
        self.gate_b_redirect_active = False
        self._sync_bays_from_fleet()

    # ------------------------------------------------------------------
    def _sync_bays_from_fleet(self):
        for v in self.fleet:
            if v.assigned_bay and v.status == VehicleStatus.LOADING:
                self.bay_occupancy[v.assigned_bay] = v.id

    def tick(self, speed_multiplier: float = 1.0) -> None:
        self.tick_count += 1
        step = 0.06 * speed_multiplier  # base progress increment per tick along a route leg

        for v in list(self.fleet):
            if v.completed:
                continue
            self._advance_vehicle(v, step)

        # occasionally spawn a fresh truck at the entry to keep the site alive
        if random.random() < 0.05 * speed_multiplier and len(self.active_vehicles()) < 26:
            self._spawn_vehicle()

        # drop completed vehicles that have fully exited, keep list bounded
        self.fleet = [v for v in self.fleet if not (v.completed and random.random() < 0.15)]

    def active_vehicles(self) -> List[Vehicle]:
        return [v for v in self.fleet if not v.completed]

    # ------------------------------------------------------------------
    def _advance_vehicle(self, v: Vehicle, step: float) -> None:
        route = v.route
        if v.route_index >= len(route) - 1:
            v.completed = True
            v.status = VehicleStatus.COMPLETED
            return

        current_key = route[v.route_index]
        next_key = route[v.route_index + 1]
        p1 = (SITE_POINTS[current_key]["lat"], SITE_POINTS[current_key]["lon"])
        p2 = (SITE_POINTS[next_key]["lat"], SITE_POINTS[next_key]["lon"])

        # Determine behavior depending on the node we're approaching / occupying
        if next_key == "WAITING_ZONE" or current_key == "WAITING_ZONE":
            self._handle_waiting_zone(v, p1, p2, step)
            return

        if next_key in LOADING_BAYS or current_key in LOADING_BAYS:
            self._handle_bay(v, p1, p2, step, next_key, current_key)
            return

        # Regular movement leg
        v.status = VehicleStatus.MOVING if v.progress > 0.05 else self._status_for_node(current_key)
        v.speed_kmh = round(random.uniform(8, 24), 1)
        v.progress += step
        if v.progress >= 1.0:
            v.progress = 0.0
            v.route_index += 1
            v.lat, v.lon = p2
        else:
            v.lat, v.lon = interpolate(p1, p2, v.progress)

        v.eta_min = round((len(route) - 1 - v.route_index) * random.uniform(2.5, 4.5), 1)

    def _status_for_node(self, node_key: str) -> VehicleStatus:
        mapping = {
            "ENTRY": VehicleStatus.APPROACHING,
            "GATE_A": VehicleStatus.AT_GATE,
            "GATE_B": VehicleStatus.AT_GATE,
            "SECURITY": VehicleStatus.AT_GATE,
            "WEIGHBRIDGE": VehicleStatus.WEIGHING,
            "EXIT": VehicleStatus.EXITING,
        }
        return mapping.get(node_key, VehicleStatus.MOVING)

    def _handle_waiting_zone(self, v: Vehicle, p1, p2, step) -> None:
        if v.status != VehicleStatus.WAITING and v.route[v.route_index] != "WAITING_ZONE":
            # entering the waiting zone leg — move towards it first
            v.progress += step
            if v.progress >= 1.0:
                v.progress = 0.0
                v.route_index += 1
                v.lat, v.lon = SITE_POINTS["WAITING_ZONE"]["lat"], SITE_POINTS["WAITING_ZONE"]["lon"]
                v.status = VehicleStatus.WAITING
                v.entered_waiting_zone_at_tick = self.tick_count
            else:
                v.lat, v.lon = interpolate(p1, p2, v.progress)
            return

        # already at waiting zone: increment wait time, try to assign a bay
        v.status = VehicleStatus.WAITING
        v.waiting_time_min = round(v.waiting_time_min + 0.35, 1)
        v.speed_kmh = 0.0

        free_bay = next((b for b, occ in self.bay_occupancy.items() if occ is None), None)
        if free_bay:
            self.bay_occupancy[free_bay] = v.id
            v.assigned_bay = free_bay
            v.route_index += 1  # move to bay leg
            v.progress = 0.0

    def _handle_bay(self, v: Vehicle, p1, p2, step, next_key, current_key) -> None:
        target_bay = v.assigned_bay or next_key
        if current_key != target_bay and v.route[v.route_index] == "WAITING_ZONE":
            # travelling from waiting zone toward the assigned bay
            p2 = (SITE_POINTS[target_bay]["lat"], SITE_POINTS[target_bay]["lon"])
            v.progress += step
            v.status = VehicleStatus.MOVING
            if v.progress >= 1.0:
                v.progress = 0.0
                v.route_index += 1
                v.lat, v.lon = p2
                v.status = VehicleStatus.LOADING
                v.loading_ticks = 0
            else:
                v.lat, v.lon = interpolate(p1, p2, v.progress)
            return

        # at the bay: loading in progress
        v.status = VehicleStatus.LOADING
        v.speed_kmh = 0.0
        loading_ticks = getattr(v, "loading_ticks", 0) + 1
        v.loading_ticks = loading_ticks
        if loading_ticks > random.randint(6, 10):
            self.bay_occupancy[target_bay] = None
            v.route_index += 1
            v.progress = 0.0
            v.status = VehicleStatus.EXITING

    def _spawn_vehicle(self) -> None:
        route = ROUTE_GATE_B if self.gate_b_redirect_active else random.choice([ROUTE_GATE_A, ROUTE_GATE_B])
        entry = SITE_POINTS["ENTRY"]
        v = Vehicle(
            id=f"TRUCK-{self.next_truck_number:03d}",
            plate=_plate(),
            driver=random.choice(["Moussa Diop", "Ibrahima Fall", "Cheikh Ndiaye", "Ousmane Sarr", "Babacar Gueye"]),
            cargo=random.choice(CARGO_TYPES),
            status=VehicleStatus.APPROACHING,
            route=route,
            route_index=0,
            progress=0.0,
            lat=entry["lat"], lon=entry["lon"],
            speed_kmh=round(random.uniform(10, 20), 1),
            arrival_time=dt.datetime.now().strftime("%H:%M"),
        )
        self.next_truck_number += 1
        self.fleet.append(v)

    # ------------------------------------------------------------------
    def waiting_vehicles(self) -> List[Vehicle]:
        return [v for v in self.active_vehicles() if v.status == VehicleStatus.WAITING]

    def loading_vehicles(self) -> List[Vehicle]:
        return [v for v in self.active_vehicles() if v.status == VehicleStatus.LOADING]

    def trigger_arrival_rush(self, count: int = 6) -> None:
        for _ in range(count):
            self._spawn_vehicle()
            # push them straight near the gate/waiting zone for immediate visible effect
            v = self.fleet[-1]
            v.route_index = 3
            v.progress = 0.0
            wp = SITE_POINTS[v.route[3]]
            v.lat, v.lon = wp["lat"], wp["lon"]

    def redirect_to_gate_b(self, active: bool = True) -> None:
        self.gate_b_redirect_active = active