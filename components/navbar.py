"""Topbar for SOCOCIM SmartFlow: page title, live clock, system status."""
from dash import html, dcc
from components.status_badge import system_status_pill
from utils.i18n import t


def topbar(page_title: str, page_subtitle: str = "", language: str = "fr"):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(t(page_title, language), className="topbar-title"),
                    html.Div(t(page_subtitle, language), className="topbar-subtitle") if page_subtitle else None,
                ],
                className="topbar-titles",
            ),
            html.Div(
                [
                    html.Div(id="live-clock", className="topbar-clock"),
                    html.Div(id="topbar-system-status"),
                    html.Button("EN" if language == "fr" else "FR", id="language-toggle", className="topbar-control", title="Français / English"),
                    html.Button("☼", id="theme-toggle", className="topbar-control topbar-theme-control", title="Light / dark mode"),
                ],
                className="topbar-right",
            ),
        ],
        className="topbar",
    )