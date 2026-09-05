"""Equipment health card — clickable, used on the Smart Maintenance page."""
from dash import html
from data.equipment import Equipment
from utils.constants import STATUS_COLOR
from components.status_badge import status_badge


def equipment_card(eq: Equipment, selected: bool = False):
    color = STATUS_COLOR.get(eq.status, "#5C6884")
    classes = "equipment-card" + (" equipment-card-selected" if selected else "")
    return html.Div(
        [
            html.Div(className="equipment-card-accent", style={"backgroundColor": color}),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(eq.name, className="equipment-card-name"),
                            html.Div(eq.zone, className="equipment-card-zone"),
                        ],
                    ),
                    status_badge(eq.status),
                ],
                className="equipment-card-header",
            ),
            html.Div(
                [
                    html.Div(
                        [html.Span(f"{eq.health_score:.0f}%", className="equipment-metric-value"),
                         html.Span("Health", className="equipment-metric-label")],
                        className="equipment-metric",
                    ),
                    html.Div(
                        [html.Span(f"{eq.temperature:.1f}°C", className="equipment-metric-value"),
                         html.Span("Temp", className="equipment-metric-label")],
                        className="equipment-metric",
                    ),
                    html.Div(
                        [html.Span(f"{eq.vibration:.1f}", className="equipment-metric-value"),
                         html.Span("Vib mm/s", className="equipment-metric-label")],
                        className="equipment-metric",
                    ),
                ],
                className="equipment-card-metrics",
            ),
            html.Div(
                html.Div(className="equipment-health-fill",
                         style={"width": f"{eq.health_score}%", "backgroundColor": color}),
                className="equipment-health-bar",
            ),
        ],
        className=classes,
        id={"type": "equipment-card", "index": eq.id},
        n_clicks=0,
    )