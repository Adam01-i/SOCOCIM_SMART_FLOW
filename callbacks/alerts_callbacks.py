"""Alert Center callbacks: filtering, acknowledge, resolve (in-memory only)."""
from dash import Input, Output, State, html, ALL, ctx

from simulation.engine import ENGINE
from components.alert_card import alert_card
from utils.i18n import t


def register(app):

    @app.callback(
        Output("alert-list-container", "children"),
        Input("alerts-interval", "n_intervals"),
        Input("alert-severity-filter", "value"),
        Input("alert-source-filter", "value"),
        Input("language-store", "data"),
    )
    def _list_alerts(_n, severity, source, language):
        alerts = ENGINE.alert_service.filtered(severity=severity, source=source)
        if not alerts:
            return html.Div(t("No alerts match this filter.", language or "fr"), className="panel", style={"color": "var(--text-muted)"})
        return html.Div([alert_card(a, language=language or "fr") for a in alerts[:40]], className="panel")

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