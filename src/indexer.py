# src/indexer.py
from elasticsearch import Elasticsearch, helpers
import json
from config import ELASTICSEARCH_URL, INDEX_NAME

es = Elasticsearch(ELASTICSEARCH_URL)

def index_data(path):
    with open(path, "r", encoding="latin-1") as f:
        lines = f.readlines()

    actions = []
    for i in range(0, len(lines), 2):
        doc = json.loads(lines[i+1])

        actions.append({
            "_index": INDEX_NAME,
            "_source": doc
        })

    helpers.bulk(es, actions)
    print("✅ Data indexed")
