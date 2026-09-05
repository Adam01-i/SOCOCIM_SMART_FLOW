"""
SOCOCIM SmartFlow — Equipment data model and mocked equipment fleet.
This module defines the Equipment dataclass and the initial fleet.
Later, this can be fed by a RealIoTSensorService instead of mock generation.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from collections import deque

from utils.constants import EquipmentStatus, DEFAULT_THRESHOLDS, TYPE_THRESHOLD_OVERRIDES, HISTORY_LENGTH


@dataclass
class Equipment:
    id: str
    name: str
    type: str
    zone: str
    status: EquipmentStatus = EquipmentStatus.NORMAL

    temperature: float = 0.0
    vibration: float = 0.0
    humidity: float = 0.0

    temperature_baseline: float = 0.0
    vibration_baseline: float = 0.0
    humidity_baseline: float = 0.0

    health_score: float = 100.0
    risk_score: float = 0.0
    anomaly_confidence: float = 0.0

    operating_hours: float = 0.0
    last_update: str = ""
    last_inspection: str = ""
    estimated_maintenance: str = ""

    # Simulation-only internal state (anomaly injection tracking)
    anomaly_active: bool = False
    anomaly_target_temp: Optional[float] = None
    anomaly_target_vib: Optional[float] = None
    forced_offline: bool = False

    temperature_history: deque = field(default_factory=lambda: deque(maxlen=HISTORY_LENGTH))
    vibration_history: deque = field(default_factory=lambda: deque(maxlen=HISTORY_LENGTH))
    health_history: deque = field(default_factory=lambda: deque(maxlen=HISTORY_LENGTH))
    risk_history: deque = field(default_factory=lambda: deque(maxlen=HISTORY_LENGTH))
    timestamp_history: deque = field(default_factory=lambda: deque(maxlen=HISTORY_LENGTH))

    def thresholds(self) -> dict:
        return TYPE_THRESHOLD_OVERRIDES.get(self.type, DEFAULT_THRESHOLDS)


def build_initial_fleet() -> List[Equipment]:
    """Create the initial mocked, realistic equipment fleet for the plant."""
    specs = [
        ("EQ-MOT-01", "MOTOR-01", "MOTOR", "Raw Mill Area", 57, 2.2, 38),
        ("EQ-MOT-02", "MOTOR-02", "MOTOR", "Raw Mill Area", 55, 2.0, 40),
        ("EQ-MOT-07", "MOTOR-07", "MOTOR", "Raw Mill Area", 58, 2.4, 41),
        ("EQ-CRU-01", "CRUSHER-01", "CRUSHER", "Crushing Station", 62, 3.1, 35),
        ("EQ-CNV-01", "CONVEYOR-01", "CONVEYOR", "Clinker Transport", 48, 1.8, 44),
        ("EQ-CNV-02", "CONVEYOR-02", "CONVEYOR", "Clinker Transport", 50, 1.9, 43),
        ("EQ-PMP-01", "PUMP-01", "PUMP", "Cooling Circuit", 53, 2.1, 50),
        ("EQ-PMP-02", "PUMP-02", "PUMP", "Cooling Circuit", 54, 2.0, 49),
        ("EQ-FAN-01", "FAN-01", "FAN", "Kiln Ventilation", 46, 1.6, 33),
        ("EQ-MIX-01", "MIXER-01", "MIXER", "Cement Mixing", 60, 2.6, 29),
        ("EQ-MIX-03", "MIXER-03", "MIXER", "Cement Mixing", 61, 2.7, 30),
        ("EQ-CMP-01", "COMPRESSOR-01", "COMPRESSOR", "Pneumatic Systems", 59, 2.9, 37),
    ]
    fleet = []
    for idx, (eid, name, etype, zone, t_base, v_base, h_base) in enumerate(specs):
        eq = Equipment(
            id=eid, name=name, type=etype, zone=zone,
            temperature=t_base, vibration=v_base, humidity=h_base,
            temperature_baseline=t_base, vibration_baseline=v_base, humidity_baseline=h_base,
            health_score=round(94 - idx * 0.3, 1),
            operating_hours=round(4200 + idx * 137.5, 1),
            last_inspection="12 Aug 2026",
            estimated_maintenance="—",
        )
        fleet.append(eq)
    return fleet