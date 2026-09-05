"""Simulation Lab callbacks: scenario buttons, speed control, demo mode."""
from dash import Input, Output, State, html, ALL, ctx

from simulation.engine import ENGINE
from simulation.scenarios import run_maintenance_scenario, run_logistics_scenario
from components.alert_card import feed_event_row


def register(app):

    @app.callback(
        Output("simulation-log-feed", "children", allow_duplicate=True),
        Input({"type": "maintenance-scenario-btn", "index": ALL}, "n_clicks"),
        State("sim-equipment-target", "value"),
        prevent_initial_call=True,
    )
    def _run_maintenance(n_clicks_list, equipment_id):
        triggered = ctx.triggered_id
        if triggered and any(n_clicks_list):
            run_maintenance_scenario(ENGINE, triggered["index"], equipment_id)
        return [feed_event_row(ts, msg) for ts, msg in list(ENGINE.events)[:20]]

    @app.callback(
        Output("simulation-log-feed", "children", allow_duplicate=True),
        Input({"type": "logistics-scenario-btn", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def _run_logistics(n_clicks_list):
        triggered = ctx.triggered_id
        if triggered and any(n_clicks_list):
            run_logistics_scenario(ENGINE, triggered["index"])
        return [feed_event_row(ts, msg) for ts, msg in list(ENGINE.events)[:20]]

    @app.callback(Output("simulation-log-feed", "children"), Input("simulation-page-interval", "n_intervals"))
    def _refresh_log(_n):
        events = list(ENGINE.events)[:20]
        return [feed_event_row(ts, msg) for ts, msg in events] if events else html.Div("No events yet.", className="text-muted")

    @app.callback(Output("simulation-speed", "value"), Input("simulation-speed", "value"))
    def _set_speed(speed):
        ENGINE.set_speed(speed)
        return speed

    @app.callback(
        Output("simulation-demo-banner", "children"),
        Input("btn-start-demo", "n_clicks"),
        Input("btn-stop-demo", "n_clicks"),
        Input("simulation-page-interval", "n_intervals"),
        prevent_initial_call=False,
    )
    def _demo_mode(start_clicks, stop_clicks, _n):
        triggered = ctx.triggered_id
        if triggered == "btn-start-demo":
            ENGINE.toggle_demo_mode(True)
        elif triggered == "btn-stop-demo":
            ENGINE.toggle_demo_mode(False)
        if ENGINE.demo_mode:
            return html.Div("● DEMO MODE ACTIVE — scenario running automatically", className="demo-banner")
        return None