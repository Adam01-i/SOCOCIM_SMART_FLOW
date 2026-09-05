"""Analytics page callbacks — maintenance & logistics historical intelligence.
Underlying data is mocked/simulated, but internally consistent with the
live simulation state (same engine, same fleet)."""
from dash import Input, Output

from simulation.engine import ENGINE
from components.charts import donut_chart, distribution_bar, stacked_area, multi_line_chart
from utils.constants import Colors, EquipmentStatus, LOADING_BAYS


def register(app):

    @app.callback(Output("an-health-distribution", "figure"), Input("analytics-interval", "n_intervals"),
                  Input("analytics-period", "value"))
    def _health_distribution(_n, _period):
        buckets = {"Excellent (90-100)": 0, "Healthy (75-89)": 0, "Warning (55-74)": 0, "Critical (0-54)": 0}
        for eq in ENGINE.equipment:
            h = eq.health_score
            if h >= 90:
                buckets["Excellent (90-100)"] += 1
            elif h >= 75:
                buckets["Healthy (75-89)"] += 1
            elif h >= 55:
                buckets["Warning (55-74)"] += 1
            else:
                buckets["Critical (0-54)"] += 1
        colors = [Colors.SUCCESS, Colors.ACCENT, Colors.WARNING, Colors.CRITICAL]
        return donut_chart(list(buckets.keys()), list(buckets.values()), colors,
                            center_text=f"{len(ENGINE.equipment)}\nunits")

    @app.callback(Output("an-anomalies-by-equipment", "figure"), Input("analytics-interval", "n_intervals"),
                  Input("analytics-period", "value"))
    def _anomalies_by_equipment(_n, _period):
        names, counts, colors = [], [], []
        for eq in ENGINE.equipment:
            anomaly_ticks = len([r for r in eq.risk_history if r >= 50])
            names.append(eq.name)
            counts.append(anomaly_ticks)
            colors.append(Colors.CRITICAL if anomaly_ticks > 10 else (Colors.WARNING if anomaly_ticks > 3 else Colors.ACCENT))
        # sort descending for readability
        pairs = sorted(zip(names, counts, colors), key=lambda p: p[1], reverse=True)
        names, counts, colors = zip(*pairs) if pairs else ([], [], [])
        return distribution_bar(list(names), list(counts), list(colors), orientation="h", height=280)

    @app.callback(Output("an-maintenance-risk", "figure"), Input("analytics-interval", "n_intervals"),
                  Input("analytics-period", "value"))
    def _maintenance_risk(_n, _period):
        ranked = ENGINE.maintenance.sorted_by_risk()
        names = [e.name for e in ranked]
        values = [e.risk_score for e in ranked]
        colors = [Colors.CRITICAL if v >= 55 else (Colors.WARNING if v >= 30 else Colors.SUCCESS) for v in values]
        return distribution_bar(names, values, colors, orientation="h", height=280)

    @app.callback(Output("an-congestion-history", "figure"), Input("analytics-interval", "n_intervals"),
                  Input("analytics-period", "value"))
    def _congestion_history(_n, _period):
        x = list(range(len(ENGINE.congestion_history)))
        series = [
            {"x": x, "y": list(ENGINE.congestion_history), "name": "Congestion Index", "color": Colors.WARNING},
        ]
        x2 = list(range(len(ENGINE.queue_length_history)))
        series.append({"x": x2, "y": [q * 5 for q in ENGINE.queue_length_history], "name": "Queue Length (x5)", "color": Colors.ACCENT_BLUE})
        return multi_line_chart(series, height=280, y_title="Index / scaled count")

    @app.callback(Output("an-bay-utilization", "figure"), Input("analytics-interval", "n_intervals"),
                  Input("analytics-period", "value"))
    def _bay_utilization(_n, _period):
        occ = ENGINE.fleet_service.bay_occupancy
        labels = [b.replace("_", " ").title() for b in LOADING_BAYS]
        values = [1 if occ.get(b) not in (None,) else 0 for b in LOADING_BAYS]
        colors = [Colors.CRITICAL if v == 1 and occ.get(b) == "BLOCKED" else (Colors.ACCENT if v == 1 else Colors.OFFLINE)
                  for v, b in zip(values, LOADING_BAYS)]
        display_values = [100 if occ.get(b) == "BLOCKED" else (85 if occ.get(b) else 15) for b in LOADING_BAYS]
        return distribution_bar(labels, display_values, colors, orientation="v", height=280)