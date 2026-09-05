"""Reusable status / severity badge components."""
from dash import html
from utils.constants import STATUS_COLOR, SEVERITY_COLOR, VEHICLE_STATUS_COLOR, Colors


def status_badge(status, label: str = None):
    color = STATUS_COLOR.get(status, Colors.TEXT_MUTED)
    text = label or (status.value if hasattr(status, "value") else str(status))
    return html.Span(
        [html.Span(className="badge-dot", style={"backgroundColor": color}), text],
        className="status-badge",
        style={"color": color, "borderColor": color + "40", "backgroundColor": color + "1A"},
    )


def severity_badge(severity, label: str = None):
    color = SEVERITY_COLOR.get(severity, Colors.TEXT_MUTED)
    text = label or (severity.value if hasattr(severity, "value") else str(severity))
    return html.Span(
        text,
        className="severity-badge",
        style={"color": color, "borderColor": color + "50", "backgroundColor": color + "1A"},
    )


def vehicle_status_badge(status, label: str = None):
    color = VEHICLE_STATUS_COLOR.get(status, Colors.TEXT_MUTED)
    text = label or (status.value if hasattr(status, "value") else str(status)).replace("_", " ")
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