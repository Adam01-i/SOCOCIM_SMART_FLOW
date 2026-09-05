"""Smart Maintenance page callbacks: KPI grid, equipment grid, digital view,
recommendations, and real-time trend charts for the selected equipment."""
from dash import Input, Output, State, html, ALL, ctx, no_update
import dash

from simulation.engine import ENGINE
from components.kpi_card import kpi_card
from components.equipment_card import equipment_card
from components.status_badge import status_badge, severity_badge
from components.charts import sensor_trend_chart, multi_line_chart
from services.recommendation_service import RecommendationEngine
from utils.constants import Colors, Severity
from utils.i18n import t, tt


def register(app):

    @app.callback(Output("maintenance-kpi-grid", "children"), Input("maintenance-interval", "n_intervals"), Input("language-store", "data"))
    def _kpis(_n, language):
        m = ENGINE.maintenance.counts()
        avg_health = ENGINE.maintenance.average_health()
        active_alerts = len([a for a in ENGINE.alert_service.active_alerts() if a.source.value == "MAINTENANCE"])
        return [
            kpi_card("Equipment Online", f"{m['online']}/{m['total']}", icon_letter="⚙", accent=Colors.ACCENT, language=language or "fr"),
            kpi_card("Equipment Warning", str(m["warning"]), icon_letter="▲", accent=Colors.WARNING, language=language or "fr"),
            kpi_card("Critical Equipment", str(m["critical"]), icon_letter="!", accent=Colors.CRITICAL, language=language or "fr"),
            kpi_card("Average Health Score", f"{avg_health:.1f}%", icon_letter="◈", accent=Colors.SUCCESS, language=language or "fr"),
            kpi_card("Active Alerts", str(active_alerts), icon_letter="◉", accent=Colors.ACCENT_PURPLE, language=language or "fr"),
        ]

    @app.callback(
        Output("maintenance-equipment-grid", "children"),
        Input("maintenance-interval", "n_intervals"),
        State("selected-equipment-store", "data"),
        Input("language-store", "data"),
    )
    def _equipment_grid(_n, language, selected_id):
        return [equipment_card(eq, selected=(eq.id == selected_id), language=language or "fr") for eq in ENGINE.equipment]

    @app.callback(
        Output("selected-equipment-store", "data"),
        Input({"type": "equipment-card", "index": ALL}, "n_clicks"),
        State("selected-equipment-store", "data"),
        prevent_initial_call=True,
    )
    def _select_equipment(n_clicks_list, current):
        triggered = ctx.triggered_id
        if not triggered or not any(n_clicks_list):
            return current
        return triggered["index"]

    @app.callback(
        Output("digital-view-panel", "children"),
        Input("maintenance-interval", "n_intervals"),
        State("selected-equipment-store", "data"),
        Input("language-store", "data"),
    )
    def _digital_view(_n, language, selected_id):
        language = language or "fr"
        eq = ENGINE.maintenance.equipment_by_id(selected_id) or ENGINE.equipment[0]
        rows = [
            ("Equipment", eq.name),
            ("Status", status_badge(eq.status, language=language)),
            ("Health", f"{eq.health_score:.1f}%"),
            ("Temperature", f"{eq.temperature:.1f} °C"),
            ("Vibration", f"{eq.vibration:.2f} mm/s"),
            ("Operating Hours", f"{eq.operating_hours:,.1f} h"),
            ("Last Inspection", eq.last_inspection),
            ("Estimated Maintenance", eq.estimated_maintenance),
        ]
        table_rows = []
        for label, value in rows:
            table_rows.append(
                html.Div(
                    [html.Div(t(label, language), className="text-muted", style={"fontSize": "12px", "flex": "1"}),
                     html.Div(value, style={"fontSize": "13px", "fontWeight": 600, "color": "var(--text-primary)", "flex": "1"})],
                    style={"display": "flex", "padding": "9px 2px", "borderBottom": "1px solid rgba(255,255,255,0.04)"},
                )
            )
        return [
            html.Div(
                [html.Div(t("Equipment Digital View", language), className="panel-title"),
                 html.Span(t(eq.zone, language), className="panel-tag")],
                className="panel-header",
            ),
            html.Div(table_rows),
        ]

    @app.callback(
        Output("maintenance-recommendation-panel", "children"),
        Input("maintenance-interval", "n_intervals"),
        State("selected-equipment-store", "data"),
        Input("language-store", "data"),
    )
    def _recommendation(_n, language, selected_id):
        language = language or "fr"
        eq = ENGINE.maintenance.equipment_by_id(selected_id) or ENGINE.equipment[0]
        recommendation = RecommendationEngine.for_equipment(eq)
        priority = RecommendationEngine.priority_for(eq)
        sev = Severity.CRITICAL if eq.status.value == "CRITICAL" else (Severity.WARNING if eq.status.value == "WARNING" else Severity.INFO)
        return html.Div(
            [
                html.Div([severity_badge(sev, label=recommendation.title(language), language=language)], style={"marginBottom": "10px"}),
                html.Div(recommendation.message(language), style={"fontSize": "13px", "color": "var(--text-secondary)", "marginBottom": "10px", "lineHeight": "1.6"}),
                html.Div(
                    [html.Span(t("Recommended action: ", language), style={"color": "var(--accent)", "fontWeight": 700}), recommendation.action(language)],
                    style={"fontSize": "12.5px", "color": "var(--text-secondary)", "background": "rgba(255,255,255,0.02)",
                           "padding": "10px 12px", "borderRadius": "8px", "marginBottom": "10px", "lineHeight": "1.6"},
                ),
                html.Div(
                    [
                        html.Span(f"{t('Priority: ', language)}{t(priority, language)}", className="mono", style={"marginRight": "16px"}),
                        html.Span(f"{t('Anomaly Confidence: ', language)}{eq.anomaly_confidence:.0f}%", className="mono"),
                    ],
                    style={"fontSize": "11.5px"},
                ),
            ]
        )

    @app.callback(
        Output("maintenance-temp-chart", "figure"),
        Input("maintenance-interval", "n_intervals"),
        State("selected-equipment-store", "data"),
        Input("language-store", "data"),
    )
    def _temp_chart(_n, language, selected_id):
        eq = ENGINE.maintenance.equipment_by_id(selected_id) or ENGINE.equipment[0]
        th = eq.thresholds()
        x = list(range(len(eq.temperature_history)))
        return sensor_trend_chart(x, list(eq.temperature_history), eq.name, Colors.SERIES_1, "°C",
                                   threshold_normal=th["temperature"]["normal"], threshold_warning=th["temperature"]["warning"])

    @app.callback(
        Output("maintenance-vib-chart", "figure"),
        Input("maintenance-interval", "n_intervals"),
        State("selected-equipment-store", "data"),
        Input("language-store", "data"),
    )
    def _vib_chart(_n, language, selected_id):
        eq = ENGINE.maintenance.equipment_by_id(selected_id) or ENGINE.equipment[0]
        th = eq.thresholds()
        x = list(range(len(eq.vibration_history)))
        return sensor_trend_chart(x, list(eq.vibration_history), eq.name, Colors.SERIES_3, "mm/s",
                                   threshold_normal=th["vibration"]["normal"], threshold_warning=th["vibration"]["warning"])

    @app.callback(
        Output("maintenance-health-risk-chart", "figure"),
        Input("maintenance-interval", "n_intervals"),
        State("selected-equipment-store", "data"),
        Input("language-store", "data"),
    )
    def _health_risk_chart(_n, language, selected_id):
        eq = ENGINE.maintenance.equipment_by_id(selected_id) or ENGINE.equipment[0]
        x = list(range(len(eq.health_history)))
        series = [
            {"x": x, "y": list(eq.health_history), "name": t("Health Score", language or "fr"), "color": Colors.SUCCESS},
            {"x": x, "y": list(eq.risk_history), "name": t("Risk Score", language or "fr"), "color": Colors.CRITICAL},
        ]
        return multi_line_chart(series, height=260, y_title="Score (0-100)")