"""KPI card component used across Overview, Maintenance, Logistics pages."""
from dash import html
from utils.constants import Colors
from utils.i18n import t


def kpi_card(label: str, value: str, delta: str = None, delta_positive: bool = True,
             icon_letter: str = "•", accent: str = Colors.ACCENT, sublabel: str = None,
             language: str = "fr"):
    delta_el = None
    if delta:
        color = Colors.SUCCESS if delta_positive else Colors.CRITICAL
        arrow = "▲" if delta_positive else "▼"
        delta_el = html.Span(f"{arrow} {delta}", className="kpi-delta", style={"color": color})

    return html.Div(
        [
            html.Div(
                [
                    html.Div(icon_letter, className="kpi-icon", style={"backgroundColor": accent + "22", "color": accent}),
                    html.Div(t(label, language), className="kpi-label"),
                ],
                className="kpi-header",
            ),
            html.Div(
                [
                    html.Span(value, className="kpi-value"),
                    delta_el,
                ],
                className="kpi-value-row",
            ),
            html.Div(sublabel, className="kpi-sublabel") if sublabel else None,
        ],
        className="kpi-card",
    )