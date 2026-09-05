"""
SOCOCIM SmartFlow — Recommendation Engine.
Pure rule-based business logic (no LLM required) simulating the
"intelligence" layer of the platform.

IMPORTANT (i18n): this module never returns final display strings. It
returns a Recommendation object holding translation keys + the raw data
needed to fill in the templates (name, temperature, zone...). This lets
the SAME recommendation be rendered correctly in whichever language is
active *at display time* — including for alerts that were raised earlier
and are only rendered now.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from data.equipment import Equipment
from utils.constants import EquipmentStatus
from utils.i18n import t, tt


@dataclass
class Recommendation:
    title_key: str
    message_key: str
    message_params: dict = field(default_factory=dict)
    recommendation_key: str = ""
    recommendation_params: dict = field(default_factory=dict)

    def title(self, language: str = "fr") -> str:
        return t(self.title_key, language)

    def message(self, language: str = "fr") -> str:
        params = dict(self.message_params)
        if "bay" in params:
            params["bay"] = t(params["bay"], language)
        return tt(self.message_key, language, **params)

    def action(self, language: str = "fr") -> str:
        params = dict(self.recommendation_params)
        if "bay" in params:
            params["bay"] = t(params["bay"], language)
        if params:
            return tt(self.recommendation_key, language, **params)
        return tt(self.recommendation_key, language)


class RecommendationEngine:

    # ------------------------------------------------------------------
    # Maintenance recommendations
    # ------------------------------------------------------------------
    @staticmethod
    def for_equipment(eq: Equipment) -> Recommendation:
        th = eq.thresholds()
        vib_warn = th["vibration"]["warning"]
        temp_warn = th["temperature"]["warning"]

        if eq.status == EquipmentStatus.OFFLINE:
            return Recommendation(
                title_key="EQUIPMENT OFFLINE",
                message_key="msg_eq_offline",
                message_params={"name": eq.name},
                recommendation_key="rec_eq_offline",
            )

        if eq.vibration >= vib_warn and eq.temperature >= temp_warn:
            return Recommendation(
                title_key="CRITICAL: COMBINED THERMAL & VIBRATION FAULT",
                message_key="msg_combined_fault",
                message_params={
                    "name": eq.name, "temp": f"{eq.temperature:.1f}",
                    "vib": f"{eq.vibration:.1f}", "zone": eq.zone,
                },
                recommendation_key="rec_combined_fault",
            )
        if eq.vibration >= vib_warn:
            return Recommendation(
                title_key="HIGH VIBRATION DETECTED",
                message_key="msg_high_vibration",
                message_params={"name": eq.name, "vib": f"{eq.vibration:.1f}", "zone": eq.zone},
                recommendation_key="rec_high_vibration",
            )
        if eq.temperature >= temp_warn:
            return Recommendation(
                title_key="ABNORMAL TEMPERATURE RISE",
                message_key="msg_abnormal_temp",
                message_params={"name": eq.name, "temp": f"{eq.temperature:.1f}", "zone": eq.zone},
                recommendation_key="rec_abnormal_temp",
            )
        if eq.health_score < 75:
            return Recommendation(
                title_key="HEALTH SCORE DEGRADING",
                message_key="msg_health_degrading",
                message_params={"name": eq.name, "score": f"{eq.health_score:.0f}"},
                recommendation_key="rec_health_degrading",
            )
        return Recommendation(
            title_key="NOMINAL",
            message_key="msg_nominal",
            message_params={"name": eq.name},
            recommendation_key="rec_none",
        )

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
                        gate_b_available: bool) -> Optional[Recommendation]:
        if congestion_idx >= 60 and gate_b_available:
            return Recommendation(
                title_key="CONGESTION DETECTED — GATE A",
                message_key="msg_congestion_queue",
                message_params={"queue_len": queue_len, "avg_wait": f"{avg_wait:.0f}"},
                recommendation_key="rec_redirect_gate_b",
            )
        if congestion_idx >= 60:
            return Recommendation(
                title_key="HIGH CONGESTION — ALL GATES",
                message_key="msg_congestion_queue",
                message_params={"queue_len": queue_len, "avg_wait": f"{avg_wait:.0f}"},
                recommendation_key="rec_open_bay_or_pause",
            )
        if congestion_idx >= 35:
            return Recommendation(
                title_key="MODERATE CONGESTION",
                message_key="msg_congestion_building",
                message_params={"queue_len": queue_len, "avg_wait": f"{avg_wait:.0f}"},
                recommendation_key="rec_monitor_prepare",
            )
        return None

    @staticmethod
    def bay_assignment_hint(free_bay: str | None, vehicle_id: str | None) -> Optional[Recommendation]:
        if free_bay and vehicle_id:
            # free_bay is expected to be the canonical English bay name
            # (e.g. "Loading Bay 2") as found in utils.i18n STATIC_TRANSLATIONS;
            # translation happens lazily in .message()/.action() so the
            # correct language is used no matter when this gets rendered.
            return Recommendation(
                title_key="LOADING BAY AVAILABLE",
                message_key="msg_bay_available",
                message_params={"bay": free_bay},
                recommendation_key="rec_assign_bay",
                recommendation_params={"vehicle_id": vehicle_id, "bay": free_bay},
            )
        return None