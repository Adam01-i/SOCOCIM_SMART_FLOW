"""Alert card component used in the Live Feed panel, Alert Center and Control Center."""
from dash import html
import dash_bootstrap_components as dbc
from services.alert_service import Alert
from utils.constants import Severity, SEVERITY_COLOR, AlertStatus
from components.status_badge import severity_badge


def alert_card(alert: Alert, compact: bool = False, show_actions: bool = True):
    color = SEVERITY_COLOR.get(alert.severity, "#5C6884")
    critical_pulse = "alert-card-critical-pulse" if alert.severity == Severity.CRITICAL and alert.status == AlertStatus.NEW else ""

    actions = None
    if show_actions and alert.status != AlertStatus.RESOLVED:
        actions = html.Div(
            [
                dbc.Button("Acknowledge", size="sm", className="alert-action-btn alert-action-ack",
                           id={"type": "ack-alert", "index": alert.id}, n_clicks=0,
                           disabled=(alert.status == AlertStatus.ACKNOWLEDGED)),
                dbc.Button("Resolve", size="sm", className="alert-action-btn alert-action-resolve",
                           id={"type": "resolve-alert", "index": alert.id}, n_clicks=0),
            ],
            className="alert-card-actions",
        )

    body = [
        html.Div(
            [
                severity_badge(alert.severity),
                html.Span(alert.subject, className="alert-card-subject"),
                html.Span(alert.created_at, className="alert-card-time"),
            ],
            className="alert-card-top",
        ),
        html.Div(alert.message, className="alert-card-message"),
    ]
    if not compact:
        body.append(
            html.Div(
                [html.Span("Recommendation: ", className="alert-card-rec-label"), alert.recommendation],
                className="alert-card-rec",
            )
        )
        body.append(
            html.Div(
                html.Span(alert.status.value, className=f"alert-status-tag alert-status-{alert.status.value.lower()}"),
                className="alert-card-status-row",
            )
        )
    if actions:
        body.append(actions)

    return html.Div(
        [html.Div(className="alert-card-accent", style={"backgroundColor": color}), html.Div(body, className="alert-card-body")],
        className=f"alert-card {critical_pulse}",
    )


def feed_event_row(timestamp: str, message: str):
    return html.Div(
        [
            html.Span(timestamp, className="feed-timestamp"),
            html.Span(message, className="feed-message"),
        ],
        className="feed-row",
    )