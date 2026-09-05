"""
SOCOCIM SmartFlow — Named scenarios for the Simulation Lab page.
Each scenario is a thin wrapper calling into the SmartFlowSimulationEngine.
"""
from __future__ import annotations
from simulation.engine import SmartFlowSimulationEngine

DEFAULT_TARGET_EQUIPMENT = "EQ-MOT-07"

MAINTENANCE_SCENARIOS = [
    "Normal Operation",
    "High Temperature",
    "High Vibration",
    "Critical Failure",
    "Sensor Offline",
    "Restore System",
]

LOGISTICS_SCENARIOS = [
    "Normal Traffic",
    "Arrival Rush",
    "Gate Congestion",
    "Loading Bay Failure",
    "Emergency Queue",
    "Restore Traffic",
]


def run_maintenance_scenario(engine: SmartFlowSimulationEngine, scenario: str, equipment_id: str = None) -> None:
    eid = equipment_id or DEFAULT_TARGET_EQUIPMENT
    if scenario == "Normal Operation":
        engine.restore_normal_state()
    elif scenario == "High Temperature":
        engine.inject_temperature_anomaly(eid)
    elif scenario == "High Vibration":
        engine.inject_vibration_anomaly(eid)
    elif scenario == "Critical Failure":
        engine.simulate_equipment_failure(eid)
    elif scenario == "Sensor Offline":
        engine.set_equipment_offline(eid, True)
    elif scenario == "Restore System":
        engine.restore_normal_state()
        for eq in engine.equipment:
            engine.set_equipment_offline(eq.id, False)


def run_logistics_scenario(engine: SmartFlowSimulationEngine, scenario: str) -> None:
    if scenario == "Normal Traffic":
        engine.restore_traffic()
    elif scenario == "Arrival Rush":
        engine.trigger_arrival_rush(6)
    elif scenario == "Gate Congestion":
        engine.trigger_gate_congestion()
        engine.redirect_gate_b(False)
    elif scenario == "Loading Bay Failure":
        engine.trigger_bay_failure("BAY_2")
    elif scenario == "Emergency Queue":
        engine.trigger_arrival_rush(10)
    elif scenario == "Restore Traffic":
        engine.restore_traffic()