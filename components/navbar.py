"""Topbar for SOCOCIM SmartFlow: page title, live clock, system status."""
from dash import html, dcc
from components.status_badge import system_status_pill


def topbar(page_title: str, page_subtitle: str = ""):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(page_title, className="topbar-title"),
                    html.Div(page_subtitle, className="topbar-subtitle") if page_subtitle else None,
                ],
                className="topbar-titles",
            ),
            html.Div(
                [
                    html.Div(id="live-clock", className="topbar-clock"),
                    html.Div(id="topbar-system-status"),
                ],
                className="topbar-right",
            ),
        ],
        className="topbar",
    )