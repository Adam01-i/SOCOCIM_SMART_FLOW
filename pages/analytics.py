"""Analytics — Maintenance & Logistics historical intelligence."""
from dash import html, dcc
from components.navbar import topbar
from utils.i18n import t


def layout(engine, language="fr"):
    return html.Div(
        [
            topbar("Analytics", "Historical intelligence across the site", language),

            dcc.RadioItems(
                id="analytics-period",
                options=[{"label": t(v, language), "value": v} for v in ["Last Hour", "Today", "7 Days", "30 Days"]],
                value="Today", inline=True, className="filter-chip-row",
                labelStyle={"marginRight": "16px", "fontSize": "12.5px", "color": "var(--text-secondary)"},
            ),

            html.Div(t("Maintenance Analytics", language), className="section-label"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div([html.Div(t("Equipment Health Distribution", language), className="panel-title")], className="panel-header"),
                            dcc.Graph(id="an-health-distribution", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div(t("Anomalies by Equipment", language), className="panel-title")], className="panel-header"),
                            dcc.Graph(id="an-anomalies-by-equipment", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div(t("Maintenance Risk", language), className="panel-title")], className="panel-header"),
                            dcc.Graph(id="an-maintenance-risk", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                ],
                className="grid-3",
            ),

            html.Div(t("Logistics Analytics", language), className="section-label"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div([html.Div(t("Queue Evolution & Congestion History", language), className="panel-title")], className="panel-header"),
                            dcc.Graph(id="an-congestion-history", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div(t("Loading Bay Utilization", language), className="panel-title")], className="panel-header"),
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