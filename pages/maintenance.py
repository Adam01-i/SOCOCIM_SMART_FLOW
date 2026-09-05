"""Smart Maintenance — Equipment health & predictive monitoring."""
from dash import html, dcc
from components.navbar import topbar
from utils.i18n import t


def layout(engine, language="fr"):
    return html.Div(
        [
            topbar("Smart Maintenance", "Equipment health & predictive monitoring", language),
            html.Div(id="maintenance-kpi-grid", className="kpi-grid"),

            html.Div(
                [
                    html.Div(t("Equipment Fleet", language), className="section-label"),
                    html.Div(id="maintenance-equipment-grid", className="equipment-grid"),
                ],
                className="panel",
            ),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(id="digital-view-panel"),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div(t("Recommendation", language), className="panel-title")], className="panel-header"),
                            html.Div(id="maintenance-recommendation-panel"),
                        ],
                        className="panel",
                    ),
                ],
                className="grid-2",
            ),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div([html.Div(t("Temperature Trend (°C)", language), className="panel-title")], className="panel-header"),
                            dcc.Graph(id="maintenance-temp-chart", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div(t("Vibration Trend (mm/s)", language), className="panel-title")], className="panel-header"),
                            dcc.Graph(id="maintenance-vib-chart", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                ],
                className="grid-2-equal",
            ),

            html.Div(
                [
                    html.Div([html.Div(t("Health & Risk Evolution", language), className="panel-title")], className="panel-header"),
                    dcc.Graph(id="maintenance-health-risk-chart", config={"displayModeBar": False}),
                ],
                className="panel",
            ),

            dcc.Store(id="selected-equipment-store", data="EQ-MOT-07"),
            dcc.Interval(id="maintenance-interval", interval=2500, n_intervals=0),
        ]
    )