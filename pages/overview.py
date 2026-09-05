"""Overview — Executive Dashboard (SmartFlow Operations Center)."""
from dash import html, dcc
from components.navbar import topbar
from components.kpi_card import kpi_card
from components.status_badge import system_status_pill


def layout(engine):
    m = engine.maintenance.counts()
    avg_health = engine.maintenance.average_health()
    log = engine.logistics
    log_counts = log.counts()
    idx, level = log.congestion()
    avg_wait = log.average_wait()

    status_label = engine.system_status_label()
    ok = status_label == "SYSTEM OPERATIONAL"

    return html.Div(
        [
            topbar("SmartFlow Operations Center", "Industrial Intelligence Platform"),
            html.Div(system_status_pill(f"● {status_label}", ok=ok), style={"marginBottom": "18px"}),

            html.Div(id="overview-kpi-grid", className="kpi-grid"),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div("SMARTFLOW OPERATIONAL PULSE", className="panel-title"),
                                            html.Div("Composite real-time site intelligence index", className="panel-subtitle"),
                                        ]
                                    ),
                                    html.Span("LIVE", className="panel-tag"),
                                ],
                                className="panel-header",
                            ),
                            dcc.Graph(id="overview-pulse-radar", config={"displayModeBar": False}),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div("Live Operations Feed", className="panel-title"),
                                    html.Span("AUTO", className="panel-tag"),
                                ],
                                className="panel-header",
                            ),
                            html.Div(id="overview-live-feed", className="feed-container"),
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
                            html.Div([html.Div("Maintenance Snapshot", className="panel-title")], className="panel-header"),
                            html.Div(id="overview-maintenance-snapshot"),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div("Logistics Snapshot", className="panel-title")], className="panel-header"),
                            html.Div(id="overview-logistics-snapshot"),
                        ],
                        className="panel",
                    ),
                ],
                className="grid-2-equal",
            ),

            dcc.Interval(id="overview-interval", interval=2500, n_intervals=0),
        ]
    )