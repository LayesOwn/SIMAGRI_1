# SIMAGRI V2 — Résumé Technique Précis

## 1. Vue d'ensemble

SIMAGRI est un **outil d'aide à la décision agro-climatique** (Decision Support System) combinant modélisation météorologique et simulation de cultures. Il permet aux utilisateurs de simuler les rendements agricoles pour le **Sénégal** (seul pays pleinement implémenté en V2) en utilisant soit des données historiques, soit des prévisions climatiques saisonnières.

**Stack technique :**
- Frontend : **Dash Plotly** + Bootstrap + Dash-Leaflet (cartes interactives)
- Backend : **Python 3.8**
- Moteur de simulation : **DSSAT-CSM** (Decision Support System for Agrotechnology Transfer) — binaire externe, intégration par fichiers I/O
- Déploiement : **Docker** + Gunicorn/Flask
- Port : 5000 (remappé via Docker sur 8080)

---

## 2. Structure du Projet

```
SIMAGRI_1/
├── app.py                          # Initialisation Dash
├── index.py                        # Point d'entrée (version Sénégal)
├── navbar.py                       # Barre de navigation
├── graph.py                        # Utilitaires graphiques Plotly
├── helpers.py                      # Fonctions helper (tableaux, plots)
├── debug.py                        # Utilitaires debug
├── requirements.txt                # Dépendances Python
├── apps/
│   └── senegal/
│       ├── __init__.py
│       ├── about.py               # Page "À propos" bilingue EN/FR
│       ├── historical.py          # Module simulation historique
│       ├── forecast_FResampler.py # Module prévisions saisonnières
│       ├── write_SNX.py           # Générateur fichiers scénario DSSAT (.snx)
│       ├── write_WTH.py           # Écrivain fichiers météo DSSAT (.wth)
│       ├── write_WTH_FR.py        # Écrivain météo pour FResampler
│       └── Dockerfile
├── shared/
│   ├── run_WGEN.py                # Orchestrateur WGEN
│   ├── run_FResampler.py          # Orchestrateur FResampler
│   ├── WGEN_generator.py          # Génération météo quotidienne
│   ├── WGEN_PAR_biweekly.py       # Estimation paramètres WGEN
│   ├── low_freq_correction.py     # Correction biais mensuelle
│   └── season_bias_corr.py        # Correction biais saisonnière
├── data/
│   ├── ET.SOL / SN.SOL            # Base de données sols
│   ├── MZCER*.CUL/ECO/SPE         # Paramètres cultivars DSSAT
│   └── WTH_files/                 # Données météo historiques (format DSSAT)
└── DSSAT/                         # Binaire DSSAT-CSM open-source
```

---

## 3. Modules Fonctionnels

### 3.1 Module Simulation Historique (`historical.py`)

**But :** Simuler les rendements agricoles sur la période **1983–2016** à partir de données météo historiques réelles.

**Paramètres d'entrée (16 paramètres) :**

| Catégorie | Paramètres |
|---|---|
| Scénario | Nom du scénario, Station (26 localisations Sénégal), Année cible |
| Culture | Crop (Arachide/PN, Mil/ML, Sorgho/SG, Riz/RI), Cultivar |
| Période | Plage d'années (1983–2016) |
| Sol | Type de sol (15 profils SN.SOL), Humidité initiale (10–100% AWC), NO3 initial (1–150 kg/ha) |
| Plantation | Date de semis, Densité (plants/m²) |
| Fertilisation | 3 applications possibles (date, quantités N/P/K, formule) |
| Phosphore | Simulation P (peanut seulement), niveau P extractable |
| Irrigation | Mode (Aucune / Dates reportées / Automatique), profondeur, seuil, efficacité |
| Économie | Prix culture, coût engrais, coût semences, coût irrigation, coûts variables/fixes |
| Saison critique | Sélection de la période de corrélation pluie (dropdown mensuel) |

