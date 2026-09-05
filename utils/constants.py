"""
SOCOCIM SmartFlow — Global constants.
Colors, thresholds, site geography and enums used across the whole app.
"""
from enum import Enum


# ---------------------------------------------------------------------------
# THEME / DESIGN TOKENS
# ---------------------------------------------------------------------------
class Colors:
    # Base surfaces — dark industrial control-room theme
    BG_MAIN = "#0B0F17"
    BG_PANEL = "#111826"
    BG_PANEL_ALT = "#161F30"
    BG_CARD = "#131B29"
    BORDER = "#212C3F"
    BORDER_LIGHT = "#2A3854"

    TEXT_PRIMARY = "#E9EEF7"
    TEXT_SECONDARY = "#8B98B0"
    TEXT_MUTED = "#5C6884"

    # Brand
    ACCENT = "#00D4B8"        # SmartFlow teal
    ACCENT_DIM = "#0A6E62"
    ACCENT_BLUE = "#3D8BFF"
    ACCENT_PURPLE = "#8B7CF6"

    # Status
    SUCCESS = "#2ED67A"
    WARNING = "#FFB020"
    CRITICAL = "#FF4757"
    INFO = "#3D8BFF"
    OFFLINE = "#5C6884"

    # Chart series
    SERIES_1 = "#00D4B8"
    SERIES_2 = "#3D8BFF"
    SERIES_3 = "#FFB020"
    SERIES_4 = "#FF4757"
    SERIES_5 = "#8B7CF6"


class EquipmentStatus(str, Enum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    OFFLINE = "OFFLINE"


class VehicleStatus(str, Enum):
    APPROACHING = "APPROACHING"
    AT_GATE = "AT_GATE"
    WAITING = "WAITING"
    WEIGHING = "WEIGHING"
    MOVING = "MOVING"
    LOADING = "LOADING"
    EXITING = "EXITING"
    COMPLETED = "COMPLETED"


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AlertStatus(str, Enum):
    NEW = "NEW"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"


class AlertSource(str, Enum):
    MAINTENANCE = "MAINTENANCE"
    LOGISTICS = "LOGISTICS"


STATUS_COLOR = {
    EquipmentStatus.NORMAL: Colors.SUCCESS,
    EquipmentStatus.WARNING: Colors.WARNING,
    EquipmentStatus.CRITICAL: Colors.CRITICAL,
    EquipmentStatus.OFFLINE: Colors.OFFLINE,
}

SEVERITY_COLOR = {
    Severity.INFO: Colors.INFO,
    Severity.WARNING: Colors.WARNING,
    Severity.CRITICAL: Colors.CRITICAL,
}

VEHICLE_STATUS_COLOR = {
    VehicleStatus.APPROACHING: Colors.INFO,
    VehicleStatus.AT_GATE: Colors.ACCENT_PURPLE,
    VehicleStatus.WAITING: Colors.WARNING,
    VehicleStatus.WEIGHING: Colors.ACCENT_BLUE,
    VehicleStatus.MOVING: Colors.SUCCESS,
    VehicleStatus.LOADING: Colors.ACCENT,
    VehicleStatus.EXITING: Colors.TEXT_SECONDARY,
    VehicleStatus.COMPLETED: Colors.OFFLINE,
}

# ---------------------------------------------------------------------------
# MAINTENANCE THRESHOLDS (business rules, mocked)
# ---------------------------------------------------------------------------
# Defaults; can be overridden per equipment type below.
DEFAULT_THRESHOLDS = {
    "temperature": {"normal": 70, "warning": 85},   # >warning => critical
    "vibration": {"normal": 4.0, "warning": 7.0},
    "humidity": {"normal": 60, "warning": 75},
}

TYPE_THRESHOLD_OVERRIDES = {
    "CRUSHER": {"temperature": {"normal": 75, "warning": 90}, "vibration": {"normal": 5.0, "warning": 8.5}},
    "MOTOR": {"temperature": {"normal": 70, "warning": 85}, "vibration": {"normal": 4.0, "warning": 7.0}},
    "MIXER": {"temperature": {"normal": 65, "warning": 80}, "vibration": {"normal": 3.5, "warning": 6.5}},
    "COMPRESSOR": {"temperature": {"normal": 68, "warning": 82}, "vibration": {"normal": 4.5, "warning": 7.5}},
    "CONVEYOR": {"temperature": {"normal": 60, "warning": 75}, "vibration": {"normal": 3.0, "warning": 6.0}},
    "PUMP": {"temperature": {"normal": 65, "warning": 80}, "vibration": {"normal": 3.5, "warning": 6.5}},
    "FAN": {"temperature": {"normal": 55, "warning": 70}, "vibration": {"normal": 3.0, "warning": 5.5}},
}

# ---------------------------------------------------------------------------
# LOGISTICS SITE GEOGRAPHY (fictional SOCOCIM-like cement plant, Rufisque area)
# ---------------------------------------------------------------------------
SITE_CENTER = (14.7167, -17.2733)  # Rufisque, Senegal area (fictional site)

SITE_POINTS = {
    "ENTRY":         {"name": "Site Entry",     "lat": 14.7215, "lon": -17.2810, "type": "entry"},
    "GATE_A":        {"name": "Gate A",         "lat": 14.7198, "lon": -17.2788, "type": "gate"},
    "GATE_B":        {"name": "Gate B",         "lat": 14.7182, "lon": -17.2795, "type": "gate"},
    "SECURITY":      {"name": "Security Check", "lat": 14.7178, "lon": -17.2760, "type": "checkpoint"},
    "WEIGHBRIDGE":   {"name": "Weighbridge",    "lat": 14.7160, "lon": -17.2745, "type": "checkpoint"},
    "WAITING_ZONE":  {"name": "Waiting Zone",   "lat": 14.7148, "lon": -17.2720, "type": "zone"},
    "BAY_1":         {"name": "Loading Bay 1",  "lat": 14.7132, "lon": -17.2700, "type": "bay"},
    "BAY_2":         {"name": "Loading Bay 2",  "lat": 14.7120, "lon": -17.2690, "type": "bay"},
    "BAY_3":         {"name": "Loading Bay 3",  "lat": 14.7108, "lon": -17.2682, "type": "bay"},
    "EXIT":          {"name": "Site Exit",      "lat": 14.7150, "lon": -17.2650, "type": "exit"},
}

# Routes: ordered waypoint keys describing the standard flow of a truck.
ROUTE_GATE_A = ["ENTRY", "GATE_A", "SECURITY", "WEIGHBRIDGE", "WAITING_ZONE", "BAY_1", "EXIT"]
ROUTE_GATE_B = ["ENTRY", "GATE_B", "SECURITY", "WEIGHBRIDGE", "WAITING_ZONE", "BAY_2", "EXIT"]

LOADING_BAYS = ["BAY_1", "BAY_2", "BAY_3"]

CARGO_TYPES = ["Clinker", "Ciment CPA 42.5", "Ciment CPJ 35", "Gypse", "Calcaire", "Pouzzolane", "Sacs ciment 50kg"]

CONGESTION_THRESHOLDS = {"MODERATE": 35, "HIGH": 60, "CRITICAL": 80}  # index 0-100

# ---------------------------------------------------------------------------
# GENERAL
# ---------------------------------------------------------------------------
HISTORY_LENGTH = 60          # rolling points kept per sensor metric
TICK_INTERVAL_MS = 2500      # base simulation heartbeat
APP_TITLE = "SOCOCIM SmartFlow"
APP_SUBTITLE = "Industrial Intelligence Platform"