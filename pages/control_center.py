"""SmartFlow Control Center — unified operational supervision view."""
from dash import html, dcc
from components.navbar import topbar
from components.status_badge import system_status_pill
from utils.i18n import t


def layout(engine, language="fr"):
    status_label = engine.system_status_label()
    ok = status_label == "SYSTEM OPERATIONAL"
    return html.Div(
        [
            topbar("SmartFlow Control Center", "Unified operational supervision", language),
            html.Div(system_status_pill(f"● {t(status_label, language)}", ok=ok), style={"marginBottom": "18px"}),

            html.Div(id="cc-kpi-grid", className="kpi-grid"),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div([html.Div(t("Site Map", language), className="panel-title")], className="panel-header"),
                            html.Div(
                                [
                                    html.Div(id="cc-map-container", className="map-container"),
                                    html.Button(
                                        t("Plein écran", language),
                                        id="cc-map-fullscreen",
                                        className="map-fullscreen-btn",
                                        title=t("Afficher la carte en plein écran", language),
                                        **{
                                            "data-target": "cc-map-frame",
                                            "data-enter-label": t("Plein écran", language),
                                            "data-exit-label": t("Quitter le plein écran", language),
                                        },
                                    ),
                                    html.Button(
                                        t("Actualiser la carte", language),
                                        id="cc-map-refresh",
                                        className="map-refresh-btn",
                                        title=t("Actualiser les positions des véhicules", language),
                                    ),
                                ],
                                id="cc-map-frame",
                                className="map-frame",
                            ),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div(t("Critical Equipment", language), className="panel-title")], className="panel-header"),
                            html.Div(id="cc-critical-equipment"),
                            html.Div(className="divider"),
                            html.Div([html.Div(t("Congestion", language), className="panel-title")], className="panel-header"),
                            html.Div(id="cc-congestion-block"),
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
                            html.Div([html.Div(t("Live Operations Feed", language), className="panel-title")], className="panel-header"),
                            html.Div(id="cc-live-feed", className="feed-container"),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div(t("Active Recommendations", language), className="panel-title")], className="panel-header"),
                            html.Div(id="cc-recommendations"),
                        ],
                        className="panel",
                    ),
                ],
                className="grid-2-equal",
            ),

            dcc.Interval(id="cc-interval", interval=2500, n_intervals=0),
        ]
    )