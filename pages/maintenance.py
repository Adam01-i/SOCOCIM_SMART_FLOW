"""Smart Maintenance — Equipment health & predictive monitoring."""
from dash import html, dcc
from components.navbar import topbar


def layout(engine):
    return html.Div(
        [
            topbar("Smart Maintenance", "Equipment health & predictive monitoring"),
            html.Div(id="maintenance-kpi-grid", className="kpi-grid"),

            html.Div(
                [
                    html.Div("Equipment Fleet", className="section-label"),
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
                            html.Div([html.Div("Recommendation", className="panel-title")], className="panel-header"),
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
                            html.Div([html.Div("Temperature Trend (°C)", className="panel-title")], className="panel-header"),
                            dcc.Graph(id="maintenance-temp-chart", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div("Vibration Trend (mm/s)", className="panel-title")], className="panel-header"),
                            dcc.Graph(id="maintenance-vib-chart", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                ],
                className="grid-2-equal",
            ),

            html.Div(
                [
                    html.Div([html.Div("Health & Risk Evolution", className="panel-title")], className="panel-header"),
                    dcc.Graph(id="maintenance-health-risk-chart", config={"displayModeBar": False}),
                ],
                className="panel",
            ),

            dcc.Store(id="selected-equipment-store", data="EQ-MOT-07"),
            dcc.Interval(id="maintenance-interval", interval=2500, n_intervals=0),
        ]
    )