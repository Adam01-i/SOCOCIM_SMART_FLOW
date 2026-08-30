# 🏭 SOCOCIM SmartFlow

### Plateforme intelligente d'optimisation des flux et de maintenance industrielle

> **Transformer les données industrielles en alertes, prédictions et décisions opérationnelles.**

---

## 📌 1. Présentation du projet

**SOCOCIM SmartFlow** est une plateforme intelligente destinée à améliorer la supervision des équipements industriels et l'optimisation des flux logistiques.

Le projet combine :

* 🌐 IoT
* 📡 ESP32
* 🌡️ Capteurs industriels
* 🚛 GPS / géolocalisation
* 🧠 Intelligence artificielle
* 📊 Analyse de données
* 🗄️ MySQL
* ⚙️ Backend Node.js
* 💻 Dashboard React

L'objectif n'est pas uniquement de collecter des données.

SmartFlow doit transformer :

```text
DONNÉES
   ↓
ANALYSE
   ↓
ALERTE
   ↓
PRÉDICTION
   ↓
RECOMMANDATION
   ↓
DÉCISION
```

La vision du projet repose sur quatre questions :

> **Que se passe-t-il ?**
> **Pourquoi ?**
> **Que risque-t-il de se passer ?**
> **Que devons-nous faire ?**

---

# 🎯 2. Problématique

Dans une industrie lourde, plusieurs éléments doivent être surveillés simultanément :

* équipements industriels ;
* véhicules ;
* opérations logistiques ;
* flux de matières ;
* temps d'attente ;
* risques de panne ;
* zones de congestion.

Une anomalie non détectée ou une panne imprévue peut entraîner :

* des arrêts de production ;
* des coûts supplémentaires ;
* des retards ;
* des temps d'attente importants ;
* une consommation inutile de ressources.

SmartFlow cherche donc à fournir une **vision centralisée et intelligente des opérations**.

---

# 🧩 3. Architecture fonctionnelle

SmartFlow est divisé en deux grands modules.

```text
                    SOCOCIM SMARTFLOW
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
    SMART MAINTENANCE            SMART LOGISTICS
             │                           │
             ▼                           ▼
       IoT / ESP32                 GPS / Véhicules
       Capteurs                    Géolocalisation
             │                           │
             └─────────────┬─────────────┘
                           ▼
                      BACKEND NODE.JS
                           │
                           ▼
                         MYSQL
                           │
                    ┌──────┴──────┐
                    ▼             ▼
                ANALYSE IA     DONNÉES
                    │
                    ▼
              RECOMMANDATIONS
                    │
                    ▼
              DASHBOARD REACT
```

---

# 🔧 4. Smart Maintenance

## Objectif

Surveiller l'état d'un équipement industriel grâce à des capteurs IoT.

Le MVP doit permettre de :

1. mesurer la température ;
2. mesurer les vibrations ;
3. transmettre les données ;
4. enregistrer les données ;
5. analyser les mesures ;
6. détecter une anomalie ;
7. générer une alerte ;
8. afficher l'état de l'équipement dans le dashboard.

Le cahier des charges prévoit notamment la surveillance d'un équipement avec un capteur de vibration/température et la détection d'une anomalie simulée.

---

# 🧪 5. Simulation IoT avec Wokwi

## Pourquoi Wokwi ?

Le projet ne disposant pas actuellement de matériel physique, **Wokwi constitue notre environnement de prototypage IoT**.

Wokwi permet de simuler des cartes ESP32 et de nombreux composants électroniques directement dans le navigateur.

L'ESP32 simulé peut également utiliser le réseau Wi-Fi virtuel de Wokwi et communiquer avec des services Internet via HTTP/HTTPS ou MQTT.

### Environnement simulé

```text
              WOKWI
                │
          ┌─────▼─────┐
          │   ESP32   │
          └─────┬─────┘
                │
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
 Température         Vibration
       │                 │
       └────────┬────────┘
                ▼
          Programme ESP32
                │
                ▼
             Wi-Fi
                │
                ▼
          Backend SmartFlow
```

