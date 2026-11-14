
import sqlite3
from pathlib import Path

from search.topk import get_top_k
from search.preprocessing import tokenize
from search.inverted_index import InvertedIndex
from search.trie import PrefixTrie


# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "cinesearch.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# --------------------------------------------------
# LOAD MOVIES FROM SQLITE
# --------------------------------------------------

def load_movies():

    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT
                m.movie_id,
                m.title,
                m.release_year,
                GROUP_CONCAT(g.genre_name, '|') AS genres
            FROM movie AS m
            LEFT JOIN movie_genre AS mg
                ON m.movie_id = mg.movie_id
            LEFT JOIN genre AS g
                ON mg.genre_id = g.genre_id
            GROUP BY m.movie_id
            ORDER BY m.movie_id
        """).fetchall()

        result = []

        for row in rows:
            genres = (
                row["genres"].split("|")
                if row["genres"]
                else []
            )

            result.append({
                "id": row["movie_id"],
                "title": row["title"],
                "year": row["release_year"],
                "release_year": row["release_year"],
                "genre": genres,
                "genres": genres
            })

        return result

    finally:
        connection.close()


# --------------------------------------------------
# INITIALIZE SEARCH DATA STRUCTURES
# --------------------------------------------------

movies = load_movies()

movie_lookup = {
    movie["id"]: movie
    for movie in movies
}

movie_index = InvertedIndex()
movie_trie = PrefixTrie()

for movie in movies:
    movie_id = movie["id"]
    title = movie["title"]

    movie_index.add_document(movie_id, title)
    movie_trie.insert(title)


# --------------------------------------------------
# SEARCH WITH INVERTED INDEX + TOP-K RANKING
# --------------------------------------------------

def search_movies(query, mode="and", limit=10):

    if not query or not query.strip():
        return []

    if limit <= 0:
        return []

    query = query.strip()
    tokens = tokenize(query)

    # Handle stop-word-only queries.
    if not tokens:
        matched_movies = [
            movie for movie in movies
            if query.lower() in movie["title"].lower()
        ]

        return matched_movies[:limit]

    # Retrieve matching movie IDs.
    if mode == "or":
        matched_ids = movie_index.boolean_or(tokens)
    else:
        matched_ids = movie_index.boolean_and(tokens)

    # Calculate relevance scores.
    score_dict = {}

    query_terms = set(tokens)

    for movie_id in matched_ids:

        if movie_id not in movie_lookup:
            continue

        title_tokens = set(
            tokenize(movie_lookup[movie_id]["title"])
        )

        matched_terms = query_terms.intersection(title_tokens)

        score = len(matched_terms) / len(query_terms)

        score_dict[movie_id] = score

    # Select the highest-scoring K movies.
    top_results = get_top_k(score_dict, k=limit)

    return [
        movie_lookup[movie_id]
        for movie_id, score in top_results
    ]


# --------------------------------------------------
# AUTOCOMPLETE
# --------------------------------------------------

def autocomplete_movies(query, limit=5):

    if not query or not query.strip():
        return []

    if limit <= 0:
        return []

    return movie_trie.search_prefix(query, limit)


# --------------------------------------------------
# MOVIE DETAILS
# --------------------------------------------------

def get_movie_by_id(movie_id):

    return movie_lookup.get(movie_id)


# --------------------------------------------------
# MOVIE RATINGS FROM SQLITE
# --------------------------------------------------

def get_movie_ratings(movie_id):

    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT user_id, rating
            FROM rating
            WHERE movie_id = ?
            ORDER BY user_id
        """, (movie_id,)).fetchall()

        return [
            {
                "user_id": row["user_id"],
                "rating": row["rating"]
            }
            for row in rows
        ]

    finally:
        connection.close()
