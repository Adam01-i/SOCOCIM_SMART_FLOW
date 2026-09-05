"""
SOCOCIM SmartFlow — business calculations.
Health score, risk score, congestion index, anomaly confidence.
No ML dependency: transparent weighted formulas + rolling statistics,
explicitly presented as a *simulation* of predictive analytics.
"""
from __future__ import annotations
import math
from typing import List


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def metric_subscore(value: float, normal_max: float, warning_max: float) -> float:
    """
    Convert a raw sensor value into a 0-100 'goodness' subscore.
    <= normal_max -> close to 100
    between normal_max and warning_max -> declining through the 50s-70s
    > warning_max -> drops sharply toward 0
    """
    if value <= normal_max:
        # Slight penalty as it approaches the normal ceiling
        ratio = value / normal_max if normal_max else 0
        return clamp(100 - ratio * 10, 90, 100)
    if value <= warning_max:
        span = warning_max - normal_max or 1
        progress = (value - normal_max) / span
        return clamp(90 - progress * 35, 55, 90)  # 90 -> 55
    # Beyond warning: critical territory, decays toward 0 asymptotically
    overshoot = (value - warning_max) / (warning_max or 1)
    return clamp(54 - overshoot * 60, 0, 54)


def health_score(temperature_score: float, vibration_score: float, stability_score: float) -> float:
    """
    Weighted composite health score (0-100).
    """
    score = temperature_score * 0.35 + vibration_score * 0.45 + stability_score * 0.20
    return round(clamp(score, 0, 100), 1)


def health_classification(score: float) -> str:
    if score >= 90:
        return "EXCELLENT"
    if score >= 75:
        return "HEALTHY"
    if score >= 55:
        return "WARNING"
    return "CRITICAL"


def rolling_stability_score(history: List[float]) -> float:
    """
    Stability subscore derived from the volatility (std relative to mean)
    of recent readings. Low volatility -> high stability score.
    """
    if len(history) < 5:
        return 95.0
    n = len(history)
    mean = sum(history) / n
    if mean == 0:
        return 95.0
    variance = sum((x - mean) ** 2 for x in history) / n
    std = math.sqrt(variance)
    cv = std / abs(mean)  # coefficient of variation
    # cv ~0 -> 100 ; cv >= 0.25 -> ~30
    score = 100 - clamp(cv * 400, 0, 70)
    return clamp(score, 30, 100)


def trend_factor(history: List[float]) -> float:
    """
    Simple slope-based trend indicator over the recent window.
    Positive = rising, used to weight risk upward when values climb.
    Returns a normalized factor roughly in [-1, 1].
    """
    if len(history) < 6:
        return 0.0
    window = history[-10:]
    first_half = window[: len(window) // 2]
    second_half = window[len(window) // 2:]
    a = sum(first_half) / len(first_half)
    b = sum(second_half) / len(second_half)
    if a == 0:
        return 0.0
    delta = (b - a) / abs(a)
    return clamp(delta * 4, -1, 1)


def risk_score(temperature_score: float, vibration_score: float, trend: float) -> float:
    """
    Risk score (0-100): inverse-flavoured composite that also factors in
    short-term trend direction (rising values increase perceived risk).
    """
    base_risk = 100 - (temperature_score * 0.5 + vibration_score * 0.5)
    trend_bonus = clamp(trend, 0, 1) * 20  # only rising trend adds risk
    return round(clamp(base_risk + trend_bonus, 0, 100), 1)


def anomaly_confidence(risk: float, trend: float) -> float:
    """
    Presented to the user as 'Anomaly Confidence' — a simulated predictive
    analytics signal, not a certified AI system.
    """
    if risk < 45:
        return 0.0
    conf = clamp((risk - 45) / 55 * 100, 0, 100) * 0.7 + clamp(trend, 0, 1) * 30
    return round(clamp(conf, 0, 99), 1)


def congestion_index(vehicles_waiting: int, avg_wait_min: float, bay_occupancy_pct: float,
                      zone_capacity: int = 12) -> float:
    """
    Composite congestion score (0-100) combining:
    - queue length relative to zone capacity
    - average waiting time
    - loading bay utilization
    """
    queue_component = clamp((vehicles_waiting / zone_capacity) * 100, 0, 100) * 0.45
    wait_component = clamp((avg_wait_min / 30) * 100, 0, 100) * 0.35
    bay_component = clamp(bay_occupancy_pct, 0, 100) * 0.20
    return round(clamp(queue_component + wait_component + bay_component, 0, 100), 1)


def congestion_level(index: float) -> str:
    if index >= 80:
        return "CRITICAL"
    if index >= 60:
        return "HIGH"
    if index >= 35:
        return "MODERATE"
    return "LOW"


def interpolate(p1, p2, progress: float):
    """Linear interpolation between two (lat, lon) tuples."""
    progress = clamp(progress, 0, 1)
    lat = p1[0] + (p2[0] - p1[0]) * progress
    lon = p1[1] + (p2[1] - p1[1]) * progress
    return (lat, lon)


def format_minutes(minutes: float) -> str:
    minutes = max(0, minutes)
    if minutes < 60:
        return f"{minutes:.0f} min"
    h = int(minutes // 60)
    m = int(minutes % 60)
    return f"{h}h{m:02d}"