---

# 🌡️ 6. Données IoT

Chaque mesure devra être associée à un équipement.

Exemple de données :

```json
{
  "deviceId": "ESP32-MAINT-001",
  "equipmentId": "EQ-001",
  "temperature": 72.5,
  "vibration": 4.8,
  "timestamp": "2026-08-30T10:30:00Z"
}
```

Le backend reçoit ces données et les enregistre dans MySQL.

---

# 🚨 7. Simulation d'une anomalie

La démonstration doit permettre de passer progressivement d'un fonctionnement normal à une situation anormale.

### Situation normale

```text
Température : 55°C
Vibration   : 2.1
État        : NORMAL
```

### Dégradation

```text
Température : 72°C
Vibration   : 4.8
État        : SURVEILLANCE
```

### Anomalie

```text
Température : 95°C
Vibration   : 9.5
État        : CRITIQUE
```

Le moteur d'analyse doit alors produire :

```text
🚨 ANOMALIE DÉTECTÉE

Équipement : EQ-001
Type       : Température + vibration
Niveau     : CRITIQUE

Recommandation :
"Effectuer une inspection de l'équipement."
```

---

# 🚛 8. Smart Logistics

## Objectif

Le module Smart Logistics permet de suivre les véhicules et d'analyser les flux logistiques.

Le système doit notamment permettre :

* de localiser les véhicules ;
* d'afficher leur position sur une carte ;
* de mesurer les temps d'attente ;
* d'identifier les zones de congestion ;
* d'analyser les flux ;
* de générer des recommandations.

## Ces fonctionnalités correspondent au démonstrateur prévu dans le projet.

# 🗺️ 9. Simulation des véhicules

Pour le MVP, les véhicules peuvent être simulés sans matériel GPS physique.

Exemple :

```json
{
  "vehicleId": "TRUCK-001",
  "latitude": 14.7167,
  "longitude": -17.4677,
  "speed": 32,
  "status": "EN_ROUTE",
  "timestamp": "2026-08-30T10:30:00Z"
}
```

Les positions peuvent être générées automatiquement afin de simuler :

```text
Véhicule
   ↓
Déplacement
   ↓
Arrivée dans une zone
   ↓
Ralentissement
   ↓
Arrêt
   ↓
Temps d'attente
   ↓
Congestion
```

---

# 🚦 10. Détection de congestion

Une congestion peut être détectée à partir de plusieurs indicateurs :

* nombre de véhicules dans une zone ;
* vitesse moyenne ;
* temps d'attente ;
* durée d'immobilisation ;
* évolution du trafic.

Exemple :

```text
Zone A

Véhicules : 8
Vitesse moyenne : 4 km/h
Temps d'attente moyen : 18 min

             ↓

       🚨 CONGESTION
```

---

# 🤖 11. Intelligence artificielle

L'IA sera développée progressivement.

## Niveau 1 — Détection

Détecter les situations anormales à partir de règles et seuils.

```text
SI température > seuil
OU vibration > seuil
→ anomalie
```

## Niveau 2 — Analyse

Analyser l'historique des mesures.

```text
Historique
    ↓
Analyse statistique
    ↓
Détection de comportement inhabituel
```

## Niveau 3 — Prédiction

À terme :

```text
Historique équipement
        ↓
Modèle prédictif
        ↓
Risque de panne
```

Pour la logistique :

```text
Historique trafic
       ↓
Modèle prédictif
       ↓
Risque de congestion
```

L'objectif à long terme est donc de passer de la simple détection à la prédiction.

---

# 💡 12. Moteur de recommandations

SmartFlow ne doit pas seulement afficher une alerte.

Il doit proposer une action.

Exemple maintenance :

