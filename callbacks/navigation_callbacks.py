"""Routing, sidebar state, topbar clock/status, and the global simulation heartbeat."""
import datetime as dt
from dash import Input, Output, html, no_update
from dash.exceptions import PreventUpdate

from components.sidebar import sidebar
from components.status_badge import system_status_pill
from simulation.engine import ENGINE
from pages import overview, maintenance, logistics, control_center, alerts, analytics, simulation as simulation_page

PAGES = {
    "/": overview,
    "/maintenance": maintenance,
    "/logistics": logistics,
    "/control-center": control_center,
    "/alerts": alerts,
    "/analytics": analytics,
    "/simulation": simulation_page,
}


def register(app):

    @app.callback(Output("global-engine-tick", "data"), Input("global-tick-interval", "n_intervals"))
    def _advance_engine(n):
        ENGINE.update()
        return n or 0

    @app.callback(Output("sidebar-container", "children"), Input("url", "pathname"))
    def _render_sidebar(pathname):
        return sidebar(pathname or "/")

    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def _render_page(pathname):
        module = PAGES.get(pathname, overview)
        return module.layout(ENGINE)

    @app.callback(Output("live-clock", "children"), Input("global-engine-tick", "data"))
    def _update_clock(_n):
        now = dt.datetime.now()
        return [html.Span("LIVE  ", style={"color": "var(--accent)", "fontWeight": 700}), now.strftime("%d %b %Y  %H:%M:%S").upper()]

    @app.callback(Output("topbar-system-status", "children"), Input("global-engine-tick", "data"))
    def _update_topbar_status(_n):
        label = ENGINE.system_status_label()
        ok = label == "SYSTEM OPERATIONAL"
        return system_status_pill(f"● {label}", ok=ok)