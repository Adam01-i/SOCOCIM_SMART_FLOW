"""Analytics — Maintenance & Logistics historical intelligence."""
from dash import html, dcc
from components.navbar import topbar


def layout(engine):
    return html.Div(
        [
            topbar("Analytics", "Historical intelligence across the site"),

            dcc.RadioItems(
                id="analytics-period",
                options=[{"label": v, "value": v} for v in ["Last Hour", "Today", "7 Days", "30 Days"]],
                value="Today", inline=True, className="filter-chip-row",
                labelStyle={"marginRight": "16px", "fontSize": "12.5px", "color": "var(--text-secondary)"},
            ),

            html.Div("Maintenance Analytics", className="section-label"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div([html.Div("Equipment Health Distribution", className="panel-title")], className="panel-header"),
                            dcc.Graph(id="an-health-distribution", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div("Anomalies by Equipment", className="panel-title")], className="panel-header"),
                            dcc.Graph(id="an-anomalies-by-equipment", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div("Maintenance Risk", className="panel-title")], className="panel-header"),
                            dcc.Graph(id="an-maintenance-risk", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                ],
                className="grid-3",
            ),

            html.Div("Logistics Analytics", className="section-label"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div([html.Div("Queue Evolution & Congestion History", className="panel-title")], className="panel-header"),
                            dcc.Graph(id="an-congestion-history", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div("Loading Bay Utilization", className="panel-title")], className="panel-header"),
                            dcc.Graph(id="an-bay-utilization", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                ],
                className="grid-2-equal",
            ),

            dcc.Interval(id="analytics-interval", interval=4000, n_intervals=0),
        ]
    )