```text
🚨 Température anormale

Analyse :
Hausse progressive depuis 20 minutes.

Recommandation :
→ Inspecter l'équipement EQ-001.
→ Vérifier le système de refroidissement.
```

Exemple logistique :

```text
🚨 Congestion détectée

Zone :
Entrée principale

Analyse :
12 véhicules / 15 minutes d'attente moyenne.

Recommandation :
→ Espacer les arrivées.
→ Réorienter certains véhicules.
```

---

# 📊 13. Dashboard React

Le dashboard constitue l'interface principale de SmartFlow.

## Dashboard principal

Il doit afficher :

```text
┌──────────────────────────────────────────────┐
│              SOCOCIM SMARTFLOW              │
├──────────────────────────────────────────────┤
│                                              │
│  Équipements    Véhicules     Alertes       │
│      24             18            3          │
│                                              │
├──────────────────────────────────────────────┤
│                                              │
│              ACTIVITÉ TEMPS RÉEL             │
│                                              │
├──────────────────────┬───────────────────────┤
│ Maintenance          │ Logistics             │
│                      │                       │
│ 🟢 12 Normal         │ 🚛 14 En circulation  │
│ 🟠 3 Surveillance    │ 🟠 2 En attente       │
│ 🔴 1 Critique        │ 🔴 2 Congestion       │
└──────────────────────┴───────────────────────┘
```

---

# 🏗️ 14. Stack technique

## IoT

* ESP32
* Wokwi
* Arduino C/C++
* Capteurs simulés
* Wi-Fi

## Backend

* Node.js
* Express.js
* API REST

## Base de données

* MySQL

## Frontend

* React
* TypeScript
* Tailwind CSS
* Bibliothèque de cartographie pour Smart Logistics

## IA / Data

* Python ou Node.js selon le modèle retenu
* Analyse statistique
* Machine Learning progressivement

## Développement

* Git
* GitHub
* VS Code
* Docker recommandé

---

# 👥 15. Organisation de l'équipe

L'équipe est divisée en deux pôles.

## 🔵 Pôle Smart Maintenance / IoT

### Khady

Responsable :

* architecture IoT ;
* ESP32 ;
* Wokwi ;
* capteurs ;
* communication ;
* simulation des anomalies ;
* transmission des données.

### Aïcha

Responsable :

* programmation ESP32 ;
* acquisition des données ;
* logique de détection ;
* tests IoT ;
* validation des scénarios ;
* documentation technique IoT.

Les deux travaillent ensemble sur le pipeline :

```text
Wokwi
 ↓
ESP32
 ↓
Capteurs
 ↓
Acquisition
 ↓
Communication
 ↓
Backend
```

---

# 🟢 Pôle Smart Logistics

### Assane

Responsable :

* backend Node.js ;
* API ;
* gestion des véhicules ;
* gestion des positions ;
* logique métier ;
* communication avec MySQL.

### Seydina Alioune

Responsable :

* frontend React ;
* dashboard ;
* carte ;
* visualisation des véhicules ;
* indicateurs logistiques ;
* interface utilisateur.

Pipeline :

```text
Simulation véhicule
        ↓
API Node.js
        ↓
MySQL
        ↓
Analyse
        ↓
Dashboard React
```

---

# 🧠 16. Responsabilité transversale

Même si les équipes sont séparées, Smart Maintenance et Smart Logistics doivent utiliser **la même plateforme**.

Architecture globale :

```text
              SMART MAINTENANCE
                     │
                     │
                     ▼
                ┌─────────┐
                │ Backend │
                └────┬────┘
                     │
              ┌──────▼──────┐
              │    MySQL    │
              └──────┬──────┘
                     │
                ┌────▼────┐
                │   IA    │
                └────┬────┘
                     │
                     ▼
              React Dashboard
                     ▲
                     │
                ┌────┴────┐
                │ Backend │
                └────▲────┘
                     │
                     │
              SMART LOGISTICS
```

---

# 🗄️ 17. Modèle de données

