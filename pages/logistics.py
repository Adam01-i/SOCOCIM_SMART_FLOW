"""Smart Logistics — Fleet monitoring & flow optimization."""
from dash import html, dcc
from components.navbar import topbar


def layout(engine):
    return html.Div(
        [
            topbar("Smart Logistics", "Fleet monitoring & flow optimization"),
            html.Div(id="logistics-kpi-grid", className="kpi-grid"),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div("Site Map — Live Fleet Position", className="panel-title"),
                                    html.Span("OpenStreetMap", className="panel-tag"),
                                ],
                                className="panel-header",
                            ),
                            html.Div(id="logistics-map-container", className="map-container"),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div("Queue Status", className="panel-title"),
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
                    html.Div([html.Div("Fleet Table", className="panel-title")], className="panel-header"),
                    html.Div(
                        dcc.RadioItems(
                            id="fleet-filter",
                            options=[{"label": v, "value": v} for v in ["All", "Waiting", "Loading", "Moving", "Critical"]],
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
                                html.Thead(html.Tr([html.Th(h) for h in
                                    ["Vehicle", "Plate", "Status", "Location", "Cargo", "Wait", "Speed", "Queue", "ETA"]])),
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