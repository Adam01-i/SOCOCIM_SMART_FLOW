"""Overview page — KPI grid, operational pulse radar, live feed, snapshots."""
from dash import Input, Output, html
from dash.exceptions import PreventUpdate

from simulation.engine import ENGINE
from components.kpi_card import kpi_card
from components.alert_card import feed_event_row
from components.charts import composite_radar
from utils.constants import Colors
from utils.calculations import format_minutes
from utils.i18n import t, tt


def register(app):

    @app.callback(Output("overview-kpi-grid", "children"), Input("overview-interval", "n_intervals"), Input("language-store", "data"))
    def _overview_kpis(_n, language):
        m = ENGINE.maintenance.counts()
        avg_health = ENGINE.maintenance.average_health()
        log = ENGINE.logistics
        lc = log.counts()
        idx, level = log.congestion()
        avg_wait = log.average_wait()
        critical_alerts = ENGINE.alert_service.critical_count()

        return [
            kpi_card("Equipment Health", f"{avg_health:.1f}%", icon_letter="◈", accent=Colors.ACCENT,
                     sublabel=tt("sub_equipment_online", language or "fr", online=m["online"], total=m["total"]), language=language or "fr"),
            kpi_card("Active Equipment", f"{m['online']}/{m['total']}", icon_letter="⚙", accent=Colors.ACCENT_BLUE,
                     sublabel=tt("sub_warning_critical", language or "fr", warning=m["warning"], critical=m["critical"]), language=language or "fr"),
            kpi_card("Critical Alerts", str(critical_alerts), icon_letter="!", accent=Colors.CRITICAL,
                     sublabel=t("Requires attention" if critical_alerts else "All clear", language or "fr"), language=language or "fr"),
            kpi_card("Vehicles On Site", str(lc["on_site"]), icon_letter="▤", accent=Colors.ACCENT_PURPLE,
                     sublabel=tt("sub_waiting_loading", language or "fr", waiting=lc["waiting"], loading=lc["loading"]), language=language or "fr"),
            kpi_card("Avg Waiting Time", format_minutes(avg_wait), icon_letter="◷", accent=Colors.WARNING,
                     sublabel=tt("sub_max_wait", language or "fr", max=format_minutes(log.max_wait())), language=language or "fr"),
            kpi_card("Congestion Level", level, icon_letter="◎",
                     accent=(Colors.CRITICAL if level in ("HIGH", "CRITICAL") else (Colors.WARNING if level == "MODERATE" else Colors.SUCCESS)),
                     sublabel=tt("sub_index", language or "fr", idx=f"{idx:.0f}"), language=language or "fr"),
            kpi_card("Maintenance Risk", f"{ENGINE.maintenance.average_risk():.0f}/100", icon_letter="▲", accent=Colors.WARNING,
                     sublabel=tt("sub_critical_units", language or "fr", n=len(ENGINE.maintenance.critical_equipment())), language=language or "fr"),
            kpi_card("Operational Efficiency", f"{max(0, 100 - idx*0.3 - (100-avg_health)*0.4):.0f}%", icon_letter="✓", accent=Colors.SUCCESS,
                     sublabel=t("Composite site efficiency", language or "fr"), language=language or "fr"),
        ]

    @app.callback(Output("overview-pulse-radar", "figure"), Input("overview-interval", "n_intervals"), Input("language-store", "data"))
    def _overview_radar(_n, language):
        avg_health = ENGINE.maintenance.average_health()
        idx, _ = ENGINE.logistics.congestion()
        logistics_score = max(0, 100 - idx)
        m = ENGINE.maintenance.counts()
        alert_score = max(0, 100 - ENGINE.alert_service.critical_count() * 25 - len(ENGINE.alert_service.active_alerts()) * 5)
        throughput_score = min(100, ENGINE.logistics.throughput_last_hour_estimate() * 4)
        stability_score = max(0, 100 - m["critical"] * 20 - m["warning"] * 8)

        categories = ["Maintenance\nHealth", "Logistics\nFlow", "Alert\nControl", "Throughput", "Fleet\nStability"]
        values = [avg_health, logistics_score, alert_score, throughput_score, stability_score]
        return composite_radar(categories, [round(v, 1) for v in values])

    @app.callback(Output("overview-live-feed", "children"), Input("overview-interval", "n_intervals"), Input("language-store", "data"))
    def _overview_feed(_n, language):
        events = list(ENGINE.events)[:12]
        if not events:
            return html.Div("No recent events." if language != "fr" else "Aucun événement récent.", className="text-muted")
        return [feed_event_row(ts, key, params, language or "fr") for ts, key, params in events]

    @app.callback(Output("overview-maintenance-snapshot", "children"), Input("overview-interval", "n_intervals"), Input("language-store", "data"))
    def _maintenance_snapshot(_n, language):
        top_risk = ENGINE.maintenance.sorted_by_risk()[:4]
        rows = []
        for eq in top_risk:
            color = "var(--critical)" if eq.status.value == "CRITICAL" else ("var(--warning)" if eq.status.value == "WARNING" else "var(--success)")
            rows.append(
                html.Div(
                    [
                        html.Div(eq.name, style={"fontWeight": 700, "fontSize": "13px", "color": "var(--text-primary)", "flex": 1}),
                        html.Div(eq.zone, className="text-muted", style={"fontSize": "11.5px", "flex": 1}),
                        html.Div(f"{eq.health_score:.0f}%", style={"fontWeight": 700, "color": color, "fontFamily": "JetBrains Mono, monospace"}),
                    ],
                    style={"display": "flex", "alignItems": "center", "padding": "9px 4px", "borderBottom": "1px solid rgba(255,255,255,0.04)"},
                )
            )
        return rows

    @app.callback(Output("overview-logistics-snapshot", "children"), Input("overview-interval", "n_intervals"), Input("language-store", "data"))
    def _logistics_snapshot(_n, language):
        queue = ENGINE.logistics.waiting_queue()[:4]
        if not queue:
            return html.Div("No vehicles currently waiting." if language != "fr" else "Aucun véhicule en attente actuellement.", className="text-muted")
        rows = []
        for v in queue:
            rows.append(
                html.Div(
                    [
                        html.Div(v.id, style={"fontWeight": 700, "fontSize": "13px", "color": "var(--text-primary)", "flex": 1, "fontFamily": "JetBrains Mono, monospace"}),
                        html.Div(v.cargo, className="text-muted", style={"fontSize": "11.5px", "flex": 1}),
                        html.Div(format_minutes(v.waiting_time_min), style={"fontWeight": 700, "color": "var(--warning)", "fontFamily": "JetBrains Mono, monospace"}),
                    ],
                    style={"display": "flex", "alignItems": "center", "padding": "9px 4px", "borderBottom": "1px solid rgba(255,255,255,0.04)"},
                )
            )
        return rows