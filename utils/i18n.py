"""
SOCOCIM SmartFlow — i18n engine.

Three layers:
- STATIC_TRANSLATIONS: flat "English text" -> "translated text" map. Covers
  page titles, panel titles, buttons, table headers, enum values (NORMAL,
  WARNING, WAITING, ...), site point names, scenario names, recommendation
  titles, etc. t() looks a string up here and falls back to the original
  text unchanged if it isn't a translatable UI string (e.g. a proper noun
  like an equipment name or a vehicle id) — this makes it safe to call t()
  on almost anything.
- TEMPLATES: "translation key" -> template string with {placeholders},
  used for any text that embeds live data (equipment name, temperature,
  counts...). tt() looks up the template for the current language and
  formats it with the given kwargs.
- t_event(): renders an (event_key, params) pair produced by the engine.
  Events are stored key+params (not final text) so they can be translated
  correctly no matter which language is active *when the event is
  displayed*, not when it was generated.
"""
from __future__ import annotations

STATIC_TRANSLATIONS = {
    "en": {
        # --- Shell: sidebar / topbar (existing) ---
        "Overview": "Overview",
        "OPERATIONS": "OPERATIONS",
        "INTELLIGENCE": "INTELLIGENCE",
        "SYSTEM": "SYSTEM",
        "Smart Maintenance": "Smart Maintenance",
        "Smart Logistics": "Smart Logistics",
        "Control Center": "Control Center",
        "Alerts": "Alerts",
        "Analytics": "Analytics",
        "Simulation Lab": "Simulation Lab",
        "Industrial Intelligence": "Industrial Intelligence",
        "Platform v0.1 — Alpha": "Platform v0.1 — Alpha",
        "Language": "Language",
        "Theme": "Theme",
        "Light mode": "Light mode",
        "Dark mode": "Dark mode",
        "SmartFlow Operations Center": "SmartFlow Operations Center",
        "Industrial Intelligence Platform": "Industrial Intelligence Platform",
        "Equipment health & predictive monitoring": "Equipment health & predictive monitoring",
        "Fleet monitoring & flow optimization": "Fleet monitoring & flow optimization",
        "SmartFlow Control Center": "SmartFlow Control Center",
        "Unified operational supervision": "Unified operational supervision",
        "Alert Center": "Alert Center",
        "All system alerts, in one place": "All system alerts, in one place",
        "Historical intelligence across the site": "Historical intelligence across the site",
        "Trigger scenarios for demonstration and testing": "Trigger scenarios for demonstration and testing",
        "SYSTEM OPERATIONAL": "SYSTEM OPERATIONAL",
        "SYSTEM MONITORING": "SYSTEM MONITORING",
        "CRITICAL ATTENTION REQUIRED": "CRITICAL ATTENTION REQUIRED",
        "LIVE": "LIVE",
        "Priority: ": "Priority: ",
        "Anomaly Confidence: ": "Anomaly Confidence: ",
        "vehicles waiting": "vehicles waiting",
        "avg": "avg",
        "Raw Mill Area": "Raw Mill Area", "Crushing Station": "Crushing Station",
        "Clinker Transport": "Clinker Transport", "Cooling Circuit": "Cooling Circuit",
        "Kiln Ventilation": "Kiln Ventilation", "Cement Mixing": "Cement Mixing",
        "Pneumatic Systems": "Pneumatic Systems", "units": "units",
        "Queue Length (x5)": "Queue Length (x5)", "Index / scaled count": "Index / scaled count",

        # --- Enum values ---
        "NORMAL": "NORMAL", "WARNING": "WARNING", "CRITICAL": "CRITICAL", "OFFLINE": "OFFLINE",
        "APPROACHING": "Approaching", "AT_GATE": "At Gate", "WAITING": "Waiting", "WEIGHING": "Weighing",
        "MOVING": "Moving", "LOADING": "Loading", "EXITING": "Exiting", "COMPLETED": "Completed",
        "INFO": "Info", "NEW": "New", "ACKNOWLEDGED": "Acknowledged", "RESOLVED": "Resolved",
        "LOW": "Low", "MODERATE": "Moderate", "HIGH": "High", "MEDIUM": "Medium",
        "ALL": "ALL", "MAINTENANCE": "MAINTENANCE", "LOGISTICS": "LOGISTICS",
        "All": "All", "Waiting": "Waiting", "Loading": "Loading", "Moving": "Moving", "Critical": "Critical",
        "Last Hour": "Last Hour", "Today": "Today", "7 Days": "7 Days", "30 Days": "30 Days",

        # --- Site point names ---
        "Site Entry": "Site Entry", "Gate A": "Gate A", "Gate B": "Gate B",
        "Security Check": "Security Check", "Weighbridge": "Weighbridge",
        "Waiting Zone": "Waiting Zone", "Loading Bay 1": "Loading Bay 1",
        "Loading Bay 2": "Loading Bay 2", "Loading Bay 3": "Loading Bay 3",
        "Site Exit": "Site Exit", "Gate A / Waiting Zone": "Gate A / Waiting Zone",

        # --- Simulation scenarios ---
        "Normal Operation": "Normal Operation", "High Temperature": "High Temperature",
        "High Vibration": "High Vibration", "Critical Failure": "Critical Failure",
        "Sensor Offline": "Sensor Offline", "Restore System": "Restore System",
        "Normal Traffic": "Normal Traffic", "Arrival Rush": "Arrival Rush",
        "Gate Congestion": "Gate Congestion", "Loading Bay Failure": "Loading Bay Failure",
        "Emergency Queue": "Emergency Queue", "Restore Traffic": "Restore Traffic",
        "Demo Mode": "Demo Mode", "Auto-run the full storytelling script": "Auto-run the full storytelling script",
        "Start Demo Mode": "Start Demo Mode", "Stop Demo Mode": "Stop Demo Mode",
        "Simulation Speed": "Simulation Speed",
        "Smart Maintenance Scenarios": "Smart Maintenance Scenarios",
        "Smart Logistics Scenarios": "Smart Logistics Scenarios",
        "Simulation Log": "Simulation Log",
        "● DEMO MODE ACTIVE — scenario running automatically": "● DEMO MODE ACTIVE — scenario running automatically",

        # --- Recommendation titles ---
        "EQUIPMENT OFFLINE": "EQUIPMENT OFFLINE",
        "CRITICAL: COMBINED THERMAL & VIBRATION FAULT": "CRITICAL: COMBINED THERMAL & VIBRATION FAULT",
        "HIGH VIBRATION DETECTED": "HIGH VIBRATION DETECTED",
        "ABNORMAL TEMPERATURE RISE": "ABNORMAL TEMPERATURE RISE",
        "HEALTH SCORE DEGRADING": "HEALTH SCORE DEGRADING",
        "NOMINAL": "NOMINAL",
        "CONGESTION DETECTED — GATE A": "CONGESTION DETECTED — GATE A",
        "HIGH CONGESTION — ALL GATES": "HIGH CONGESTION — ALL GATES",
        "MODERATE CONGESTION": "MODERATE CONGESTION",
        "LOADING BAY AVAILABLE": "LOADING BAY AVAILABLE",

        # --- Overview page ---
        "SMARTFLOW OPERATIONAL PULSE": "SMARTFLOW OPERATIONAL PULSE",
        "Composite real-time site intelligence index": "Composite real-time site intelligence index",
        "AUTO": "AUTO",
        "Live Operations Feed": "Live Operations Feed",
        "Maintenance Snapshot": "Maintenance Snapshot",
        "Logistics Snapshot": "Logistics Snapshot",
        "Maintenance\nHealth": "Maintenance\nHealth", "Logistics\nFlow": "Logistics\nFlow",
        "Alert\nControl": "Alert\nControl", "Throughput": "Throughput",
        "Fleet\nStability": "Fleet\nStability",

        # --- KPI labels ---
        "Vehicles On Site": "Vehicles On Site", "Vehicles Waiting": "Vehicles Waiting",
        "Vehicles Loading": "Vehicles Loading", "Vehicles Exiting": "Vehicles Exiting",
        "Average Waiting": "Average Waiting", "Longest Waiting": "Longest Waiting",
        "Congestion Index": "Congestion Index", "Throughput / hour": "Throughput / hour",
        "Equipment Online": "Equipment Online", "Equipment Warning": "Equipment Warning",
        "Critical Equipment": "Critical Equipment", "Average Health Score": "Average Health Score",
        "Active Alerts": "Active Alerts", "Equipment Health": "Equipment Health",
        "Active Equipment": "Active Equipment", "Critical Alerts": "Critical Alerts",
        "Avg Waiting Time": "Avg Waiting Time", "Congestion Level": "Congestion Level",
        "Maintenance Risk": "Maintenance Risk", "Operational Efficiency": "Operational Efficiency",
        "Requires attention": "Requires attention", "All clear": "All clear",
        "Composite site efficiency": "Composite site efficiency",

        # --- Maintenance page ---
        "Equipment Fleet": "Equipment Fleet", "Recommendation": "Recommendation",
        "Temperature Trend (°C)": "Temperature Trend (°C)",
        "Vibration Trend (mm/s)": "Vibration Trend (mm/s)",
        "Health & Risk Evolution": "Health & Risk Evolution",
        "Equipment Digital View": "Equipment Digital View",
        "Equipment": "Equipment", "Status": "Status", "Health": "Health",
        "Temperature": "Temperature", "Vibration": "Vibration",
        "Operating Hours": "Operating Hours", "Last Inspection": "Last Inspection",
        "Estimated Maintenance": "Estimated Maintenance",
        "Health Score": "Health Score", "Risk Score": "Risk Score",
        "Temp": "Temp", "Vib mm/s": "Vib mm/s",
        "Recommended action: ": "Recommended action: ",

        # --- Logistics page ---
        "Site Map — Live Fleet Position": "Site Map — Live Fleet Position",
        "OpenStreetMap": "OpenStreetMap", "Queue Status": "Queue Status",
        "Fleet Table": "Fleet Table",
        "Vehicle": "Vehicle", "Plate": "Plate", "Location": "Location",
        "Cargo": "Cargo", "Wait": "Wait", "Speed": "Speed", "Queue": "Queue", "ETA": "ETA",
        "Average wait": "Average wait", "Max wait": "Max wait",
        "Queue length": "Queue length", "Est. clearance time": "Est. clearance time",

        # --- Control Center page ---
        "Site Map": "Site Map", "Congestion": "Congestion",
        "Active Recommendations": "Active Recommendations",

        # --- Analytics page ---
        "Maintenance Analytics": "Maintenance Analytics",
        "Equipment Health Distribution": "Equipment Health Distribution",
        "Anomalies by Equipment": "Anomalies by Equipment",
        "Logistics Analytics": "Logistics Analytics",
        "Queue Evolution & Congestion History": "Queue Evolution & Congestion History",
        "Loading Bay Utilization": "Loading Bay Utilization",
        "Excellent (90-100)": "Excellent (90-100)", "Healthy (75-89)": "Healthy (75-89)",
        "Warning (55-74)": "Warning (55-74)", "Critical (0-54)": "Critical (0-54)",

        # --- Empty states ---
        "No alerts match this filter.": "No alerts match this filter.",
        "No vehicles currently waiting.": "No vehicles currently waiting.",
        "No vehicles match this filter.": "No vehicles match this filter.",
        "No critical equipment at this time.": "No critical equipment at this time.",
        "No active recommendations — operations nominal.": "No active recommendations — operations nominal.",
        "No events yet.": "No events yet.",
        "No recent events.": "No recent events.",

        # --- Alert card ---
        "Acknowledge": "Acknowledge", "Resolve": "Resolve",
        "Recommendation: ": "Recommendation: ",
    },
    "fr": {
        "Overview": "Vue d’ensemble",
        "OPERATIONS": "OPÉRATIONS",
        "INTELLIGENCE": "INTELLIGENCE",
        "SYSTEM": "SYSTÈME",
        "Smart Maintenance": "Maintenance intelligente",
        "Smart Logistics": "Logistique intelligente",
        "Control Center": "Centre de contrôle",
        "Alerts": "Alertes",
        "Analytics": "Analytique",
        "Simulation Lab": "Laboratoire de simulation",
        "Industrial Intelligence": "Intelligence industrielle",
        "Platform v0.1 — Alpha": "Plateforme v0.1 — Alpha",
        "Language": "Langue",
        "Theme": "Thème",
        "Light mode": "Mode clair",
        "Dark mode": "Mode sombre",
        "SmartFlow Operations Center": "Centre des opérations SmartFlow",
        "Industrial Intelligence Platform": "Plateforme d’intelligence industrielle",
        "Equipment health & predictive monitoring": "État des équipements et maintenance prédictive",
        "Fleet monitoring & flow optimization": "Suivi de la flotte et optimisation des flux",
        "SmartFlow Control Center": "Centre de contrôle SmartFlow",
        "Unified operational supervision": "Supervision opérationnelle unifiée",
        "Alert Center": "Centre des alertes",
        "All system alerts, in one place": "Toutes les alertes système au même endroit",
        "Historical intelligence across the site": "Intelligence historique du site",
        "Trigger scenarios for demonstration and testing": "Déclencher des scénarios pour la démonstration et les tests",
        "SYSTEM OPERATIONAL": "SYSTÈME OPÉRATIONNEL",
        "SYSTEM MONITORING": "SYSTÈME SOUS SURVEILLANCE",
        "CRITICAL ATTENTION REQUIRED": "ATTENTION CRITIQUE REQUISE",
        "LIVE": "EN DIRECT",
        "Priority: ": "Priorité : ",
        "Anomaly Confidence: ": "Confiance d’anomalie : ",
        "vehicles waiting": "véhicules en attente",
        "avg": "moyenne",
        "Raw Mill Area": "Zone broyeur cru", "Crushing Station": "Station de concassage",
        "Clinker Transport": "Transport du clinker", "Cooling Circuit": "Circuit de refroidissement",
        "Kiln Ventilation": "Ventilation du four", "Cement Mixing": "Mélange du ciment",
        "Pneumatic Systems": "Systèmes pneumatiques", "units": "unités",
        "Queue Length (x5)": "Longueur de file (x5)", "Index / scaled count": "Indice / nombre mis à l’échelle",

        "NORMAL": "NORMAL", "WARNING": "AVERTISSEMENT", "CRITICAL": "CRITIQUE", "OFFLINE": "HORS LIGNE",
        "APPROACHING": "En approche", "AT_GATE": "Au portail", "WAITING": "En attente", "WEIGHING": "Pesée",
        "MOVING": "En mouvement", "LOADING": "Chargement", "EXITING": "Sortie", "COMPLETED": "Terminé",
        "INFO": "Info", "NEW": "Nouveau", "ACKNOWLEDGED": "Accusé de réception", "RESOLVED": "Résolu",
        "LOW": "Faible", "MODERATE": "Modérée", "HIGH": "Élevée", "MEDIUM": "Moyenne",
        "ALL": "TOUS", "MAINTENANCE": "Maintenance", "LOGISTICS": "Logistique",
        "All": "Tous", "Waiting": "En attente", "Loading": "Chargement", "Moving": "En mouvement", "Critical": "Critique",
        "Last Hour": "Dernière heure", "Today": "Aujourd’hui", "7 Days": "7 jours", "30 Days": "30 jours",

        "Site Entry": "Entrée du site", "Gate A": "Portail A", "Gate B": "Portail B",
        "Security Check": "Contrôle de sécurité", "Weighbridge": "Pont-bascule",
        "Waiting Zone": "Zone d’attente", "Loading Bay 1": "Baie de chargement 1",
        "Loading Bay 2": "Baie de chargement 2", "Loading Bay 3": "Baie de chargement 3",
        "Site Exit": "Sortie du site", "Gate A / Waiting Zone": "Portail A / Zone d’attente",

        "Normal Operation": "Fonctionnement normal", "High Temperature": "Température élevée",
        "High Vibration": "Vibration élevée", "Critical Failure": "Panne critique",
        "Sensor Offline": "Capteur hors ligne", "Restore System": "Restaurer le système",
        "Normal Traffic": "Trafic normal", "Arrival Rush": "Afflux d’arrivées",
        "Gate Congestion": "Congestion au portail", "Loading Bay Failure": "Panne de baie de chargement",
        "Emergency Queue": "File d’urgence", "Restore Traffic": "Restaurer le trafic",
        "Demo Mode": "Mode démo", "Auto-run the full storytelling script": "Exécuter automatiquement le scénario complet",
        "Start Demo Mode": "Démarrer le mode démo", "Stop Demo Mode": "Arrêter le mode démo",
        "Simulation Speed": "Vitesse de simulation",
        "Smart Maintenance Scenarios": "Scénarios de maintenance intelligente",
        "Smart Logistics Scenarios": "Scénarios de logistique intelligente",
        "Simulation Log": "Journal de simulation",
        "● DEMO MODE ACTIVE — scenario running automatically": "● MODE DÉMO ACTIF — scénario en cours d’exécution automatique",

        "EQUIPMENT OFFLINE": "ÉQUIPEMENT HORS LIGNE",
        "CRITICAL: COMBINED THERMAL & VIBRATION FAULT": "CRITIQUE : DÉFAUT THERMIQUE ET VIBRATOIRE COMBINÉ",
        "HIGH VIBRATION DETECTED": "VIBRATION ÉLEVÉE DÉTECTÉE",
        "ABNORMAL TEMPERATURE RISE": "HAUSSE DE TEMPÉRATURE ANORMALE",
        "HEALTH SCORE DEGRADING": "SCORE DE SANTÉ EN DÉGRADATION",
        "NOMINAL": "NOMINAL",
        "CONGESTION DETECTED — GATE A": "CONGESTION DÉTECTÉE — PORTAIL A",
        "HIGH CONGESTION — ALL GATES": "CONGESTION ÉLEVÉE — TOUS LES PORTAILS",
        "MODERATE CONGESTION": "CONGESTION MODÉRÉE",
        "LOADING BAY AVAILABLE": "BAIE DE CHARGEMENT DISPONIBLE",

        "SMARTFLOW OPERATIONAL PULSE": "POULS OPÉRATIONNEL SMARTFLOW",
        "Composite real-time site intelligence index": "Indice composite d’intelligence du site en temps réel",
        "AUTO": "AUTO",
        "Live Operations Feed": "Flux des opérations en direct",
        "Maintenance Snapshot": "Aperçu maintenance",
        "Logistics Snapshot": "Aperçu logistique",
        "Maintenance\nHealth": "Santé\nMaintenance", "Logistics\nFlow": "Flux\nLogistique",
        "Alert\nControl": "Contrôle\ndes alertes", "Throughput": "Débit",
        "Fleet\nStability": "Stabilité\nde la flotte",

        "Vehicles On Site": "Véhicules sur site", "Vehicles Waiting": "Véhicules en attente",
        "Vehicles Loading": "Véhicules en chargement", "Vehicles Exiting": "Véhicules en sortie",
        "Average Waiting": "Attente moyenne", "Longest Waiting": "Attente la plus longue",
        "Congestion Index": "Indice de congestion", "Throughput / hour": "Débit / heure",
        "Equipment Online": "Équipements en ligne", "Equipment Warning": "Équipements en alerte",
        "Critical Equipment": "Équipements critiques", "Average Health Score": "Score de santé moyen",
        "Active Alerts": "Alertes actives", "Equipment Health": "Santé des équipements",
        "Active Equipment": "Équipements actifs", "Critical Alerts": "Alertes critiques",
        "Avg Waiting Time": "Temps d’attente moyen", "Congestion Level": "Niveau de congestion",
        "Maintenance Risk": "Risque de maintenance", "Operational Efficiency": "Efficacité opérationnelle",
        "Requires attention": "Nécessite une attention", "All clear": "Tout est normal",
        "Composite site efficiency": "Efficacité composite du site",

        "Equipment Fleet": "Flotte d’équipements", "Recommendation": "Recommandation",
        "Temperature Trend (°C)": "Tendance de température (°C)",
        "Vibration Trend (mm/s)": "Tendance de vibration (mm/s)",
        "Health & Risk Evolution": "Évolution santé & risque",
        "Equipment Digital View": "Vue numérique de l’équipement",
        "Equipment": "Équipement", "Status": "Statut", "Health": "Santé",
        "Temperature": "Température", "Vibration": "Vibration",
        "Operating Hours": "Heures de fonctionnement", "Last Inspection": "Dernière inspection",
        "Estimated Maintenance": "Maintenance estimée",
        "Health Score": "Score de santé", "Risk Score": "Score de risque",
        "Temp": "Temp.", "Vib mm/s": "Vib. mm/s",
        "Recommended action: ": "Action recommandée : ",

        "Site Map — Live Fleet Position": "Carte du site — Position de la flotte en direct",
        "OpenStreetMap": "OpenStreetMap", "Queue Status": "État de la file",
        "Fleet Table": "Tableau de la flotte",
        "Vehicle": "Véhicule", "Plate": "Immatriculation", "Location": "Position",
        "Cargo": "Cargaison", "Wait": "Attente", "Speed": "Vitesse", "Queue": "File", "ETA": "ETA",
        "Average wait": "Attente moyenne", "Max wait": "Attente max",
        "Queue length": "Longueur de file", "Est. clearance time": "Temps d’écoulement estimé",

        "Site Map": "Carte du site", "Congestion": "Congestion",
        "Active Recommendations": "Recommandations actives",

        "Maintenance Analytics": "Analytique maintenance",
        "Equipment Health Distribution": "Répartition de la santé des équipements",
        "Anomalies by Equipment": "Anomalies par équipement",
        "Logistics Analytics": "Analytique logistique",
        "Queue Evolution & Congestion History": "Évolution de la file & historique de congestion",
        "Loading Bay Utilization": "Utilisation des baies de chargement",
        "Excellent (90-100)": "Excellent (90-100)", "Healthy (75-89)": "Bon (75-89)",
        "Warning (55-74)": "Alerte (55-74)", "Critical (0-54)": "Critique (0-54)",

        "No alerts match this filter.": "Aucune alerte ne correspond à ce filtre.",
        "No vehicles currently waiting.": "Aucun véhicule en attente actuellement.",
        "No vehicles match this filter.": "Aucun véhicule ne correspond à ce filtre.",
        "No critical equipment at this time.": "Aucun équipement critique pour le moment.",
        "No active recommendations — operations nominal.": "Aucune recommandation active — opérations nominales.",
        "No events yet.": "Aucun événement pour le moment.",
        "No recent events.": "Aucun événement récent.",

        "Acknowledge": "Acquitter", "Resolve": "Résoudre",
        "Recommendation: ": "Recommandation : ",
    },
}

