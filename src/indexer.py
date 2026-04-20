# src/indexer.py
import json
import time
from typing import Any

from elasticsearch import helpers

from config import DATA_FILE, INDEX_NAME, get_client


def wait_for_elasticsearch(max_attempts: int = 30, delay: int = 2) -> bool:
    es = get_client()
    for attempt in range(1, max_attempts + 1):
        try:
            es.info()
            return True
        except Exception:
            print(f"En attente d'Elasticsearch... ({attempt}/{max_attempts})")
            time.sleep(delay)
    return False


def create_movies_index(recreate: bool = True) -> None:
    es = get_client()
    mappings: dict[str, Any] = {
        "properties": {
            "title": {"type": "text", "analyzer": "standard"},
            "directors": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}},
            },
            "actors": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}},
            },
            "genres": {"type": "keyword"},
            "year": {"type": "integer"},
            "rating": {"type": "float"},
            "rank": {"type": "integer"},
            "release_date": {"type": "date"},
            "plot": {"type": "text", "analyzer": "english"},
            "running_time_secs": {"type": "integer"},
            "image_url": {"type": "keyword"},
        }
    }

    if es.indices.exists(index=INDEX_NAME):
        if recreate:
            es.indices.delete(index=INDEX_NAME)
            print(f"Index '{INDEX_NAME}' supprimé pour réindexation.")
        else:
            return

    es.indices.create(index=INDEX_NAME, mappings=mappings)
    print(f"Index '{INDEX_NAME}' créé avec mapping explicite.")


def _build_actions(path: str):
    with open(path, "r", encoding="latin-1") as f:
        lines = f.readlines()

    for i in range(0, len(lines), 2):
        metadata = json.loads(lines[i].strip()).get("index", {})
        raw_doc = json.loads(lines[i + 1].strip())
        source = raw_doc.get("fields", raw_doc)
        doc_id = metadata.get("_id")
        action = {"_index": INDEX_NAME, "_source": source}
        if doc_id is not None:
            action["_id"] = doc_id
        yield action


def verify_index() -> None:
    es = get_client()
    count = es.count(index=INDEX_NAME)["count"]
    print(f"Nombre de documents indexés: {count}")

    sample = es.search(index=INDEX_NAME, size=3)
    print("\nExtrait de 3 films:")
    for hit in sample["hits"]["hits"]:
        src = hit["_source"]
        print(f"- {src.get('title', 'N/A')} ({src.get('year', 'N/A')}) note={src.get('rating', 'N/A')}")

    mapping = es.indices.get_mapping(index=INDEX_NAME)
    mapping_fields = mapping[INDEX_NAME]["mappings"]["properties"].keys()
    print(f"\nChamps du mapping: {', '.join(sorted(mapping_fields))}")


def index_data(path: str | None = None) -> None:
    dataset_path = path or str(DATA_FILE)

    if not wait_for_elasticsearch():
        print("Elasticsearch indisponible. Vérifie docker compose.")
        return

    create_movies_index(recreate=True)
    es = get_client()
    start = time.time()
    success = 0
    errors = 0

    try:
        for ok, _ in helpers.streaming_bulk(
            es,
            _build_actions(dataset_path),
            chunk_size=500,
            raise_on_error=False,
        ):
            if ok:
                success += 1
            else:
                errors += 1
            if (success + errors) % 500 == 0:
                print(f"Progression: {success + errors} documents traités...")
    except Exception as exc:
        print(f"Erreur lors de l'indexation: {exc}")
        return

    es.indices.refresh(index=INDEX_NAME)
    elapsed = time.time() - start
    print("\nIndexation terminée.")
    print(f"- Succès : {success}")
    print(f"- Erreurs: {errors}")
    print(f"- Durée  : {elapsed:.2f}s")
    verify_index()
