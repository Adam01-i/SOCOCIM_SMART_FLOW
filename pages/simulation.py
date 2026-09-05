"""Simulation Lab — manual scenario triggers, anomaly injection, demo mode."""
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.navbar import topbar
from simulation.scenarios import MAINTENANCE_SCENARIOS, LOGISTICS_SCENARIOS
from data.equipment import build_initial_fleet
from utils.i18n import t


def layout(engine, language="fr"):
    equipment_options = [{"label": eq.name, "value": eq.id} for eq in engine.equipment]

    return html.Div(
        [
            topbar("Simulation Lab", "Trigger scenarios for demonstration and testing", language),

            html.Div(id="simulation-demo-banner"),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(t("Demo Mode", language), className="panel-title"),
                            html.Div(t("Auto-run the full storytelling script", language), className="panel-subtitle"),
                        ]
                    ),
                    dbc.Button(t("Start Demo Mode", language), id="btn-start-demo", className="control-btn control-btn-primary", n_clicks=0),
                    dbc.Button(t("Stop Demo Mode", language), id="btn-stop-demo", className="control-btn", n_clicks=0, style={"marginLeft": "8px"}),
                ],
                className="panel",
                style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"},
            ),

            html.Div(
                [
                    html.Div(t("Simulation Speed", language), className="section-label"),
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
                    html.Div(t("Smart Maintenance Scenarios", language), className="section-label"),
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
                            # value/id stay in canonical English (matched against
                            # simulation/scenarios.py logic); only the visible label
                            # is translated.
                            dbc.Button(t(s, language), id={"type": "maintenance-scenario-btn", "index": s},
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
                    html.Div(t("Smart Logistics Scenarios", language), className="section-label"),
                    html.Div(
                        [
                            dbc.Button(t(s, language), id={"type": "logistics-scenario-btn", "index": s},
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
                    html.Div([html.Div(t("Simulation Log", language), className="panel-title")], className="panel-header"),
                    html.Div(id="simulation-log-feed", className="feed-container"),
                ],
                className="panel",
            ),

            dcc.Interval(id="simulation-page-interval", interval=2000, n_intervals=0),
        ]
    )