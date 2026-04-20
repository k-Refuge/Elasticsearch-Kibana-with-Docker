# src/main.py
from analytics import global_stats, movies_per_decade, top_actors, top_directors, top_genres
from config import DATA_FILE
from indexer import index_data
from search import search_advanced, search_by_title, search_fuzzy, search_plot, suggest_titles


def _to_float(value: str):
    return float(value) if value.strip() else None


def _to_int(value: str):
    return int(value) if value.strip() else None


def run_cli() -> None:
    print("Bienvenue dans CinéSearch.")
    while True:
        print("\n╔══════════════════════════════════════════╗")
        print("║         CinéSearch — Menu Principal      ║")
        print("╠══════════════════════════════════════════╣")
        print("║  1. Indexer les films                    ║")
        print("║  2. Recherche par titre                  ║")
        print("║  3. Recherche avancée (multi-critères)   ║")
        print("║  4. Recherche dans le synopsis           ║")
        print("║  5. Recherche floue                      ║")
        print("║  6. Suggestions de titres                ║")
        print("║  7. Statistiques globales                ║")
        print("║  8. Top genres/réalisateurs/acteurs      ║")
        print("║  9. Répartition par décennie             ║")
        print("║  0. Quitter                              ║")
        print("╚══════════════════════════════════════════╝")

        choice = input("Choix: ").strip()

        try:
            if choice == "1":
                index_data(str(DATA_FILE))
            elif choice == "2":
                q = input("Titre recherché: ").strip()
                search_by_title(q)
            elif choice == "3":
                title = input("Titre (optionnel): ")
                actor = input("Acteur (optionnel): ")
                director = input("Réalisateur (optionnel): ")
                genre = input("Genre exact (optionnel): ")
                min_rating = _to_float(input("Note min (optionnel): "))
                max_rating = _to_float(input("Note max (optionnel): "))
                year_from = _to_int(input("Année min (optionnel): "))
                year_to = _to_int(input("Année max (optionnel): "))
                search_advanced(title, actor, director, genre, min_rating, max_rating, year_from, year_to)
            elif choice == "4":
                keywords = input("Mots-clés du synopsis: ").strip()
                search_plot(keywords)
            elif choice == "5":
                fuzzy_query = input("Texte avec fautes éventuelles: ").strip()
                fuzziness = _to_int(input("Niveau de fuzziness (défaut 2): ")) or 2
                search_fuzzy(fuzzy_query, fuzziness=fuzziness)
            elif choice == "6":
                prefix = input("Préfixe du titre: ").strip()
                suggest_titles(prefix)
            elif choice == "7":
                global_stats()
            elif choice == "8":
                top_genres()
                top_directors()
                top_actors()
            elif choice == "9":
                movies_per_decade()
            elif choice == "0":
                print("Fermeture de CinéSearch. À bientôt.")
                break
            else:
                print("Choix invalide. Merci de réessayer.")
        except ValueError:
            print("Saisie numérique invalide.")
        except Exception as exc:
            print(f"Erreur: {exc}")


if __name__ == "__main__":
    run_cli()