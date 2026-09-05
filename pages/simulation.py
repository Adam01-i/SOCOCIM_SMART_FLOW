"""Simulation Lab — manual scenario triggers, anomaly injection, demo mode."""
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.navbar import topbar
from simulation.scenarios import MAINTENANCE_SCENARIOS, LOGISTICS_SCENARIOS
from data.equipment import build_initial_fleet


def layout(engine):
    equipment_options = [{"label": eq.name, "value": eq.id} for eq in engine.equipment]

    return html.Div(
        [
            topbar("Simulation Lab", "Trigger scenarios for demonstration and testing"),

            html.Div(id="simulation-demo-banner"),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Demo Mode", className="panel-title"),
                            html.Div("Auto-run the full storytelling script", className="panel-subtitle"),
                        ]
                    ),
                    dbc.Button("Start Demo Mode", id="btn-start-demo", className="control-btn control-btn-primary", n_clicks=0),
                    dbc.Button("Stop Demo Mode", id="btn-stop-demo", className="control-btn", n_clicks=0, style={"marginLeft": "8px"}),
                ],
                className="panel",
                style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"},
            ),

            html.Div(
                [
                    html.Div("Simulation Speed", className="section-label"),
                    dcc.RadioItems(
                        id="simulation-speed",
                        options=[{"label": f"{s}x", "value": s} for s in [1, 2, 5, 10]],
                        value=1, inline=True, className="filter-chip-row",
                        labelStyle={"marginRight": "18px", "fontSize": "13px", "color": "var(--text-secondary)"},
                    ),
                ],
                className="panel",
            ),

            html.Div(
                [
                    html.Div("Smart Maintenance Scenarios", className="section-label"),
                    dcc.Dropdown(
                        id="sim-equipment-target",
                        options=equipment_options,
                        value="EQ-MOT-07",
                        clearable=False,
                        style={"maxWidth": "320px", "marginBottom": "14px"},
                        className="mono",
                    ),
                    html.Div(
                        [
                            dbc.Button(s, id={"type": "maintenance-scenario-btn", "index": s},
                                       className="control-btn" + (" control-btn-danger" if "Critical" in s or "Failure" in s else ""),
                                       n_clicks=0, style={"marginRight": "8px", "marginBottom": "8px"})
                            for s in MAINTENANCE_SCENARIOS
                        ],
                    ),
                ],
                className="panel",
            ),

            html.Div(
                [
                    html.Div("Smart Logistics Scenarios", className="section-label"),
                    html.Div(
                        [
                            dbc.Button(s, id={"type": "logistics-scenario-btn", "index": s},
                                       className="control-btn" + (" control-btn-danger" if "Failure" in s or "Emergency" in s else ""),
                                       n_clicks=0, style={"marginRight": "8px", "marginBottom": "8px"})
                            for s in LOGISTICS_SCENARIOS
                        ],
                    ),
                ],
                className="panel",
            ),

            html.Div(
                [
                    html.Div([html.Div("Simulation Log", className="panel-title")], className="panel-header"),
                    html.Div(id="simulation-log-feed", className="feed-container"),
                ],
                className="panel",
            ),

            dcc.Interval(id="simulation-page-interval", interval=2000, n_intervals=0),
        ]
    )