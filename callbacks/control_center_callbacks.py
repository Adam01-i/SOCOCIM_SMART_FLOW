"""Control Center callbacks — unified supervision combining both modules."""
from dash import Input, Output, html

from simulation.engine import ENGINE
from components.kpi_card import kpi_card
from components.alert_card import feed_event_row, alert_card
from callbacks.logistics_callbacks import _build_map
from utils.constants import Colors
from utils.calculations import format_minutes
from utils.i18n import t


def register(app):

    @app.callback(Output("cc-kpi-grid", "children"), Input("cc-interval", "n_intervals"), Input("language-store", "data"))
    def _kpis(_n, language):
        m = ENGINE.maintenance.counts()
        idx, level = ENGINE.logistics.congestion()
        avg_health = ENGINE.maintenance.average_health()
        critical_alerts = ENGINE.alert_service.critical_count()
        return [
            kpi_card("Equipment Health", f"{avg_health:.1f}%", icon_letter="◈", accent=Colors.ACCENT, language=language or "fr"),
            kpi_card("Critical Equipment", str(m["critical"]), icon_letter="!", accent=Colors.CRITICAL, language=language or "fr"),
            kpi_card("Congestion Index", f"{idx:.0f}/100", icon_letter="◎",
                     accent=(Colors.CRITICAL if level in ("HIGH", "CRITICAL") else Colors.WARNING if level == "MODERATE" else Colors.SUCCESS),
                     sublabel=t(level, language or "fr"), language=language or "fr"),
            kpi_card("Critical Alerts", str(critical_alerts), icon_letter="◉", accent=Colors.CRITICAL, language=language or "fr"),
        ]

    @app.callback(Output("cc-map-container", "children"), Input("cc-interval", "n_intervals"), Input("language-store", "data"))
    def _map(_n, language):
        return _build_map("cc-map", height="380px", language=language or "fr")

    @app.callback(Output("cc-critical-equipment", "children"), Input("cc-interval", "n_intervals"), Input("language-store", "data"))
    def _critical_equipment(_n, language):
        crit = ENGINE.maintenance.critical_equipment()
        if not crit:
            return html.Div(t("No critical equipment at this time.", language or "fr"), className="text-muted", style={"fontSize": "12.5px"})
        rows = []
        for eq in crit:
            rows.append(
                html.Div(
                    [
                        html.Div(eq.name, style={"fontWeight": 700, "color": "var(--critical)", "fontSize": "13px"}),
                        html.Div(f"{eq.zone} · {t('Health', language or 'fr')} {eq.health_score:.0f}%", className="text-muted", style={"fontSize": "11px"}),
                    ],
                    style={"padding": "8px 4px", "borderBottom": "1px solid rgba(255,255,255,0.04)"},
                )
            )
        return rows

    @app.callback(Output("cc-congestion-block", "children"), Input("cc-interval", "n_intervals"), Input("language-store", "data"))
    def _congestion_block(_n, language):
        idx, level = ENGINE.logistics.congestion()
        color = "var(--critical)" if level in ("HIGH", "CRITICAL") else ("var(--warning)" if level == "MODERATE" else "var(--success)")
        return html.Div(
            [
                html.Div(f"{idx:.0f}/100", style={"fontSize": "26px", "fontWeight": 800, "color": color, "fontFamily": "JetBrains Mono, monospace"}),
                html.Div(f"{t(level, language or 'fr')} · {len(ENGINE.logistics.waiting_queue())} {t('vehicles waiting', language or 'fr')}, {t('avg', language or 'fr')} {format_minutes(ENGINE.logistics.average_wait())}",
                         className="text-muted", style={"fontSize": "11.5px", "marginTop": "4px"}),
            ]
        )

    @app.callback(Output("cc-live-feed", "children"), Input("cc-interval", "n_intervals"), Input("language-store", "data"))
    def _feed(_n, language):
        events = list(ENGINE.events)[:14]
        return [feed_event_row(ts, key, params, language or "fr") for ts, key, params in events] if events else html.Div(t("No events yet.", language or "fr"), className="text-muted")

    @app.callback(Output("cc-recommendations", "children"), Input("cc-interval", "n_intervals"), Input("language-store", "data"))
    def _recommendations(_n, language):
        active = [a for a in ENGINE.alert_service.active_alerts()][:5]
        if not active:
            return html.Div(t("No active recommendations — operations nominal.", language or "fr"), className="text-muted", style={"fontSize": "12.5px"})
        return [alert_card(a, compact=True, show_actions=False, language=language or "fr") for a in active]