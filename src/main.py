# src/main.py
from indexer import index_data
from search import search_movie
from analytics import top_genres

while True:
    print("\n1. Index")
    print("2. Search")
    print("3. Stats")
    print("4. Exit")

    c = input("Choice: ")

    if c == "1":
        index_data("../data/movies_cleaned_v2.json")
    elif c == "2":
        q = input("Query: ")
        search_movie(q)
    elif c == "3":
        top_genres()
    elif c == "4":
        break