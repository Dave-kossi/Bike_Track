# 🚴 VeloTrack Mulhouse - Collecteur de Données en Temps Réel

> Application Streamlit de capture instantanée et d'archivage des données du réseau Vélostation Mulhouse pour l'analyse prédictive et le Machine Learning.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Description

Ce projet est un **collecteur automatique de données** pour le système de vélos en libre-service Vélostation de l'agglomération mulhousienne. Il capture l'état complet de toutes les stations en temps réel, calcule des métriques de tension (taux d'occupation) et archive les données dans un format CSV structuré pour analyse ultérieure.

### 🎯 Objectifs

- **Surveillance en temps réel** : Capture 100% des stations de l'agglomération
- **Analyse de tension** : Calcul automatique du taux de disponibilité par station
- **Archivage historique** : Sauvegarde horodatée pour constituer un jeu de données d'entraînement
- **Export ML** : Format CSV optimisé pour l'entraînement de modèles de prédiction

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| 📸 Capture instantanée | Récupère l'état de toutes les stations en une seule requête |
| 🔴 Indicateur d'urgence | Classification des stations selon leur niveau de tension |
| 💾 Archivage automatique | Sauvegarde locale avec horodatage précis (date, heure, timestamp) |
| 📊 Tableau de bord | Interface Streamlit pour visualisation et suivi |
| ⬇️ Export CSV | Téléchargement du dataset historique pour le Machine Learning |

---

## 🏗️ Architecture

```
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   API Nextbike      │────▶│  Application         │────▶│  Fichier CSV    │
│   (GBFS V2)         │     │  Streamlit           │     │  (Archivage)    │
└─────────────────────┘     └──────────────────────┘     └─────────────────┘
                                      │
                                      ▼
                              ┌──────────────────┐
                              │   Dashboard      │
                              │   Visualization   │
                              └──────────────────┘
```

### Flux de données

1. **Récupération** : Appel API synchrone vers le flux GBFS de Nextbike
2. **Fusion** : Jointure entre les données station_info et station_status
3. **Calcul** : Taux de disponibilité réel et score de tension
4. **Enrichissement** : Ajout des colonnes temporelles (timestamp, date, heure)
5. **Archivage** : Sauvegarde incrémentale en format TSV

---

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Clonez le dépôt** (ou copiez les fichiers)

```bash
git clone <url-du-depot>
cd Climate_project
```

2. **Créez un environnement virtuel** (recommandé)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Installez les dépendances**

```bash
pip install streamlit requests pandas numpy
```

---

## ▶️ Utilisation

### Lancement de l'application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

### Guide d'utilisation

1. **Page d'accueil** : Consultation du tableau de bord et des statistiques
2. **Capture de données** : Cliquez sur le bouton "📸 Lancer une capture de TOUTES les stations"
3. **Analyse** : Visualisez le tableau des stations avec leurs indicateurs de tension
4. **Export** : Téléchargez le fichier CSV complet pour vos analyses ML

---

## 📊 Colonnes du dataset

| Colonne | Type | Description |
|---------|------|-------------|
| `station_id` | Entier | Identifiant unique de la station |
| `name` | Texte | Nom officiel de la station |
| `capacity` | Entier | Nombre total de places disponibles |
| `num_bikes_available` | Entier | Nombre de vélos actuellement disponibles |
| `taux_reel` | Flottant | Taux de disponibilité (0 à 1) |
| `score_tension` | Flottant | Score de tension inversé (0 à 100) |
| `etat_label` | Texte | Indicateur visuel (🔴 URGENCE / 🟠 TENSION / 🟢 OK) |
| `timestamp` | DateTime | Horodatage complet ISO |
| `date` | Date | Date de la capture (YYYY-MM-DD) |
| `heure` | Heure | Heure de la capture (HH:MM:SS) |

---

## 🔧 Configuration

### Paramètres modifiables

Dans le fichier `app.py` :

```python
# Fichier de sortie
DATA_FILE = "dataset_complet_mulhouse.csv"

# Timeout des requêtes API (secondes)
timeout = 10
```

### Seuils de tension

Les seuils de classification peuvent être ajustés dans la fonction `get_status_label()` :

- **🔴 URGENCE** : Taux ≤ 15%
- **🟠 TENSION** : Taux ≤ 35%
- **🟢 OK** : Taux > 35%

---

## 🛠️ Dépendances

```
streamlit>=1.28.0
requests>=2.28.0
pandas>=1.5.0
numpy>=1.23.0
```

---

## 📈 Exemple de visualisation

L'interface Streamlit affiche :

- **Métriques globales** : Nombre total de lignes, nombre de captures, nom du fichier
- **Tableau des stations** : Toutes les stations triées par urgence
- **Bouton de téléchargement** : Export CSV avec date automatique

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez suivre ces étapes :

1. Fork le projet
2. Créez une branche (`git checkout -b feature/Amelioration`)
3. Committez vos changements (`git commit -m 'Ajout d'une fonctionnalité'`)
4. Push vers la branche (`git push origin feature/Amelioration`)
5. Ouvrez une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 🙏 Remerciements

- [Nextbike](https://www.nextbike.fr/) pour l'API GBFS
- [Streamlit](https://streamlit.io/) pour le framework d'interface
- Communauté open source

---

## 📞 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

*Généré automatiquement pour le projet Vélostation Mulhouse - Collecteur de Données*
