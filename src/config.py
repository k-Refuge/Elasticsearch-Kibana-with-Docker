from pathlib import Path

from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "movies"
REQUEST_TIMEOUT = 30
DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "movies_cleaned_v2.json"


def get_client() -> Elasticsearch:
    return Elasticsearch(ELASTICSEARCH_URL, request_timeout=REQUEST_TIMEOUT)