Les principales tables prévues sont :

```text
users
equipment
sensors
sensor_measurements
maintenance_alerts

vehicles
vehicle_positions
trips
waiting_events
congestion_events

recommendations
notifications
```

### Exemple

```text
equipment
---------
id
name
type
location
status
created_at
```

```text
sensor_measurements
-------------------
id
equipment_id
temperature
vibration
measured_at
```

```text
vehicles
--------
id
registration
name
status
created_at
```

```text
vehicle_positions
-----------------
id
vehicle_id
latitude
longitude
speed
recorded_at
```

---

# 🔌 18. API Backend

Quelques endpoints prévus :

## Maintenance

```http
POST /api/maintenance/measurements
GET  /api/maintenance/equipment
GET  /api/maintenance/equipment/:id
GET  /api/maintenance/alerts
```

## Logistics

```http
POST /api/logistics/vehicles/:id/position
GET  /api/logistics/vehicles
GET  /api/logistics/vehicles/:id
GET  /api/logistics/congestions
GET  /api/logistics/waiting-times
```

## Dashboard

```http
GET /api/dashboard/overview
GET /api/dashboard/alerts
GET /api/dashboard/kpis
```

---

# 🔄 19. Circuit complet des données

## Smart Maintenance

```text
CAPTEUR
   ↓
ESP32
   ↓
WOKWI
   ↓
Wi-Fi
   ↓
API NODE.JS
   ↓
VALIDATION
   ↓
MYSQL
   ↓
ANALYSE
   ↓
ANOMALIE ?
   │
   ├── NON → NORMAL
   │
   └── OUI
         ↓
       ALERTE
         ↓
   RECOMMANDATION
         ↓
     DASHBOARD
```

## Smart Logistics

```text
POSITION VÉHICULE
       ↓
API NODE.JS
       ↓
MYSQL
       ↓
ANALYSE DES FLUX
       ↓
TEMPS D'ATTENTE
       ↓
CONGESTION ?
       │
       ├── NON → NORMAL
       │
       └── OUI
             ↓
           ALERTE
             ↓
       RECOMMANDATION
             ↓
         DASHBOARD
```

---

# 📁 20. Structure du projet

```text
SOCOCIM_SMARTFLOW/
│
├── README.md
│
├── backend/
│   ├── src/
│   │   ├── maintenance/
│   │   ├── logistics/
│   │   ├── alerts/
│   │   ├── analytics/
│   │   └── dashboard/
│   │
│   ├── database/
│   ├── tests/
│   ├── package.json
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── modules/
│   │   │   ├── maintenance/
│   │   │   └── logistics/
│   │   ├── services/
│   │   └── types/
│   │
│   └── package.json
│
├── iot/
│   └── smart-maintenance/
│       ├── equipment-001/
│       │   ├── diagram.json
│       │   ├── sketch.ino
│       │   ├── libraries.txt
│       │   └── wokwi.toml
│       │
│       └── equipment-002/
│
├── ai/
│   ├── anomaly-detection/
│   ├── congestion-detection/
│   └── recommendations/
│
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   └── migrations/
│
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── iot/
│   └── diagrams/
│
└── docker-compose.yml
```

Wokwi permet notamment d'utiliser `diagram.json` pour définir le circuit et `wokwi.toml` pour la configuration du projet.

---

# 🌿 21. Organisation Git

La branche principale :

```text
main
```

Branches de développement :

```text
develop

feature/iot-maintenance
feature/backend-maintenance

feature/logistics-backend
feature/logistics-frontend

feature/ai
feature/dashboard
```

Chaque membre travaille sur sa branche.

Exemple :

```bash
git checkout -b feature/iot-maintenance
```

Puis :

```bash
git add .
git commit -m "feat(iot): add temperature sensor simulation"
git push origin feature/iot-maintenance
```

Les fonctionnalités sont ensuite fusionnées dans `develop`.

`main` représente la version stable destinée à la démonstration.

