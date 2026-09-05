"""Overview — Executive Dashboard (SmartFlow Operations Center)."""
from dash import html, dcc
from components.navbar import topbar
from components.kpi_card import kpi_card
from components.status_badge import system_status_pill
from utils.i18n import t


def layout(engine, language="fr"):
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
            topbar("SmartFlow Operations Center", "Industrial Intelligence Platform", language),
            html.Div(system_status_pill(f"● {t(status_label, language)}", ok=ok), style={"marginBottom": "18px"}),

            html.Div(id="overview-kpi-grid", className="kpi-grid"),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(t("SMARTFLOW OPERATIONAL PULSE", language), className="panel-title"),
                                            html.Div(t("Composite real-time site intelligence index", language), className="panel-subtitle"),
                                        ]
                                    ),
                                    html.Span(t("LIVE", language), className="panel-tag"),
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
                                    html.Div(t("Live Operations Feed", language), className="panel-title"),
                                    html.Span(t("AUTO", language), className="panel-tag"),
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
                            html.Div([html.Div(t("Maintenance Snapshot", language), className="panel-title")], className="panel-header"),
                            html.Div(id="overview-maintenance-snapshot"),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div(t("Logistics Snapshot", language), className="panel-title")], className="panel-header"),
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