"""
SOCOCIM SmartFlow — Alert Service.
In-memory alert lifecycle: creation, deduplication, acknowledge, resolve.
No database — alerts live for the duration of the session, as specified.

IMPORTANT (i18n): alerts store a Recommendation (translation keys + data),
never final text, so an alert raised while the UI was in one language still
displays correctly after the user switches language.
"""
from __future__ import annotations
import datetime as dt
import itertools
from dataclasses import dataclass, field
from typing import List, Optional

from utils.constants import Severity, AlertStatus, AlertSource
from services.recommendation_service import Recommendation

_counter = itertools.count(1)


@dataclass
class Alert:
    id: str
    severity: Severity
    source: AlertSource
    subject: str          # equipment id/name, vehicle id, or a translatable static phrase
    rec: Recommendation
    status: AlertStatus = AlertStatus.NEW
    created_at: str = field(default_factory=lambda: dt.datetime.now().strftime("%H:%M:%S"))
    created_ts: float = field(default_factory=lambda: dt.datetime.now().timestamp())

    def message(self, language: str = "fr") -> str:
        return self.rec.message(language)

    def recommendation(self, language: str = "fr") -> str:
        return self.rec.action(language)


class AlertService:
    def __init__(self):
        self.alerts: List[Alert] = []
        self._active_keys = set()  # (source, subject, message_key, params) currently open, avoids duplicate spam

    @staticmethod
    def _dedup_key(source: AlertSource, subject: str, rec: Recommendation):
        return (source, subject, rec.message_key, tuple(sorted(rec.message_params.items())))

    def raise_alert(self, severity: Severity, source: AlertSource, subject: str,
                     rec: Recommendation) -> Optional[Alert]:
        key = self._dedup_key(source, subject, rec)
        if key in self._active_keys:
            return None  # avoid flooding duplicate alerts every tick
        alert = Alert(
            id=f"ALT-{next(_counter):04d}",
            severity=severity, source=source, subject=subject, rec=rec,
        )
        self.alerts.insert(0, alert)
        self._active_keys.add(key)
        return alert

    def clear_subject(self, source: AlertSource, subject: str) -> None:
        """Clear all active-keys for a subject (e.g. equipment restored to normal)."""
        self._active_keys = {k for k in self._active_keys if not (k[0] == source and k[1] == subject)}

    def acknowledge(self, alert_id: str) -> None:
        for a in self.alerts:
            if a.id == alert_id and a.status == AlertStatus.NEW:
                a.status = AlertStatus.ACKNOWLEDGED

    def resolve(self, alert_id: str) -> None:
        for a in self.alerts:
            if a.id == alert_id:
                a.status = AlertStatus.RESOLVED

    def active_alerts(self) -> List[Alert]:
        return [a for a in self.alerts if a.status != AlertStatus.RESOLVED]

    def critical_count(self) -> int:
        return len([a for a in self.active_alerts() if a.severity == Severity.CRITICAL])

    def filtered(self, severity: Optional[str] = None, source: Optional[str] = None) -> List[Alert]:
        result = self.alerts
        if severity and severity != "ALL":
            result = [a for a in result if a.severity.value == severity]
        if source and source != "ALL":
            result = [a for a in result if a.source.value == source]
        return result