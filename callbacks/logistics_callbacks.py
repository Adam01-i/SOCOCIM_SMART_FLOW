"""Smart Logistics page callbacks: KPI grid, live Leaflet map, queue, fleet table."""
from dash import Input, Output, State, html
import dash_leaflet as dl

from simulation.engine import ENGINE
from components.kpi_card import kpi_card
from components.vehicle_card import vehicle_table_row, queue_row
from utils.constants import SITE_POINTS, SITE_CENTER, VEHICLE_STATUS_COLOR, VehicleStatus, Colors
from utils.calculations import format_minutes
from utils.i18n import t

POINT_ICON_COLOR = {
    "entry": "#3D8BFF", "gate": "#8B7CF6", "checkpoint": "#FFB020",
    "zone": "#FF4757", "bay": "#00D4B8", "exit": "#5C6884",
}


def _build_map(map_id: str, height="480px", language="fr"):
    site_markers = []
    for key, pt in SITE_POINTS.items():
        color = POINT_ICON_COLOR.get(pt["type"], "#8B98B0")
        site_markers.append(
            dl.CircleMarker(
                center=(pt["lat"], pt["lon"]), radius=7, color=color, fillColor=color, fillOpacity=0.9, weight=2,
                children=[dl.Tooltip(t(pt["name"], language))],
            )
        )

    vehicle_markers = []
    for v in ENGINE.logistics.active():
        color = VEHICLE_STATUS_COLOR.get(v.status, "#8B98B0")
        vehicle_markers.append(
            dl.CircleMarker(
                center=(v.lat, v.lon), radius=5, color=color, fillColor=color, fillOpacity=1.0, weight=1,
                children=[dl.Tooltip(f"{v.id} — {t(v.status.value, language)} — {v.cargo}")],
            )
        )

    return dl.Map(
        [
            dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                         attribution='&copy; OpenStreetMap contributors'),
            dl.LayerGroup(site_markers),
            dl.LayerGroup(vehicle_markers, id=f"{map_id}-vehicles"),
        ],
        center=SITE_CENTER, zoom=16, id=map_id, style={"height": height, "width": "100%"},
    )


def register(app):

    @app.callback(Output("logistics-kpi-grid", "children"), Input("logistics-interval", "n_intervals"), Input("language-store", "data"))
    def _kpis(_n, language):
        counts = ENGINE.logistics.counts()
        idx, level = ENGINE.logistics.congestion()
        return [
            kpi_card("Vehicles On Site", str(counts["on_site"]), icon_letter="▤", accent=Colors.ACCENT, language=language or "fr"),
            kpi_card("Vehicles Waiting", str(counts["waiting"]), icon_letter="◷", accent=Colors.WARNING, language=language or "fr"),
            kpi_card("Vehicles Loading", str(counts["loading"]), icon_letter="▣", accent=Colors.ACCENT_BLUE, language=language or "fr"),
            kpi_card("Vehicles Exiting", str(counts["exiting"]), icon_letter="→", accent=Colors.TEXT_SECONDARY, language=language or "fr"),
            kpi_card("Average Waiting", format_minutes(ENGINE.logistics.average_wait()), icon_letter="◔", accent=Colors.WARNING, language=language or "fr"),
            kpi_card("Longest Waiting", format_minutes(ENGINE.logistics.max_wait()), icon_letter="◔", accent=Colors.CRITICAL, language=language or "fr"),
            kpi_card("Congestion Index", f"{idx:.0f}/100", icon_letter="◎", accent=(Colors.CRITICAL if level in ("HIGH","CRITICAL") else Colors.WARNING if level=="MODERATE" else Colors.SUCCESS), sublabel=t(level, language or "fr"), language=language or "fr"),
            kpi_card("Throughput / hour", str(ENGINE.logistics.throughput_last_hour_estimate()), icon_letter="⇄", accent=Colors.SUCCESS, language=language or "fr"),
        ]

    @app.callback(Output("logistics-map-container", "children"), Input("logistics-map-refresh", "n_clicks"), Input("language-store", "data"))
    def _map(_refresh_clicks, language):
        return _build_map("logistics-map", language=language or "fr")

    @app.callback(Output("logistics-congestion-tag", "children"), Input("logistics-interval", "n_intervals"), Input("language-store", "data"))
    def _congestion_tag(_n, language):
        idx, level = ENGINE.logistics.congestion()
        color = Colors.CRITICAL if level in ("HIGH", "CRITICAL") else (Colors.WARNING if level == "MODERATE" else Colors.SUCCESS)
        return html.Span(f"{t(level, language or 'en')} · {idx:.0f}/100", className="panel-tag", style={"color": color, "backgroundColor": color + "22"})

    @app.callback(Output("logistics-queue-list", "children"), Input("logistics-interval", "n_intervals"), Input("language-store", "data"))
    def _queue_list(_n, language):
        queue = ENGINE.logistics.waiting_queue()
        if not queue:
            return html.Div(t("No vehicles currently waiting.", language or "fr"), className="text-muted", style={"padding": "12px 4px"})
        return [queue_row(i + 1, v, language or "fr") for i, v in enumerate(queue[:8])]

    @app.callback(Output("logistics-queue-stats", "children"), Input("logistics-interval", "n_intervals"), Input("language-store", "data"))
    def _queue_stats(_n, language):
        log = ENGINE.logistics
        queue = log.waiting_queue()
        clearance = round(len(queue) * 3.2, 1)
        stats = [
            (t("Average wait", language or "fr"), format_minutes(log.average_wait())),
            (t("Max wait", language or "fr"), format_minutes(log.max_wait())),
            (t("Queue length", language or "fr"), str(len(queue))),
            (t("Est. clearance time", language or "fr"), format_minutes(clearance)),
        ]
        return html.Div(
            [html.Div([html.Span(k, className="text-muted", style={"fontSize": "11.5px"}),
                       html.Span(v, style={"fontWeight": 700, "fontFamily": "JetBrains Mono, monospace", "float": "right"})],
                      style={"padding": "6px 2px", "display": "flex", "justifyContent": "space-between"})
             for k, v in stats]
        )

    @app.callback(
        Output("fleet-table-body", "children"),
        Input("logistics-interval", "n_intervals"),
        State("fleet-filter", "value"),
        Input("language-store", "data"),
    )
    def _fleet_table(_n, language, fleet_filter):
        vehicles = ENGINE.logistics.active()
        if fleet_filter == "Waiting":
            vehicles = [v for v in vehicles if v.status == VehicleStatus.WAITING]
        elif fleet_filter == "Loading":
            vehicles = [v for v in vehicles if v.status == VehicleStatus.LOADING]
        elif fleet_filter == "Moving":
            vehicles = [v for v in vehicles if v.status == VehicleStatus.MOVING]
        elif fleet_filter == "Critical":
            vehicles = [v for v in vehicles if v.waiting_time_min > 20]
        vehicles = vehicles[:20]
        if not vehicles:
            return html.Tr(html.Td(t("No vehicles match this filter.", language or "fr"), colSpan=9, className="text-muted"))
        return [vehicle_table_row(v, language or "fr") for v in vehicles]