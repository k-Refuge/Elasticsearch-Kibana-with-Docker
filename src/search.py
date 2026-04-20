# src/search.py
from tabulate import tabulate

from config import INDEX_NAME, get_client


def _print_hits(hits, title: str = "Résultats") -> None:
    if not hits:
        print(f"{title}: aucun résultat.")
        return

    rows = []
    for i, hit in enumerate(hits, start=1):
        src = hit.get("_source", {})
        directors = ", ".join(src.get("directors", [])) if isinstance(src.get("directors"), list) else src.get("directors", "N/A")
        rows.append(
            [
                i,
                src.get("title", "N/A"),
                src.get("year", "N/A"),
                src.get("rating", "N/A"),
                directors,
                round(hit.get("_score", 0), 3),
            ]
        )

    print(f"\n{title}")
    print(tabulate(rows, headers=["#", "Titre", "Année", "Note", "Réalisateur(s)", "Score"], tablefmt="grid"))
    print(f"{len(rows)} résultat(s) trouvé(s).")


def search_by_title(query: str, size: int = 10) -> None:
    es = get_client()
    result = es.search(index=INDEX_NAME, query={"match": {"title": query}}, size=size)
    _print_hits(result["hits"]["hits"], title=f"Recherche par titre: {query}")


def search_advanced(
    title: str | None = None,
    actor: str | None = None,
    director: str | None = None,
    genre: str | None = None,
    min_rating: float | None = None,
    max_rating: float | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    size: int = 10,
) -> None:
    es = get_client()
    must = []
    filters = []

    if title:
        must.append({"match": {"title": title}})
    if actor:
        must.append({"match": {"actors": actor}})
    if director:
        must.append({"match": {"directors": director}})
    if genre:
        filters.append({"term": {"genres": genre}})

    rating_range = {}
    if min_rating is not None:
        rating_range["gte"] = min_rating
    if max_rating is not None:
        rating_range["lte"] = max_rating
    if rating_range:
        filters.append({"range": {"rating": rating_range}})

    year_range = {}
    if year_from is not None:
        year_range["gte"] = year_from
    if year_to is not None:
        year_range["lte"] = year_to
    if year_range:
        filters.append({"range": {"year": year_range}})

    query = {"bool": {"must": must if must else [{"match_all": {}}], "filter": filters}}
    result = es.search(index=INDEX_NAME, query=query, size=size)
    _print_hits(result["hits"]["hits"], title="Recherche avancée")


def search_plot(keywords: str, size: int = 5) -> None:
    es = get_client()
    result = es.search(
        index=INDEX_NAME,
        query={"match": {"plot": keywords}},
        highlight={"fields": {"plot": {"fragment_size": 150, "number_of_fragments": 1}}},
        size=size,
    )
    hits = result["hits"]["hits"]
    if not hits:
        print("Recherche synopsis: aucun résultat.")
        return

    for hit in hits:
        src = hit["_source"]
        print(f"\n- {src.get('title', 'N/A')} ({src.get('year', 'N/A')})")
        fragments = hit.get("highlight", {}).get("plot", [])
        if fragments:
            print(f"  Extrait: {fragments[0]}")
    print(f"\n{len(hits)} résultat(s) trouvé(s).")


def search_fuzzy(query: str, fuzziness: int = 2, size: int = 10) -> None:
    es = get_client()
    result = es.search(
        index=INDEX_NAME,
        query={"match": {"title": {"query": query, "fuzziness": fuzziness}}},
        size=size,
    )
    _print_hits(result["hits"]["hits"], title=f"Recherche floue: {query}")


def suggest_titles(prefix: str, size: int = 10) -> None:
    es = get_client()
    result = es.search(
        index=INDEX_NAME,
        query={"prefix": {"title": {"value": prefix.lower()}}},
        size=size,
    )
    titles = [hit.get("_source", {}).get("title", "N/A") for hit in result["hits"]["hits"]]
    if not titles:
        print("Aucune suggestion.")
        return
    print("\nSuggestions:")
    for i, title in enumerate(titles, start=1):
        print(f"{i}. {title}")