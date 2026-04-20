# src/analytics.py
from tabulate import tabulate

from config import INDEX_NAME, get_client


def global_stats() -> None:
    es = get_client()
    aggs = {
        "avg_rating": {"avg": {"field": "rating"}},
        "min_rating": {"min": {"field": "rating"}},
        "max_rating": {"max": {"field": "rating"}},
    }
    result = es.search(index=INDEX_NAME, size=0, aggs=aggs)
    total = result["hits"]["total"]["value"]
    avg_rating = result["aggregations"]["avg_rating"]["value"]
    min_rating = result["aggregations"]["min_rating"]["value"]
    max_rating = result["aggregations"]["max_rating"]["value"]

    top_movie = es.search(index=INDEX_NAME, size=1, query={"exists": {"field": "rating"}}, sort=[{"rating": "desc"}])["hits"]["hits"]
    low_movie = es.search(index=INDEX_NAME, size=1, query={"exists": {"field": "rating"}}, sort=[{"rating": "asc"}])["hits"]["hits"]

    print("\nStatistiques globales")
    print(f"- Nombre total de films: {total}")
    print(f"- Note moyenne        : {avg_rating:.2f}" if avg_rating is not None else "- Note moyenne        : N/A")
    print(f"- Note min / max      : {min_rating} / {max_rating}")
    if top_movie:
        src = top_movie[0]["_source"]
        print(f"- Film le mieux noté  : {src.get('title', 'N/A')} ({src.get('rating', 'N/A')})")
    if low_movie:
        src = low_movie[0]["_source"]
        print(f"- Film le moins noté  : {src.get('title', 'N/A')} ({src.get('rating', 'N/A')})")


def _print_terms_agg(agg_name: str, field_label: str, field: str, size: int = 10) -> None:
    es = get_client()
    result = es.search(index=INDEX_NAME, size=0, aggs={agg_name: {"terms": {"field": field, "size": size}}})
    buckets = result["aggregations"][agg_name]["buckets"]
    rows = [[i + 1, b["key"], b["doc_count"]] for i, b in enumerate(buckets)]
    if not rows:
        print(f"Aucune donnée pour {field_label}.")
        return
    print(f"\nTop {size} {field_label}")
    print(tabulate(rows, headers=["#", field_label, "Films"], tablefmt="grid"))


def top_genres(size: int = 10) -> None:
    _print_terms_agg("genres", "Genres", "genres", size=size)


def top_directors(size: int = 10) -> None:
    _print_terms_agg("directors", "Réalisateurs", "directors.keyword", size=size)


def top_actors(size: int = 10) -> None:
    _print_terms_agg("actors", "Acteurs", "actors.keyword", size=size)


def movies_per_decade() -> None:
    es = get_client()
    result = es.search(
        index=INDEX_NAME,
        size=0,
        aggs={"decades": {"histogram": {"field": "year", "interval": 10, "min_doc_count": 1}}},
    )
    buckets = result["aggregations"]["decades"]["buckets"]
    rows = [[int(b["key"]), b["doc_count"]] for b in buckets]
    if not rows:
        print("Aucune donnée par décennie.")
        return
    print("\nDistribution par décennie")
    print(tabulate(rows, headers=["Décennie", "Nombre de films"], tablefmt="grid"))