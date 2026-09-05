"""
SOCOCIM SmartFlow — Vehicle data model and mocked truck fleet.
Later this can be fed by a RealGPSFleetService instead of mock generation.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import random

from utils.constants import VehicleStatus, SITE_POINTS, ROUTE_GATE_A, ROUTE_GATE_B, CARGO_TYPES

FIRST_NAMES = ["Moussa", "Ibrahima", "Cheikh", "Abdou", "Mamadou", "Ousmane", "Alioune",
               "Serigne", "Modou", "Babacar", "El Hadji", "Pape", "Lamine", "Souleymane"]
LAST_NAMES = ["Diop", "Fall", "Ndiaye", "Sarr", "Gueye", "Ba", "Diallo", "Sy", "Kane", "Faye", "Thiam", "Mbaye"]


@dataclass
class Vehicle:
    id: str
    plate: str
    driver: str
    cargo: str

    status: VehicleStatus = VehicleStatus.APPROACHING
    route: List[str] = field(default_factory=list)
    route_index: int = 0          # index of the waypoint the truck is heading towards
    progress: float = 0.0         # 0..1 progress between current and next waypoint
    lat: float = 0.0
    lon: float = 0.0

    speed_kmh: float = 0.0
    waiting_time_min: float = 0.0
    queue_position: Optional[int] = None
    assigned_bay: Optional[str] = None
    arrival_time: str = ""
    eta_min: float = 0.0

    entered_waiting_zone_at_tick: Optional[int] = None
    completed: bool = False


def _plate() -> str:
    return f"DK-{random.randint(1000, 9999)}-{random.choice('ABCDEFGH')}"


def build_initial_fleet(n: int = 18) -> List[Vehicle]:
    """Create the initial mocked truck fleet, staggered along the route so the
    site looks alive immediately rather than everyone starting at the gate."""
    fleet: List[Vehicle] = []
    entry = SITE_POINTS["ENTRY"]
    for i in range(n):
        route = ROUTE_GATE_A if i % 2 == 0 else ROUTE_GATE_B
        vid = f"TRUCK-{i+1:03d}"
        driver = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        cargo = random.choice(CARGO_TYPES)

        # Stagger starting waypoint index so trucks are spread across the site
        start_idx = random.randint(0, len(route) - 2)
        wp = SITE_POINTS[route[start_idx]]
        status = random.choice(
            [VehicleStatus.APPROACHING, VehicleStatus.AT_GATE, VehicleStatus.WAITING,
             VehicleStatus.WEIGHING, VehicleStatus.MOVING]
        )
        v = Vehicle(
            id=vid,
            plate=_plate(),
            driver=driver,
            cargo=cargo,
            status=status,
            route=route,
            route_index=start_idx,
            progress=random.random(),
            lat=wp["lat"], lon=wp["lon"],
            speed_kmh=round(random.uniform(5, 22), 1),
            waiting_time_min=round(random.uniform(0, 12), 1),
            arrival_time=f"{random.randint(6, 18):02d}:{random.randint(0,59):02d}",
        )
        fleet.append(v)
    return fleet