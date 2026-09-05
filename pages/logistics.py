"""Smart Logistics — Fleet monitoring & flow optimization."""
from dash import html, dcc
from components.navbar import topbar
from utils.i18n import t


def layout(engine, language="fr"):
    return html.Div(
        [
            topbar("Smart Logistics", "Fleet monitoring & flow optimization", language),
            html.Div(id="logistics-kpi-grid", className="kpi-grid"),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(t("Site Map — Live Fleet Position", language), className="panel-title"),
                                    html.Span(t("OpenStreetMap", language), className="panel-tag"),
                                ],
                                className="panel-header",
                            ),
                            html.Div(
                                [
                                    html.Div(id="logistics-map-container", className="map-container"),
                                    html.Button(
                                        t("Plein écran", language),
                                        id="logistics-map-fullscreen",
                                        className="map-fullscreen-btn",
                                        title=t("Afficher la carte en plein écran", language),
                                        **{
                                            "data-target": "logistics-map-frame",
                                            "data-enter-label": t("Plein écran", language),
                                            "data-exit-label": t("Quitter le plein écran", language),
                                        },
                                    ),
                                ],
                                id="logistics-map-frame",
                                className="map-frame",
                            ),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(t("Queue Status", language), className="panel-title"),
                                    html.Div(id="logistics-congestion-tag"),
                                ],
                                className="panel-header",
                            ),
                            html.Div(id="logistics-queue-list"),
                            html.Div(className="divider"),
                            html.Div(id="logistics-queue-stats"),
                        ],
                        className="panel",
                    ),
                ],
                className="grid-2",
            ),

            html.Div(
                [
                    html.Div([html.Div(t("Fleet Table", language), className="panel-title")], className="panel-header"),
                    html.Div(
                        dcc.RadioItems(
                            id="fleet-filter",
                            options=[{"label": t(v, language), "value": v} for v in ["All", "Waiting", "Loading", "Moving", "Critical"]],
                            value="All",
                            inline=True,
                            className="filter-chip-row",
                            inputClassName="me-1",
                            labelStyle={"marginRight": "16px", "fontSize": "12.5px", "color": "var(--text-secondary)"},
                        ),
                    ),
                    html.Div(
                        html.Table(
                            [
                                html.Thead(html.Tr([
                                    html.Th(t(h, language))
                                    for h in ["Vehicle", "Plate", "Status", "Location", "Cargo", "Wait", "Speed", "Queue", "ETA"]
                                ])),
                                html.Tbody(id="fleet-table-body"),
                            ],
                            className="fleet-table",
                        ),
                        style={"overflowX": "auto"},
                    ),
                ],
                className="panel",
            ),

            dcc.Interval(id="logistics-interval", interval=2500, n_intervals=0),
        ]
    )