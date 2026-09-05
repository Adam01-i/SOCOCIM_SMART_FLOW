"""
SOCOCIM SmartFlow — Industrial Intelligence Platform (Alpha)
Main application entrypoint.

Run with:
    python app.py
Then open http://127.0.0.1:8050
"""
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from components.sidebar import sidebar
from simulation.engine import ENGINE
from utils.constants import APP_TITLE

app = dash.Dash(
    __name__,
    title=f"{APP_TITLE} — Alpha",
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.DARKLY],
    update_title=None,
)
server = app.server

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),

        # Global simulation heartbeat — always mounted, drives ENGINE.update()
        dcc.Interval(id="global-tick-interval", interval=2000, n_intervals=0),
        dcc.Store(id="global-engine-tick", data=0),

        dcc.Store(id="language-store", storage_type="local", data="fr"),
        dcc.Store(id="theme-store", storage_type="local", data="dark"),

        html.Div(
            [
                html.Div(id="sidebar-container", children=sidebar("/", "fr")),
                html.Div(html.Div(id="page-content"), className="main-content"),
            ],
            id="app-shell",
            className="app-shell theme-dark",
        ),
    ]
)

# ---------------------------------------------------------------------------
# Register all callbacks
# ---------------------------------------------------------------------------
from callbacks import (
    navigation_callbacks,
    overview_callbacks,
    maintenance_callbacks,
    logistics_callbacks,
    control_center_callbacks,
    alerts_callbacks,
    analytics_callbacks,
    simulation_callbacks,
)

navigation_callbacks.register(app)
overview_callbacks.register(app)
maintenance_callbacks.register(app)
logistics_callbacks.register(app)
control_center_callbacks.register(app)
alerts_callbacks.register(app)
analytics_callbacks.register(app)
simulation_callbacks.register(app)


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)