# KAYAK - Recommandation de destination en France

## Objectif

Recommander les meilleures destinations de vacances en France selon deux critères principaux :
- **La météo** : température, précipitations et vent sur les 7 prochains jours.
- **Les hôtels** : offre hôtelière, notes des utilisateurs et description.

Le projet couvre la collecte de données (APIs & Scraping), le stockage dans un Data Lake (S3), le nettoyage et le chargement dans un Data Warehouse (RDS), et la visualisation des résultats.

## Architecture
Le flux de données suit l'architecture suivante :

1. **Extraction (Extract)** :
   - **Météo** : récupération des données via l'API *OpenWeatherMap* et coordonnées GPS via *Nominatim*.
   - **Hôtels** : scraping du site *Booking.com* à l'aide du framework **Scrapy**.
2. **Stockage (Data Lake)** :
   - Stockage des données brutes et nettoyées (`.csv`) sur **AWS S3**.
3. **Chargement (Load)** :
   - Ingestion des données consolidées dans une base de données SQL sur **AWS RDS** (PostgreSQL).
4. **Visualisation** :
   - Création de cartes interactives avec **Plotly** pour afficher le Top 5 des destinations et les 20 meilleurs hôtels.