# ---------------------------------------------------------------------------
# Templates: translation-key -> template with {placeholders}, formatted with
# already-resolved plain values (numbers/strings), never with raw enum
# members — callers pre-format numbers (e.g. f"{x:.1f}") before passing them.
# ---------------------------------------------------------------------------
TEMPLATES = {
    "en": {
        "msg_eq_offline": "{name} sensor feed is currently unavailable.",
        "msg_combined_fault": "{name} shows simultaneous high temperature ({temp}\u00b0C) and high vibration ({vib} mm/s) in {zone}.",
        "msg_high_vibration": "{name} vibration ({vib} mm/s) exceeded the recommended operating range in {zone}.",
        "msg_abnormal_temp": "{name} temperature ({temp}\u00b0C) is increasing abnormally in {zone}.",
        "msg_health_degrading": "{name} composite health score dropped to {score}%.",
        "msg_nominal": "{name} is operating within normal parameters.",
        "msg_congestion_queue": "Current queue: {queue_len} vehicles. Average wait: {avg_wait} min.",
        "msg_congestion_building": "Queue building up: {queue_len} vehicles waiting, average wait {avg_wait} min.",
        "msg_bay_available": "{bay} is available.",

        "rec_eq_offline": "Dispatch a technician to verify sensor connectivity and equipment status on site.",
        "rec_combined_fault": "Stop equipment for inspection within the next maintenance window. Check bearing assembly, lubrication and cooling circuit.",
        "rec_high_vibration": "Inspect bearing assembly and mounting within the next maintenance window.",
        "rec_abnormal_temp": "Check lubrication levels and cooling system airflow.",
        "rec_health_degrading": "Schedule a preventive inspection during the next planned downtime.",
        "rec_none": "No action required.",
        "rec_redirect_gate_b": "Temporarily redirect incoming trucks to Gate B to balance the flow.",
        "rec_open_bay_or_pause": "Open an additional loading bay or temporarily pause new arrivals.",
        "rec_monitor_prepare": "Monitor closely; prepare Gate B redirection if trend continues.",
        "rec_assign_bay": "Assign {vehicle_id} to {bay}.",

        "event_truck_entered_gate": "{vehicle} entered {gate}",
        "event_temp_stabilized": "{name} temperature stabilized",
        "event_assigned_bay": "{vehicle} assigned {bay}",
        "event_congestion_decreased": "Queue congestion decreased",
        "event_operating_normally": "{name} operating normally",
        "event_critical_alert": "CRITICAL alert: {name} — {title}",
        "event_warning_alert": "Warning: {name} — {title}",
        "event_congestion_detected": "{level} congestion detected near {subject}",
        "event_temp_anomaly_injected": "Temperature anomaly injected on {name}",
        "event_vib_anomaly_injected": "Vibration anomaly injected on {name}",
        "event_failure_simulated": "Equipment failure simulated on {name}",
        "event_marked_offline": "{name} marked OFFLINE",
        "event_marked_online": "{name} marked back ONLINE",
        "event_normal_restored_target": "Normal state restored for {name}",
        "event_normal_restored_all": "Normal state restored for all equipment",
        "event_arrival_rush": "Arrival rush triggered: +{count} trucks incoming",
        "event_gate_congestion_triggered": "Gate congestion scenario triggered",
        "event_bay_unavailable": "{bay} reported unavailable",
        "event_bay_restored": "{bay} restored to service",
        "event_congestion_resolved": "Congestion resolution actions applied",
        "event_redirect_gate_b_on": "Incoming trucks redirected to Gate B",
        "event_redirect_gate_b_off": "Gate B redirection lifted",
        "event_traffic_restored": "Traffic conditions restored to normal",
        "event_speed_set": "Simulation speed set to {speed}x",
        "event_demo_on": "DEMO MODE activated",
        "event_demo_off": "DEMO MODE stopped",

        "sub_equipment_online": "{online}/{total} equipment online",
        "sub_warning_critical": "{warning} warning · {critical} critical",
        "sub_waiting_loading": "{waiting} waiting · {loading} loading",
        "sub_max_wait": "Max: {max}",
        "sub_index": "Index: {idx}/100",
        "sub_critical_units": "{n} critical unit(s)",
        "sub_priority": "Priority: {p}",
        "sub_anomaly_confidence": "Anomaly Confidence: {c}%",
        "kpi_units_count": "{n}\nunits",
    },
    "fr": {
        "msg_eq_offline": "Le flux du capteur de {name} est actuellement indisponible.",
        "msg_combined_fault": "{name} présente simultanément une température élevée ({temp}\u00b0C) et une vibration élevée ({vib} mm/s) dans {zone}.",
        "msg_high_vibration": "La vibration de {name} ({vib} mm/s) a dépassé la plage de fonctionnement recommandée dans {zone}.",
        "msg_abnormal_temp": "La température de {name} ({temp}\u00b0C) augmente anormalement dans {zone}.",
        "msg_health_degrading": "Le score de santé composite de {name} est tombé à {score}%.",
        "msg_nominal": "{name} fonctionne dans les paramètres normaux.",
        "msg_congestion_queue": "File actuelle : {queue_len} véhicules. Attente moyenne : {avg_wait} min.",
        "msg_congestion_building": "La file s’allonge : {queue_len} véhicules en attente, attente moyenne de {avg_wait} min.",
        "msg_bay_available": "{bay} est disponible.",

        "rec_eq_offline": "Envoyer un technicien vérifier la connectivité du capteur et l’état de l’équipement sur site.",
        "rec_combined_fault": "Arrêter l’équipement pour inspection lors de la prochaine fenêtre de maintenance. Vérifier les roulements, la lubrification et le circuit de refroidissement.",
        "rec_high_vibration": "Inspecter les roulements et la fixation lors de la prochaine fenêtre de maintenance.",
        "rec_abnormal_temp": "Vérifier les niveaux de lubrification et la ventilation du système de refroidissement.",
        "rec_health_degrading": "Planifier une inspection préventive lors du prochain arrêt planifié.",
        "rec_none": "Aucune action requise.",
        "rec_redirect_gate_b": "Rediriger temporairement les camions entrants vers le Portail B pour équilibrer le flux.",
        "rec_open_bay_or_pause": "Ouvrir une baie de chargement supplémentaire ou suspendre temporairement les nouvelles arrivées.",
        "rec_monitor_prepare": "Surveiller de près ; préparer la redirection vers le Portail B si la tendance se poursuit.",
        "rec_assign_bay": "Assigner {vehicle_id} à {bay}.",

        "event_truck_entered_gate": "{vehicle} est entré à {gate}",
        "event_temp_stabilized": "Température de {name} stabilisée",
        "event_assigned_bay": "{vehicle} assigné à {bay}",
        "event_congestion_decreased": "La congestion de la file a diminué",
        "event_operating_normally": "{name} fonctionne normalement",
        "event_critical_alert": "Alerte CRITIQUE : {name} — {title}",
        "event_warning_alert": "Avertissement : {name} — {title}",
        "event_congestion_detected": "Congestion {level} détectée près de {subject}",
        "event_temp_anomaly_injected": "Anomalie de température injectée sur {name}",
        "event_vib_anomaly_injected": "Anomalie de vibration injectée sur {name}",
        "event_failure_simulated": "Panne d’équipement simulée sur {name}",
        "event_marked_offline": "{name} marqué HORS LIGNE",
        "event_marked_online": "{name} remis EN LIGNE",
        "event_normal_restored_target": "État normal restauré pour {name}",
        "event_normal_restored_all": "État normal restauré pour tous les équipements",
        "event_arrival_rush": "Afflux d’arrivées déclenché : +{count} camions entrants",
        "event_gate_congestion_triggered": "Scénario de congestion au portail déclenché",
        "event_bay_unavailable": "{bay} signalée indisponible",
        "event_bay_restored": "{bay} remise en service",
        "event_congestion_resolved": "Actions de résolution de congestion appliquées",
        "event_redirect_gate_b_on": "Camions entrants redirigés vers le Portail B",
        "event_redirect_gate_b_off": "Redirection vers le Portail B levée",
        "event_traffic_restored": "Conditions de trafic restaurées à la normale",
        "event_speed_set": "Vitesse de simulation réglée sur {speed}x",
        "event_demo_on": "MODE DÉMO activé",
        "event_demo_off": "MODE DÉMO arrêté",

        "sub_equipment_online": "{online}/{total} équipements en ligne",
        "sub_warning_critical": "{warning} en alerte · {critical} critiques",
        "sub_waiting_loading": "{waiting} en attente · {loading} en chargement",
        "sub_max_wait": "Max : {max}",
        "sub_index": "Indice : {idx}/100",
        "sub_critical_units": "{n} unité(s) critique(s)",
        "sub_priority": "Priorité : {p}",
        "sub_anomaly_confidence": "Confiance d’anomalie : {c}%",
        "kpi_units_count": "{n}\nunités",
    },
}


def t(text: str, language: str = "fr") -> str:
    """Static UI-string lookup. Falls back to the original text unchanged
    (safe to call on proper nouns like equipment/vehicle names)."""
    return STATIC_TRANSLATIONS.get(language, STATIC_TRANSLATIONS["en"]).get(text, text)


def tt(key: str, language: str = "fr", **params) -> str:
    """Templated lookup: formats the template for `key` with `params`."""
    table = TEMPLATES.get(language, TEMPLATES["en"])
    template = table.get(key) or TEMPLATES["en"].get(key, key)
    try:
        return template.format(**params)
    except (KeyError, IndexError):
        return template


def t_event(key: str, params: dict, language: str = "fr") -> str:
    """Render a stored (event_key, params) pair. Resolves nested translation
    keys (title_key, subject_key) before formatting the outer template."""
    resolved = {}
    for k, v in (params or {}).items():
        if k == "title_key":
            resolved["title"] = t(v, language).lower()
        elif k == "subject_key":
            resolved["subject"] = t(v, language)
        elif k == "level_key":
            resolved["level"] = t(v, language)
        else:
            resolved[k] = v
    return tt(key, language, **resolved)