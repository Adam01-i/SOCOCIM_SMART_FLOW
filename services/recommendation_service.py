"""
SOCOCIM SmartFlow — Recommendation Engine.
Pure rule-based business logic (no LLM required) simulating the
"intelligence" layer of the platform.
"""
from __future__ import annotations
from data.equipment import Equipment
from utils.constants import EquipmentStatus


class RecommendationEngine:

    # ------------------------------------------------------------------
    # Maintenance recommendations
    # ------------------------------------------------------------------
    @staticmethod
    def for_equipment(eq: Equipment) -> tuple[str, str, str]:
        """Returns (title, message, recommendation) for the current equipment state."""
        th = eq.thresholds()
        vib_warn = th["vibration"]["warning"]
        temp_warn = th["temperature"]["warning"]

        if eq.status == EquipmentStatus.OFFLINE:
            return (
                "EQUIPMENT OFFLINE",
                f"{eq.name} sensor feed is currently unavailable.",
                "Dispatch a technician to verify sensor connectivity and equipment status on site.",
            )

        if eq.vibration >= vib_warn and eq.temperature >= temp_warn:
            return (
                "CRITICAL: COMBINED THERMAL & VIBRATION FAULT",
                f"{eq.name} shows simultaneous high temperature ({eq.temperature:.1f}\u00b0C) "
                f"and high vibration ({eq.vibration:.1f} mm/s) in {eq.zone}.",
                "Stop equipment for inspection within the next maintenance window. "
                "Check bearing assembly, lubrication and cooling circuit.",
            )
        if eq.vibration >= vib_warn:
            return (
                "HIGH VIBRATION DETECTED",
                f"{eq.name} vibration ({eq.vibration:.1f} mm/s) exceeded the recommended "
                f"operating range in {eq.zone}.",
                "Inspect bearing assembly and mounting within the next maintenance window.",
            )
        if eq.temperature >= temp_warn:
            return (
                "ABNORMAL TEMPERATURE RISE",
                f"{eq.name} temperature ({eq.temperature:.1f}\u00b0C) is increasing abnormally in {eq.zone}.",
                "Check lubrication levels and cooling system airflow.",
            )
        if eq.health_score < 75:
            return (
                "HEALTH SCORE DEGRADING",
                f"{eq.name} composite health score dropped to {eq.health_score:.0f}%.",
                "Schedule a preventive inspection during the next planned downtime.",
            )
        return ("NOMINAL", f"{eq.name} is operating within normal parameters.", "No action required.")

    @staticmethod
    def priority_for(eq: Equipment) -> str:
        if eq.status == EquipmentStatus.CRITICAL:
            return "HIGH"
        if eq.status == EquipmentStatus.WARNING:
            return "MEDIUM"
        return "LOW"

    # ------------------------------------------------------------------
    # Logistics recommendations
    # ------------------------------------------------------------------
    @staticmethod
    def for_congestion(congestion_idx: float, queue_len: int, avg_wait: float,
                        gate_b_available: bool) -> tuple[str, str, str] | None:
        if congestion_idx >= 60 and gate_b_available:
            return (
                "CONGESTION DETECTED — GATE A",
                f"Current queue: {queue_len} vehicles. Average wait: {avg_wait:.0f} min.",
                "Temporarily redirect incoming trucks to Gate B to balance the flow.",
            )
        if congestion_idx >= 60:
            return (
                "HIGH CONGESTION — ALL GATES",
                f"Current queue: {queue_len} vehicles. Average wait: {avg_wait:.0f} min.",
                "Open an additional loading bay or temporarily pause new arrivals.",
            )
        if congestion_idx >= 35:
            return (
                "MODERATE CONGESTION",
                f"Queue building up: {queue_len} vehicles waiting, average wait {avg_wait:.0f} min.",
                "Monitor closely; prepare Gate B redirection if trend continues.",
            )
        return None

    @staticmethod
    def bay_assignment_hint(free_bay: str | None, vehicle_id: str | None) -> tuple[str, str, str] | None:
        if free_bay and vehicle_id:
            return (
                "LOADING BAY AVAILABLE",
                f"{free_bay.replace('_', ' ').title()} is available.",
                f"Assign {vehicle_id} to {free_bay.replace('_', ' ').title()}.",
            )
        return None