## Historique des modifications

Ce document liste les changements effectués dans l'ordre chronologique.

### 1) Alignement de version Elasticsearch Python -> ES Docker
- Fichier modifié: `pyproject.toml`
- Changement: dépendance `elasticsearch>=9.3.0` remplacée par `elasticsearch>=8.12.0,<9.0.0`.
- Pourquoi: le cluster Docker est en ES 8.x, donc il faut un client Python 8.x pour éviter les erreurs de compatibilité des headers HTTP.

### 2) Correction du chemin du dataset JSON
- Fichier modifié: `src/main.py`
- Changement: remplacement du chemin relatif fragile par un chemin absolu construit avec `Path(__file__)`.
- Pourquoi: permettre l'exécution depuis la racine du projet (`uv run python src/main.py`) sans `FileNotFoundError`.

### 3) Centralisation de la configuration et du client ES
- Fichier modifié: `src/config.py`
- Changements:
  - ajout de `REQUEST_TIMEOUT`,
  - ajout de `DATA_FILE`,
  - ajout de `get_client()`.
- Pourquoi: éviter la duplication de code et faciliter la maintenance.

### 4) Refonte de l'indexation et création du mapping explicite
- Fichier modifié: `src/indexer.py`
- Changements:
  - ajout de l'attente de disponibilité Elasticsearch,
  - création programmatique du mapping complet de l'index `movies`,
  - parsing correct du dataset bulk (`fields` extrait comme source),
  - indexation par lots avec `helpers.streaming_bulk`,
  - progression pendant l'indexation,
  - résumé final succès/erreurs/temps,
  - vérifications post-indexation (`count`, échantillon, champs mapping).
- Pourquoi: répondre aux exigences du sujet et fiabiliser l'indexation.

### 5) Implémentation des fonctions de recherche demandées
- Fichier modifié: `src/search.py`
- Changements:
  - ajout de `search_by_title`,
  - ajout de `search_advanced`,
  - ajout de `search_plot` avec highlights,
  - ajout de `search_fuzzy`,
  - ajout de `suggest_titles`,
  - affichage formaté avec `tabulate`.
- Pourquoi: couvrir les différents cas de recherche du projet.

### 6) Implémentation des statistiques principales
- Fichier modifié: `src/analytics.py`
- Changements:
  - ajout de `global_stats`,
  - ajout de `top_genres`,
  - ajout de `top_directors`,
  - ajout de `top_actors`,
  - ajout de `movies_per_decade`,
  - affichage formaté avec `tabulate`.
- Pourquoi: fournir les analyses de base attendues.

### 7) Refonte de l'interface CLI
- Fichier modifié: `src/main.py`
- Changements:
  - menu complet et interactif,
  - saisie guidée pour les recherches simples et avancées,
  - accès à l'indexation, recherches et statistiques,
  - gestion des erreurs de saisie et des erreurs runtime.
- Pourquoi: rendre l'application utilisable de bout en bout depuis le terminal.

### 8) Mise à jour des dépendances "requirements"
- Fichier modifié: `requirements.txt`
- Changements: ajout de `elasticsearch>=8.12.0,<9.0.0` et `tabulate>=0.10.0`.
- Pourquoi: fournir un fichier de dépendances explicite pour le rendu.

### 9) Documentation de lancement et d'usage
- Fichier modifié: `README.md`
- Changements:
  - instructions d'installation,
  - commandes Docker,
  - commande de lancement CLI,
  - liste des fonctionnalités implémentées.
- Pourquoi: rendre le projet facilement exécutable et présentable.

### 10) Nettoyage Docker Compose (warning de version)
- Fichier modifié: `docker-compose.yml`
- Changement: suppression de la clé `version` obsolète.
- Pourquoi: éviter l'avertissement Docker Compose v2 et garder un fichier propre.