---

# 🚀 22. Circuit de développement

Le développement doit suivre cet ordre.

## Phase 1 — Architecture

Définir :

* architecture générale ;
* modèle de données ;
* API ;
* flux IoT ;
* flux logistique ;
* contrats JSON.

---

## Phase 2 — Base de données

Créer :

```text
MySQL
 ↓
Tables
 ↓
Relations
 ↓
Indexes
 ↓
Données de test
```

---

## Phase 3 — Backend

Développer d'abord les API.

```text
Node.js
 ↓
Express
 ↓
Routes
 ↓
Controllers
 ↓
Services
 ↓
MySQL
```

Tester chaque endpoint avant de connecter le frontend.

---

# 🔵 23. Développement Smart Maintenance

### Étape 1

Créer le projet ESP32 dans Wokwi.

### Étape 2

Ajouter les capteurs.

### Étape 3

Lire les valeurs.

### Étape 4

Afficher les valeurs dans le Serial Monitor.

### Étape 5

Créer les valeurs normales.

### Étape 6

Créer une anomalie simulée.

### Étape 7

Connecter l'ESP32 au Wi-Fi.

Wokwi fournit notamment le réseau virtuel `Wokwi-GUEST` pour les ESP32 simulés.

### Étape 8

Envoyer les données au backend.

### Étape 9

Vérifier leur présence dans MySQL.

### Étape 10

Développer la détection d'anomalies.

### Étape 11

Afficher l'alerte dans React.

---

# 🟢 24. Développement Smart Logistics

### Étape 1

Créer les véhicules fictifs.

### Étape 2

Créer leurs positions.

### Étape 3

Créer l'API GPS.

### Étape 4

Stocker les positions.

### Étape 5

Afficher les véhicules sur la carte.

### Étape 6

Simuler les déplacements.

### Étape 7

Calculer les temps d'attente.

### Étape 8

Détecter les congestions.

### Étape 9

Générer une recommandation.

### Étape 10

Afficher la recommandation dans le dashboard.

---

# 🤖 25. Développement IA

L'IA ne doit pas être développée en premier.

Ordre recommandé :

```text
DONNÉES
   ↓
STOCKAGE
   ↓
ANALYSE SIMPLE
   ↓
RÈGLES
   ↓
DÉTECTION
   ↓
HISTORIQUE
   ↓
MACHINE LEARNING
   ↓
PRÉDICTION
```

Cela permet d'avoir un MVP fonctionnel même si le modèle prédictif n'est pas encore suffisamment entraîné.

---

# 🧪 26. Tests

Chaque module doit être testé séparément.

### IoT

```text
[ ] ESP32 démarre
[ ] Capteur fonctionne
[ ] Valeurs reçues
[ ] Wi-Fi fonctionne
[ ] API reçoit les données
```

### Backend

```text
[ ] API accessible
[ ] Validation des données
[ ] MySQL fonctionne
[ ] CRUD fonctionne
[ ] Gestion des erreurs
```

### Logistics

```text
[ ] Véhicules visibles
[ ] Position correcte
[ ] Déplacement simulé
[ ] Temps d'attente calculé
[ ] Congestion détectée
```

### Dashboard

```text
[ ] KPI
[ ] Alertes
[ ] Carte
[ ] Équipements
[ ] Véhicules
[ ] Recommandations
```

---

# 🎬 27. Scénario de démonstration

La démonstration doit raconter une histoire.

### 1️⃣ Situation normale

Dashboard :

```text
🟢 Tous les systèmes fonctionnent normalement.
```

### 2️⃣ Anomalie industrielle

Dans Wokwi :

```text
Température ↑
Vibration ↑
```

SmartFlow détecte :

```text
🚨 ANOMALIE
```

### 3️⃣ Analyse

Le système identifie :

```text
Équipement EQ-001
Risque : élevé
```

### 4️⃣ Recommandation

```text
Effectuer une inspection préventive.
```