**Sorties :**
- Box plots rendements
- Courbes CDF (Cumulative Distribution Function)
- Séries temporelles
- Box plots par classe d'années (AN/BN/NN selon azote et pluies)
- Téléchargements CSV (rendements simulés, probabilité de dépassement, pluies saisonnières)
- Tableau de gestion des scénarios (éditable, importable, téléchargeable)

---

### 3.2 Module Prévisions Saisonnières (`forecast_FResampler.py`)

**But :** Simuler les rendements en utilisant des **prévisions climatiques saisonnières** (SCF) avec downscaling météorologique via FResampler.

**Différences par rapport au module historique :**
- Ajout de 2 périodes de prévisions climatiques (trimestres) avec probabilités AN%, BN%, NN%
- Utilise FResampler au lieu des années historiques directes
- Génère **100 réalisations d'ensemble** à partir des prévisions
- Paramètres agricoles identiques au module historique

**Entrées supplémentaires spécifiques :**
- Trimestre 1 (12 options : JFM → DJF), Trimestre 2 (dérivé automatiquement)
- Probabilités : AN (Au-dessus Normal), BN (En-dessous Normal), NN = 100 - AN - BN

---

## 4. Système de Génération Météorologique

### 4.1 WGEN (Weather Generator)

**Rôle :** Génère 100 années synthétiques de météo quotidienne pour les prévisions.

**Algorithmes utilisés :**
- **Chaînes de Markov** : transitions jour sec/humide (P(wet|wet), P(wet|dry))
- **Modèle de mélange exponentiel (EMM)** : 2 composantes pour les quantités de pluie
- **Séries de Fourier** : ajustement température/rayonnement solaire (2 harmoniques)
- **Modèles AR(2)/AR(3)** : autocorrélation temporelle des résidus
- **Correction de biais** : quantile mapping mensuel + ajustement saisonnier

**Résolution paramètres :** Biennuelle (26 périodes/an de 14 jours chacune)

**Paramètres WGEN :**
- Pluie : `p000, p010, p100, p110` (probabilités transitions Markov)
- Quantités pluie : `alpha1, beta1, beta2` (poids mélange, moyennes exponentielles)
- Temp/Srad : coefficients Fourier (moyenne, amplitude, phase pour 2 harmoniques)
- Matrices d'autocorrélation des résidus

### 4.2 FResampler (Forecast Resampler)

**Rôle :** Approche plus simple — rééchantillonne les années historiques selon les probabilités de prévision.

**Algorithme :**
1. Classer les années par totaux de pluies saisonnières
2. Assigner aux terciles (BN=tiers inférieur, NN=milieu, AN=tiers supérieur)
3. Sélectionner proportionnellement : si BN%=30, sélectionner 30% du tercile inférieur
4. Fusionner climatologie + périodes dirigées par la prévision
5. Gère 6 cas selon le positionnement des trimestres (y compris les saisons à cheval sur 2 années)

---

## 5. Intégration DSSAT

### 5.1 Fichiers Scénario SNX (`write_SNX.py`)

Génère les fichiers `.snx` pour DSSAT-CSM :
- Configure : cultivars, champs, profils de sol, conditions initiales, plantation, irrigation, fertilisation
- Deux préfixes : `CL` (climatologie) et `FC` (prévision)
- Gère la simulation phosphore (section `SA` si activé)
- Calcule les dates de récolte (210 jours après semis + ajustements)

### 5.2 Fichiers Météo WTH (`write_WTH.py`, `write_WTH_FR.py`)

Convertit les DataFrames Python en format météo DSSAT :
```
*WEATHER DATA
@ INSI  LAT   LONG  ELEV  TAV  AMP  REFHT WNDHT
@DATE   SRAD  TMAX  TMIN  RAIN
YYDOY   SRAD  TMAX  TMIN  RAIN
```
- Gestion des années bissextiles
- Calculs jour-de-l'an
- Fichiers WTH individuels par membre d'ensemble
- Fichiers WTH multi-années consolidés

---

## 6. Cultures et Cultivars Supportés

