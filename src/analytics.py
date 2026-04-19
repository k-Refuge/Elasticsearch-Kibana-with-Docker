# src/analytics.py
from elasticsearch import Elasticsearch
from config import ELASTICSEARCH_URL, INDEX_NAME

es = Elasticsearch(ELASTICSEARCH_URL)

def top_genres():
    res = es.search(
        index=INDEX_NAME,
        size=0,
        aggs={
            "genres": {
                "terms": {"field": "genres.keyword"}
            }
        }
    )

    for g in res["aggregations"]["genres"]["buckets"]:
        print(g["key"], g["doc_count"])