# src/search.py
from elasticsearch import Elasticsearch
from config import ELASTICSEARCH_URL, INDEX_NAME

es = Elasticsearch(ELASTICSEARCH_URL)

def search_movie(q):
    res = es.search(
        index=INDEX_NAME,
        query={
            "multi_match": {
                "query": q,
                "fields": ["title", "overview"]
            }
        }
    )

    for hit in res["hits"]["hits"]:
        print(hit["_source"]["title"])