| Code DSSAT | Culture | Cultivars (V2) |
|---|---|---|
| PN | Arachide (Peanut) | 6 cultivars |
| ML | Mil (Millet) | 4 cultivars |
| SG | Sorgho (Sorghum) | 4 cultivars : IB0066 Fadda-D, IB0069 IS15401-D, IB0070 Soumba-D, IB0071 Faourou-D |
| RI | Riz (Rice) | Définis dans DSSAT |

---

## 7. Base de Données Sol

**15 profils prédéfinis** (SN.SOL) avec :
- Profondeurs de couches, capacité de rétention d'eau (FC, WP)
- Classes texturales (S, LS, SL)
- Matière organique, salinité
- NO3 initial et phosphore extractable

---

## 8. Interface Utilisateur

**Framework :** Dash (Plotly) + Bootstrap
- Grille responsive (md=5 pour inputs, reste pour outputs)
- Conteneurs formulaires défilants
- Callbacks temps-réel pour visibilité dynamique (ex: table irrigation visible si irrigation sélectionnée)
- Upload/download de fichiers intégré
- Tableaux de données interactifs (lignes éditables, suppression)
- Cartes Leaflet avec marqueurs pour les 26 stations météo du Sénégal

**Navigation (bilingue FR/EN) :**
- "Analyse historique"
- "Analyse des prévisions"
- "Manuel"
- "Retour d'information"
- Page "À propos" bilingue

---

## 9. Calculs Économiques (Enterprise Budgeting)

| Calcul | Formule |
|---|---|
| Revenu total | Rendement simulé × Prix culture |
| Coût fertilisants | Σ(Quantité N × Coût unitaire N) par application |
| Coût variable total | Engrais + Semences + Irrigation + Autres |
| Marge brute | Revenu - Coût variable total - Coûts fixes |

---

## 10. Pipeline de Données (Data Flow)

```
Entrée Utilisateur
       ↓
Création Scénario (writeSNX_clim() ou writeSNX_frst())
       ↓
Sélection/Génération Météo
  ├── Historique: Chargement fichiers WTH existants
  └── Prévision: run_WGEN() ou run_FResampler()
       ↓
Écriture Fichiers WTH (write_WTH() ou write_WTH_FR())
       ↓
Exécution DSSAT (subprocess → binaire DSSAT-CSM)
       ↓
Parsing Sorties DSSAT (PlantGro, Summary, etc.)
       ↓
Visualisation (graphiques Plotly via callbacks Dash)
       ↓
Export CSV (téléchargement utilisateur)
```

---

## 11. Dépendances Python

| Package | Version | Rôle |
|---|---|---|
| dash | 1.20.0 | Framework UI |
| dash-bootstrap-components | — | Styling Bootstrap |
| dash-extensions | — | Extensions Dash |
| plotly | — | Graphiques |
| pandas | — | Manipulation données |
| numpy | — | Calculs numériques |
| folium + dash-leaflet | — | Cartes interactives |
| Flask + gunicorn | — | Serveur web WSGI |

**Exécutables externes :**
- **DSSAT-CSM** (modèle de culture) — binaire open-source
- **WGEN compilé** (Fortran) — non inclus dans le repo

---

## 12. Déploiement

```bash
docker build -f ./apps/senegal/Dockerfile -t simagri_senegal_img:latest .
docker run --name=simagri_senegal -e PYTHONUNBUFFERED=1 --rm -dp 8080:5000 simagri_senegal_img:latest
```

---

## 13. Limitations & Notes de Conception (V2)

| Limitation | Détail |
|---|---|
| **Pays unique** | Sénégal uniquement implémenté (placeholders Éthiopie, Colombie non fonctionnels) |
| **Dépendance WGEN Fortran** | Binaire WGEN précompilé requis (absent du repo) |
| **DSSAT file-based** | Intégration uniquement par lecture/écriture fichiers (pas d'API) |
| **Taille ensemble fixe** | 100 réalisations codées en dur |
| **Plage historique fixe** | 1983–2016 (contrainte fichiers WTD) |
| **UI French-first** | Chaînes françaises hardcodées dans le code |
| **Dash v1.20.0** | Version ancienne (2021) de Dash |
| **Architecture monolithique** | Tout dans un seul container Docker |
