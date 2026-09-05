"""Routing, sidebar state, topbar clock/status, and the global simulation heartbeat."""
import datetime as dt
from dash import Input, Output, State, html, ctx

from components.sidebar import sidebar
from components.status_badge import system_status_pill
from utils.i18n import t
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


def _apply_preference_click(triggered_id, language_clicks, theme_clicks, language, theme):
    language = language or "fr"
    theme = theme or "dark"
    if triggered_id == "language-toggle" and (language_clicks or 0) > 0:
        language = "fr" if language == "en" else "en"
    elif triggered_id == "theme-toggle" and (theme_clicks or 0) > 0:
        theme = "light" if theme == "dark" else "dark"
    return language, theme


def register(app):

    @app.callback(Output("global-engine-tick", "data"), Input("global-tick-interval", "n_intervals"))
    def _advance_engine(n):
        ENGINE.update()
        return n or 0

    @app.callback(Output("sidebar-container", "children"), Input("url", "pathname"), Input("language-store", "data"))
    def _render_sidebar(pathname, language):
        return sidebar(pathname or "/", language or "fr")

    @app.callback(Output("page-content", "children"), Input("url", "pathname"), Input("language-store", "data"))
    def _render_page(pathname, language):
        module = PAGES.get(pathname, overview)
        return module.layout(ENGINE, language or "fr")

    @app.callback(
        Output("language-store", "data"),
        Output("theme-store", "data"),
        Input("language-toggle", "n_clicks"),
        Input("theme-toggle", "n_clicks"),
        State("language-store", "data"),
        State("theme-store", "data"),
        prevent_initial_call=True,
    )
    def _update_preferences(_language_clicks, _theme_clicks, language, theme):
        return _apply_preference_click(ctx.triggered_id, _language_clicks, _theme_clicks, language, theme)

    @app.callback(Output("app-shell", "className"), Input("theme-store", "data"))
    def _apply_theme(theme):
        return "app-shell theme-light" if theme == "light" else "app-shell theme-dark"

    @app.callback(Output("live-clock", "children"), Input("global-engine-tick", "data"), Input("language-store", "data"))
    def _update_clock(_n, language):
        now = dt.datetime.now()
        return [html.Span(f"{t('LIVE', language or 'fr')}  ", style={"color": "var(--accent)", "fontWeight": 700}), now.strftime("%d %b %Y  %H:%M:%S").upper()]

    @app.callback(Output("topbar-system-status", "children"), Input("global-engine-tick", "data"), Input("language-store", "data"))
    def _update_topbar_status(_n, language):
        label = ENGINE.system_status_label()
        ok = label == "SYSTEM OPERATIONAL"
        return system_status_pill(f"● {t(label, language or 'fr')}", ok=ok)