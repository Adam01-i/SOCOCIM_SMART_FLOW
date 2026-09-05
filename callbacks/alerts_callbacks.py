"""Alert Center callbacks: filtering, acknowledge, resolve (in-memory only)."""
from dash import Input, Output, State, html, ALL, ctx

from simulation.engine import ENGINE
from components.alert_card import alert_card


def register(app):

    @app.callback(
        Output("alert-list-container", "children"),
        Input("alerts-interval", "n_intervals"),
        Input("alert-severity-filter", "value"),
        Input("alert-source-filter", "value"),
    )
    def _list_alerts(_n, severity, source):
        alerts = ENGINE.alert_service.filtered(severity=severity, source=source)
        if not alerts:
            return html.Div("No alerts match this filter.", className="panel", style={"color": "var(--text-muted)"})
        return html.Div([alert_card(a) for a in alerts[:40]], className="panel")

    @app.callback(
        Output("alerts-interval", "disabled"),
        Input({"type": "ack-alert", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def _ack(n_clicks_list):
        triggered = ctx.triggered_id
        if triggered and any(n_clicks_list):
            ENGINE.alert_service.acknowledge(triggered["index"])
        return False

    @app.callback(
        Output("alerts-interval", "disabled", allow_duplicate=True),
        Input({"type": "resolve-alert", "index": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def _resolve(n_clicks_list):
        triggered = ctx.triggered_id
        if triggered and any(n_clicks_list):
            ENGINE.alert_service.resolve(triggered["index"])
        return False