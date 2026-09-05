"""Vehicle row component for the fleet table, and compact queue row."""
from dash import html
from data.vehicles import Vehicle
from components.status_badge import vehicle_status_badge
from utils.calculations import format_minutes


def vehicle_table_row(v: Vehicle):
    return html.Tr(
        [
            html.Td(html.Span(v.id, className="mono-strong")),
            html.Td(v.plate, className="mono"),
            html.Td(vehicle_status_badge(v.status)),
            html.Td(v.route[min(v.route_index, len(v.route)-1)].replace("_", " ").title()),
            html.Td(v.cargo),
            html.Td(format_minutes(v.waiting_time_min)),
            html.Td(f"{v.speed_kmh:.0f} km/h"),
            html.Td(str(v.queue_position) if v.queue_position else "—"),
            html.Td(f"{v.eta_min:.0f} min" if v.eta_min else "—"),
        ],
        id={"type": "vehicle-row", "index": v.id},
        className="fleet-table-row",
        n_clicks=0,
    )


def queue_row(rank: int, v: Vehicle):
    urgency = "queue-row-urgent" if v.waiting_time_min > 15 else ""
    return html.Div(
        [
            html.Div(f"#{rank}", className="queue-rank"),
            html.Div(
                [
                    html.Div(v.id, className="queue-vehicle-id"),
                    html.Div(v.cargo, className="queue-vehicle-cargo"),
                ],
                className="queue-vehicle-info",
            ),
            html.Div(format_minutes(v.waiting_time_min), className=f"queue-wait {urgency}"),
        ],
        className="queue-row",
    )