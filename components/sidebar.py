"""Premium sidebar navigation for SOCOCIM SmartFlow."""
from dash import html, dcc
from utils.i18n import t

NAV_SECTIONS = [
    {
        "title": None,
        "items": [("Overview", "/", "grid")],
    },
    {
        "title": "OPERATIONS",
        "items": [
            ("Smart Maintenance", "/maintenance", "gear"),
            ("Smart Logistics", "/logistics", "truck"),
            ("Control Center", "/control-center", "target"),
        ],
    },
    {
        "title": "INTELLIGENCE",
        "items": [
            ("Alerts", "/alerts", "bell"),
            ("Analytics", "/analytics", "chart"),
        ],
    },
    {
        "title": "SYSTEM",
        "items": [
            ("Simulation Lab", "/simulation", "flask"),
        ],
    },
]

ICONS = {
    "grid": "▦",
    "gear": "⚙",
    "truck": "▤",
    "target": "◎",
    "bell": "◈",
    "chart": "▪",
    "flask": "◇",
}


def sidebar(active_path: str = "/", language: str = "fr"):
    sections = []
    for section in NAV_SECTIONS:
        if section["title"]:
            sections.append(html.Div(t(section["title"], language), className="sidebar-section-title"))
        links = []
        for label, path, icon in section["items"]:
            is_active = (active_path == path)
            links.append(
                dcc.Link(
                    [
                        html.Span(ICONS.get(icon, "•"), className="sidebar-icon"),
                        html.Span(t(label, language), className="sidebar-label"),
                    ],
                    href=path,
                    className="sidebar-link" + (" sidebar-link-active" if is_active else ""),
                )
            )
        sections.append(html.Div(links, className="sidebar-links"))

    return html.Div(
        [
            html.Div(
                [
                    html.Div("SOCOCIM", className="sidebar-brand-main"),
                    html.Div("SMARTFLOW", className="sidebar-brand-sub"),
                ],
                className="sidebar-brand",
            ),
            html.Div(sections, className="sidebar-nav"),
            html.Div(
                [
                    html.Div(className="sidebar-footer-dot"),
                    html.Div(
                        [
                            html.Div(t("Industrial Intelligence", language), className="sidebar-footer-title"),
                            html.Div(t("Platform v0.1 — Alpha", language), className="sidebar-footer-sub"),
                        ]
                    ),
                ],
                className="sidebar-footer",
            ),
        ],
        className="sidebar",
    )