### 5️⃣ Situation logistique

Plusieurs véhicules arrivent dans une même zone.

```text
🚛 🚛 🚛 🚛 🚛
```

Le temps d'attente augmente.

### 6️⃣ Congestion

SmartFlow affiche :

```text
🚨 CONGESTION DÉTECTÉE
```

### 7️⃣ Décision

Le système recommande :

```text
→ Espacer les arrivées
→ Réorienter certains véhicules
```

Le jury voit ainsi toute la chaîne :

```text
CAPTEUR / GPS
      ↓
DONNÉE
      ↓
BACKEND
      ↓
BASE DE DONNÉES
      ↓
ANALYSE
      ↓
ALERTE
      ↓
RECOMMANDATION
      ↓
DÉCISION
```

---

# 📈 28. Évolution future

Le MVP constitue la première étape.

La stratégie d'évolution est :

```text
DIAGNOSTIC
    ↓
PROTOTYPE
    ↓
PILOTE
    ↓
DÉPLOIEMENT
```

Cette démarche correspond à la stratégie de déploiement proposée dans le projet.

À terme :

* vrais capteurs industriels ;
* vrais véhicules ;
* GPS réel ;
* données historiques importantes ;
* modèles prédictifs ;
* maintenance prédictive ;
* prédiction des congestions ;
* recommandations plus intelligentes ;
* notifications ;
* application mobile ;
* intégration aux systèmes industriels existants.

---

# 👨‍💻 29. Règles de développement de l'équipe

### Chaque fonctionnalité doit respecter :

```text
1. Créer une issue
2. Créer une branche
3. Développer
4. Tester
5. Commit
6. Push
7. Pull Request
8. Review
9. Merge
```

### Convention des commits

```text
feat: nouvelle fonctionnalité
fix: correction
docs: documentation
refactor: restructuration
test: ajout de tests
chore: maintenance
```

Exemples :

```bash
feat(iot): add vibration sensor simulation

feat(logistics): add vehicle tracking API

feat(frontend): add logistics dashboard

fix(backend): validate sensor payload

docs: update architecture
```

---

# 🏁 30. Objectif final

À la fin du développement, SOCOCIM SmartFlow devra être capable de démontrer :

```text
                    SMARTFLOW
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
   SMART MAINTENANCE          SMART LOGISTICS
          │                           │
      ESP32/Wokwi                Véhicules
          │                           │
     Température                 GPS/Position
     Vibration                       │
          │                           │
          └─────────────┬─────────────┘
                        ▼
                   NODE.JS API
                        │
                        ▼
                      MYSQL
                        │
                        ▼
                  ANALYSE / IA
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
          ALERTES            RECOMMANDATIONS
             │                     │
             └──────────┬──────────┘
                        ▼
                  REACT DASHBOARD
                        │
                        ▼
                     DÉCISION
```

## 🌟 Vision

**SOCOCIM SmartFlow ne se limite pas à surveiller l'industrie.**

Il transforme les données industrielles en informations exploitables, puis en recommandations permettant d'anticiper les problèmes et d'améliorer les décisions opérationnelles.

> **Observer → Comprendre → Prédire → Agir.**

---

## 👥 Équipe

### Smart Maintenance / IoT

* **Khady** — IoT / ESP32 / Wokwi
* **Aïcha** — IoT / Capteurs / Analyse

### Smart Logistics

* **Assane** — Backend / API / Logistique
* **Seydina Alioune** — Frontend / Dashboard / Cartographie

### Architecture & Système d'Information

* **Adama Seck** — Architecture SI / Données / Intégration / Coordination technique

---

## 📚 Documentation

* Projet : **SOCOCIM SmartFlow**
* Simulation IoT : **Wokwi**
* Backend : **Node.js**
* Base de données : **MySQL**
* Frontend : **React**
* Analyse : **IA / Data Analysis**

**Statut : 🚧 MVP en développement**


