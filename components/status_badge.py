"""Reusable status / severity badge components."""
from dash import html
from utils.constants import STATUS_COLOR, SEVERITY_COLOR, VEHICLE_STATUS_COLOR, Colors
from utils.i18n import t


def status_badge(status, label: str = None, language: str = "fr"):
    color = STATUS_COLOR.get(status, Colors.TEXT_MUTED)
    raw = status.value if hasattr(status, "value") else str(status)
    text = label if label is not None else t(raw, language)
    return html.Span(
        [html.Span(className="badge-dot", style={"backgroundColor": color}), text],
        className="status-badge",
        style={"color": color, "borderColor": color + "40", "backgroundColor": color + "1A"},
    )


def severity_badge(severity, label: str = None, language: str = "fr"):
    color = SEVERITY_COLOR.get(severity, Colors.TEXT_MUTED)
    raw = severity.value if hasattr(severity, "value") else str(severity)
    text = label if label is not None else t(raw, language)
    return html.Span(
        text,
        className="severity-badge",
        style={"color": color, "borderColor": color + "50", "backgroundColor": color + "1A"},
    )


def vehicle_status_badge(status, label: str = None, language: str = "fr"):
    color = VEHICLE_STATUS_COLOR.get(status, Colors.TEXT_MUTED)
    raw = status.value if hasattr(status, "value") else str(status)
    text = label if label is not None else t(raw, language)
    return html.Span(
        text,
        className="status-badge",
        style={"color": color, "borderColor": color + "40", "backgroundColor": color + "1A"},
    )


def system_status_pill(label: str, ok: bool = True):
    color = Colors.SUCCESS if ok else Colors.CRITICAL
    return html.Div(
        [
            html.Span(className="pulse-dot", style={"backgroundColor": color}),
            html.Span(label, style={"color": color, "fontWeight": 600, "letterSpacing": "0.06em"}),
        ],
        className="system-status-pill",
    )