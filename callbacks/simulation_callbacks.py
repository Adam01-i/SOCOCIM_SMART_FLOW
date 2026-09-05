"""Simulation Lab callbacks: scenario buttons, speed control, demo mode."""
from dash import Input, Output, State, html, ALL, ctx

from simulation.engine import ENGINE
from simulation.scenarios import run_maintenance_scenario, run_logistics_scenario
from components.alert_card import feed_event_row
from utils.i18n import t


def register(app):

    @app.callback(
        Output("simulation-log-feed", "children", allow_duplicate=True),
        Input({"type": "maintenance-scenario-btn", "index": ALL}, "n_clicks"),
        State("sim-equipment-target", "value"),
        State("language-store", "data"),
        prevent_initial_call=True,
    )
    def _run_maintenance(n_clicks_list, equipment_id, language):
        triggered = ctx.triggered_id
        if triggered and any(n_clicks_list):
            run_maintenance_scenario(ENGINE, triggered["index"], equipment_id)
        return [feed_event_row(ts, key, params, language or "fr") for ts, key, params in list(ENGINE.events)[:20]]

    @app.callback(
        Output("simulation-log-feed", "children", allow_duplicate=True),
        Input({"type": "logistics-scenario-btn", "index": ALL}, "n_clicks"),
        State("language-store", "data"),
        prevent_initial_call=True,
    )
    def _run_logistics(n_clicks_list, language):
        triggered = ctx.triggered_id
        if triggered and any(n_clicks_list):
            run_logistics_scenario(ENGINE, triggered["index"])
        return [feed_event_row(ts, key, params, language or "fr") for ts, key, params in list(ENGINE.events)[:20]]

    @app.callback(Output("simulation-log-feed", "children"), Input("simulation-page-interval", "n_intervals"), Input("language-store", "data"))
    def _refresh_log(_n, language):
        events = list(ENGINE.events)[:20]
        return [feed_event_row(ts, key, params, language or "fr") for ts, key, params in events] if events else html.Div(t("No events yet.", language or "fr"), className="text-muted")

    @app.callback(Output("simulation-speed", "value"), Input("simulation-speed", "value"))
    def _set_speed(speed):
        ENGINE.set_speed(speed)
        return speed

    @app.callback(
        Output("simulation-demo-banner", "children"),
        Input("btn-start-demo", "n_clicks"),
        Input("btn-stop-demo", "n_clicks"),
        Input("simulation-page-interval", "n_intervals"),
        Input("language-store", "data"),
        prevent_initial_call=False,
    )
    def _demo_mode(start_clicks, stop_clicks, _n, language):
        triggered = ctx.triggered_id
        if triggered == "btn-start-demo":
            ENGINE.toggle_demo_mode(True)
        elif triggered == "btn-stop-demo":
            ENGINE.toggle_demo_mode(False)
        if ENGINE.demo_mode:
            return html.Div(t("● DEMO MODE ACTIVE — scenario running automatically", language or "fr"), className="demo-banner")
        return None