# CinéSearch

Moteur de recherche de films avec Elasticsearch, Kibana et Python.

## Prérequis

- Docker et Docker Compose
- Python 3.10+
- uv

## Installation

```bash
uv sync
```

## Lancer Elasticsearch et Kibana

```bash
docker compose up -d
curl http://localhost:9200
```

- Elasticsearch: `http://localhost:9200`
- Kibana: `http://localhost:5601`

## Lancer l'application CLI

Depuis la racine du projet:

```bash
uv run python src/main.py
```

## Fonctionnalités actuelles

- Indexation bulk des films avec mapping explicite
- Recherche par titre
- Recherche avancée multi-critères
- Recherche dans le synopsis avec highlight
- Recherche floue (fuzziness)
- Suggestions de titres par préfixe
- Statistiques globales
- Tops genres/réalisateurs/acteurs
- Distribution des films par décennie

## Arrêter la stack

```bash
docker compose down
```
