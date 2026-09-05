"""Smart Logistics page callbacks: KPI grid, live Leaflet map, queue, fleet table."""
from dash import Input, Output, State, html
import dash_leaflet as dl

from simulation.engine import ENGINE
from components.kpi_card import kpi_card
from components.vehicle_card import vehicle_table_row, queue_row
from utils.constants import SITE_POINTS, SITE_CENTER, VEHICLE_STATUS_COLOR, VehicleStatus, Colors
from utils.calculations import format_minutes

POINT_ICON_COLOR = {
    "entry": "#3D8BFF", "gate": "#8B7CF6", "checkpoint": "#FFB020",
    "zone": "#FF4757", "bay": "#00D4B8", "exit": "#5C6884",
}


def _build_map(map_id: str, height="480px"):
    site_markers = []
    for key, pt in SITE_POINTS.items():
        color = POINT_ICON_COLOR.get(pt["type"], "#8B98B0")
        site_markers.append(
            dl.CircleMarker(
                center=(pt["lat"], pt["lon"]), radius=7, color=color, fillColor=color, fillOpacity=0.9, weight=2,
                children=[dl.Tooltip(pt["name"])],
            )
        )

    vehicle_markers = []
    for v in ENGINE.logistics.active():
        color = VEHICLE_STATUS_COLOR.get(v.status, "#8B98B0")
        vehicle_markers.append(
            dl.CircleMarker(
                center=(v.lat, v.lon), radius=5, color=color, fillColor=color, fillOpacity=1.0, weight=1,
                children=[dl.Tooltip(f"{v.id} — {v.status.value.replace('_',' ').title()} — {v.cargo}")],
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

    @app.callback(Output("logistics-kpi-grid", "children"), Input("logistics-interval", "n_intervals"))
    def _kpis(_n):
        counts = ENGINE.logistics.counts()
        idx, level = ENGINE.logistics.congestion()
        return [
            kpi_card("Vehicles On Site", str(counts["on_site"]), icon_letter="▤", accent=Colors.ACCENT),
            kpi_card("Vehicles Waiting", str(counts["waiting"]), icon_letter="◷", accent=Colors.WARNING),
            kpi_card("Vehicles Loading", str(counts["loading"]), icon_letter="▣", accent=Colors.ACCENT_BLUE),
            kpi_card("Vehicles Exiting", str(counts["exiting"]), icon_letter="→", accent=Colors.TEXT_SECONDARY),
            kpi_card("Average Waiting", format_minutes(ENGINE.logistics.average_wait()), icon_letter="◔", accent=Colors.WARNING),
            kpi_card("Longest Waiting", format_minutes(ENGINE.logistics.max_wait()), icon_letter="◔", accent=Colors.CRITICAL),
            kpi_card("Congestion Index", f"{idx:.0f}/100", icon_letter="◎", accent=(Colors.CRITICAL if level in ("HIGH","CRITICAL") else Colors.WARNING if level=="MODERATE" else Colors.SUCCESS), sublabel=level),
            kpi_card("Throughput / hour", str(ENGINE.logistics.throughput_last_hour_estimate()), icon_letter="⇄", accent=Colors.SUCCESS),
        ]

    @app.callback(Output("logistics-map-container", "children"), Input("logistics-interval", "n_intervals"))
    def _map(_n):
        return _build_map("logistics-map")

    @app.callback(Output("logistics-congestion-tag", "children"), Input("logistics-interval", "n_intervals"))
    def _congestion_tag(_n):
        idx, level = ENGINE.logistics.congestion()
        color = Colors.CRITICAL if level in ("HIGH", "CRITICAL") else (Colors.WARNING if level == "MODERATE" else Colors.SUCCESS)
        return html.Span(f"{level} · {idx:.0f}/100", className="panel-tag", style={"color": color, "backgroundColor": color + "22"})

    @app.callback(Output("logistics-queue-list", "children"), Input("logistics-interval", "n_intervals"))
    def _queue_list(_n):
        queue = ENGINE.logistics.waiting_queue()
        if not queue:
            return html.Div("No vehicles currently waiting.", className="text-muted", style={"padding": "12px 4px"})
        return [queue_row(i + 1, v) for i, v in enumerate(queue[:8])]

    @app.callback(Output("logistics-queue-stats", "children"), Input("logistics-interval", "n_intervals"))
    def _queue_stats(_n):
        log = ENGINE.logistics
        queue = log.waiting_queue()
        clearance = round(len(queue) * 3.2, 1)
        stats = [
            ("Average wait", format_minutes(log.average_wait())),
            ("Max wait", format_minutes(log.max_wait())),
            ("Queue length", str(len(queue))),
            ("Est. clearance time", format_minutes(clearance)),
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
    )
    def _fleet_table(_n, fleet_filter):
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
            return html.Tr(html.Td("No vehicles match this filter.", colSpan=9, className="text-muted"))
        return [vehicle_table_row(v) for v in vehicles]