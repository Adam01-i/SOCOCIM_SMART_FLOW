"""SmartFlow Control Center — unified operational supervision view."""
from dash import html, dcc
from components.navbar import topbar
from components.status_badge import system_status_pill


def layout(engine):
    status_label = engine.system_status_label()
    ok = status_label == "SYSTEM OPERATIONAL"
    return html.Div(
        [
            topbar("SmartFlow Control Center", "Unified operational supervision"),
            html.Div(system_status_pill(f"● {status_label}", ok=ok), style={"marginBottom": "18px"}),

            html.Div(id="cc-kpi-grid", className="kpi-grid"),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div([html.Div("Site Map", className="panel-title")], className="panel-header"),
                            html.Div(id="cc-map-container", className="map-container"),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div("Critical Equipment", className="panel-title")], className="panel-header"),
                            html.Div(id="cc-critical-equipment"),
                            html.Div(className="divider"),
                            html.Div([html.Div("Congestion", className="panel-title")], className="panel-header"),
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
                            html.Div([html.Div("Live Operations Feed", className="panel-title")], className="panel-header"),
                            html.Div(id="cc-live-feed", className="feed-container"),
                        ],
                        className="panel",
                    ),
                    html.Div(
                        [
                            html.Div([html.Div("Active Recommendations", className="panel-title")], className="panel-header"),
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