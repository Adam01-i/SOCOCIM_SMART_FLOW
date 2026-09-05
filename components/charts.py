"""
SOCOCIM SmartFlow — Plotly chart factories.
All charts share a consistent dark, industrial theme with no default
Plotly chrome (toolbar hidden, minimal gridlines, custom fonts/colors).
"""
import plotly.graph_objects as go
from utils.constants import Colors

FONT = dict(family="Inter, -apple-system, sans-serif", color=Colors.TEXT_SECONDARY, size=11)

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=FONT,
    margin=dict(l=40, r=20, t=28, b=32),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                bgcolor="rgba(0,0,0,0)", font=dict(size=10, color=Colors.TEXT_SECONDARY)),
    hoverlabel=dict(bgcolor=Colors.BG_PANEL_ALT, font_size=11, font_family="Inter",
                     bordercolor=Colors.BORDER_LIGHT),
)

AXIS_STYLE = dict(
    showgrid=True, gridcolor=Colors.BORDER, zeroline=False,
    showline=False, tickfont=dict(size=10, color=Colors.TEXT_MUTED),
)

CONFIG_NO_CHROME = {"displayModeBar": False, "responsive": True}


def _apply_axes(fig, title=None):
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE, title=title)
    fig.update_layout(**BASE_LAYOUT)
    return fig


def sensor_trend_chart(x, y, name, color, unit, threshold_normal=None, threshold_warning=None, height=200):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(x), y=list(y), mode="lines", name=name,
        line=dict(color=color, width=2.4, shape="spline", smoothing=0.35),
        fill="tozeroy", fillcolor=color.replace(")", ", 0.10)").replace("rgb", "rgba") if "rgb" in color else color + "1A",
    ))
    if threshold_warning is not None:
        fig.add_hline(y=threshold_warning, line=dict(color=Colors.WARNING, width=1, dash="dot"))
    if threshold_normal is not None:
        fig.add_hline(y=threshold_normal, line=dict(color=Colors.TEXT_MUTED, width=1, dash="dot"))
    _apply_axes(fig, title=unit)
    fig.update_layout(height=height, showlegend=False)
    return fig


def multi_line_chart(series: list[dict], height=260, y_title=None):
    """series = [{x, y, name, color}]"""
    fig = go.Figure()
    for s in series:
        fig.add_trace(go.Scatter(
            x=s["x"], y=s["y"], mode="lines", name=s["name"],
            line=dict(color=s["color"], width=2.2, shape="spline", smoothing=0.3),
        ))
    _apply_axes(fig, title=y_title)
    fig.update_layout(height=height)
    return fig


def health_gauge(value: float, height=200):
    color = Colors.SUCCESS if value >= 75 else (Colors.WARNING if value >= 55 else Colors.CRITICAL)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": "%", "font": {"size": 30, "color": Colors.TEXT_PRIMARY}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": Colors.TEXT_MUTED, "tickfont": {"size": 9}},
            "bar": {"color": color, "thickness": 0.28},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 55], "color": Colors.CRITICAL + "22"},
                {"range": [55, 75], "color": Colors.WARNING + "22"},
                {"range": [75, 100], "color": Colors.SUCCESS + "22"},
            ],
        },
    ))
    fig.update_layout(**BASE_LAYOUT, height=height, margin=dict(l=20, r=20, t=10, b=10))
    return fig


def composite_radar(categories: list[str], values: list[float], height=340):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]], theta=categories + [categories[0]],
        fill="toself", fillcolor=Colors.ACCENT + "26",
        line=dict(color=Colors.ACCENT, width=2.5),
        marker=dict(size=5, color=Colors.ACCENT),
    ))
    fig.update_layout(
        **BASE_LAYOUT,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=True, tickfont=dict(size=8, color=Colors.TEXT_MUTED),
                             gridcolor=Colors.BORDER, linecolor=Colors.BORDER),
            angularaxis=dict(tickfont=dict(size=11, color=Colors.TEXT_SECONDARY), gridcolor=Colors.BORDER, linecolor=Colors.BORDER),
        ),
        height=height, showlegend=False, margin=dict(l=60, r=60, t=30, b=20),
    )
    return fig


def distribution_bar(labels, values, colors, height=240, orientation="v"):
    fig = go.Figure()
    if orientation == "v":
        fig.add_trace(go.Bar(x=labels, y=values, marker_color=colors, marker_line_width=0,
                              width=0.55))
    else:
        fig.add_trace(go.Bar(y=labels, x=values, marker_color=colors, marker_line_width=0,
                              orientation="h", width=0.55))
    _apply_axes(fig)
    fig.update_layout(height=height, showlegend=False, bargap=0.35)
    return fig


def stacked_area(x, series: list[dict], height=260):
    fig = go.Figure()
    for s in series:
        fig.add_trace(go.Scatter(
            x=x, y=s["y"], name=s["name"], mode="lines",
            stackgroup="one", line=dict(width=0.5, color=s["color"]),
            fillcolor=s["color"] + "55",
        ))
    _apply_axes(fig)
    fig.update_layout(height=height)
    return fig


def donut_chart(labels, values, colors, height=220, center_text=""):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.68,
        marker=dict(colors=colors, line=dict(color=Colors.BG_CARD, width=3)),
        textinfo="none",
        hoverinfo="label+percent",
    ))
    fig.update_layout(
        **BASE_LAYOUT, height=height, showlegend=True,
        margin=dict(l=10, r=10, t=10, b=10),
        annotations=[dict(text=center_text, x=0.5, y=0.5, font=dict(size=18, color=Colors.TEXT_PRIMARY), showarrow=False)],
    )
    return fig