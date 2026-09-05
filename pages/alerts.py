"""Alert Center — filterable alert feed with acknowledge/resolve actions."""
from dash import html, dcc
from components.navbar import topbar
from utils.i18n import t


def layout(engine, language="fr"):
    return html.Div(
        [
            topbar("Alert Center", "All system alerts, in one place", language),

            html.Div(
                [
                    dcc.RadioItems(
                        id="alert-severity-filter",
                        options=[{"label": t(v, language), "value": v} for v in ["ALL", "INFO", "WARNING", "CRITICAL"]],
                        value="ALL", inline=True, className="filter-chip-row",
                        labelStyle={"marginRight": "16px", "fontSize": "12.5px", "color": "var(--text-secondary)"},
                    ),
                    dcc.RadioItems(
                        id="alert-source-filter",
                        options=[{"label": t(v, language), "value": v} for v in ["ALL", "MAINTENANCE", "LOGISTICS"]],
                        value="ALL", inline=True, className="filter-chip-row",
                        labelStyle={"marginRight": "16px", "fontSize": "12.5px", "color": "var(--text-secondary)"},
                    ),
                ],
                className="panel",
            ),

            html.Div(id="alert-list-container"),

            dcc.Interval(id="alerts-interval", interval=2500, n_intervals=0),
        ]
    )