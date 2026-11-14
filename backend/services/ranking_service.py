
import sqlite3
import math
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "cinesearch.db"

_movies_cache = []
_title_vectorizer = None
_genre_vectorizer = None
_title_matrix = None
_genre_matrix = None
_composite_scores = {}


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def load_ranking_data():
    connection = get_connection()
    try:
        rows = connection.execute("""
            SELECT m.movie_id, m.title, m.release_year,
                   GROUP_CONCAT(g.genre_name, '|') AS genres,
                   COALESCE(ms.rating_count, 0) AS rating_count,
                   COALESCE(ms.average_rating, 0) AS average_rating
            FROM movie m
            LEFT JOIN movie_genre mg ON m.movie_id = mg.movie_id
            LEFT JOIN genre g ON mg.genre_id = g.genre_id
            LEFT JOIN movie_stats ms ON m.movie_id = ms.movie_id
            GROUP BY m.movie_id
            ORDER BY m.movie_id
        """).fetchall()

        movies = []
        for row in rows:
            genres = row["genres"].split("|") if row["genres"] else []
            movies.append({
                "id": row["movie_id"],
                "title": row["title"],
                "year": row["release_year"],
                "release_year": row["release_year"],
                "genre": genres,
                "genres": genres,
                "rating_count": row["rating_count"],
                "average_rating": row["average_rating"]
            })
        return movies
    finally:
        connection.close()


def prepare_ranking_models():
    global _movies_cache, _title_vectorizer
    global _genre_vectorizer, _title_matrix, _genre_matrix
    global _composite_scores

    if _movies_cache:
        return

    _movies_cache = load_ranking_data()
    if not _movies_cache:
        return

    counts = [m["rating_count"] for m in _movies_cache]
    max_count = max(counts, default=0)
    max_log = math.log1p(max_count) if max_count else 1

    for movie in _movies_cache:
        popularity = math.log1p(movie["rating_count"]) / max_log
        rating_score = movie["average_rating"] / 5
        _composite_scores[movie["id"]] = (
            0.5 * popularity + 0.5 * rating_score
        )

    titles = [m["title"] or "" for m in _movies_cache]
    genres = [" ".join(m["genres"]) for m in _movies_cache]

    _title_vectorizer = TfidfVectorizer(
        stop_words="english", ngram_range=(1, 2)
    )
    _title_matrix = _title_vectorizer.fit_transform(titles)

    _genre_vectorizer = TfidfVectorizer(
        token_pattern=r"(?u)\b\w+\b"
    )
    _genre_matrix = _genre_vectorizer.fit_transform(genres)


def rank_movies(query, limit=10):
    prepare_ranking_models()
    if not query or not query.strip() or not _movies_cache:
        return []

    title_query = _title_vectorizer.transform([query])
    genre_query = _genre_vectorizer.transform([query])

    title_scores = cosine_similarity(title_query, _title_matrix).flatten()
    genre_scores = cosine_similarity(genre_query, _genre_matrix).flatten()
    scores = 0.7 * title_scores + 0.3 * genre_scores

    ranked = scores.argsort()[::-1][:limit]
    return [
        {**_movies_cache[i], "search_score": round(float(scores[i]), 4)}
        for i in ranked if scores[i] > 0
    ]


def recommend_popular(limit=10):
    prepare_ranking_models()
    return sorted(
        _movies_cache,
        key=lambda m: _composite_scores.get(m["id"], 0),
        reverse=True
    )[:limit]


def recommend_by_genre(genre, limit=10):
    prepare_ranking_models()
    matches = [
        m for m in _movies_cache
        if any(g.lower() == genre.lower() for g in m["genres"])
    ]
    return sorted(
        matches,
        key=lambda m: _composite_scores.get(m["id"], 0),
        reverse=True
    )[:limit]


def build_user_genre_profile(user_id):
    connection = get_connection()
    try:
        rows = connection.execute("""
            SELECT mg.genre_id, g.genre_name, AVG(r.rating) AS avg_rating
            FROM rating r
            JOIN movie_genre mg ON r.movie_id = mg.movie_id
            JOIN genre g ON mg.genre_id = g.genre_id
            WHERE r.user_id = ? AND r.rating >= 3.5
            GROUP BY mg.genre_id
        """, (user_id,)).fetchall()
    finally:
        connection.close()

    total = sum(row["avg_rating"] for row in rows)
    if not total:
        return {}

    return {
        row["genre_name"]: row["avg_rating"] / total
        for row in rows
    }


def recommend_genre_affinity(user_id, limit=10):
    prepare_ranking_models()
    profile = build_user_genre_profile(user_id)
    if not profile:
        return []

    connection = get_connection()
    try:
        seen = {
            row["movie_id"] for row in connection.execute(
                "SELECT movie_id FROM rating WHERE user_id = ?",
                (user_id,)
            ).fetchall()
        }
    finally:
        connection.close()

    results = []
    for movie in _movies_cache:
        if movie["id"] in seen:
            continue

        affinity = sum(
            profile.get(g, 0) for g in movie["genres"]
        )
        score = (
            0.7 * affinity
            + 0.3 * _composite_scores.get(movie["id"], 0)
        )
        if score > 0:
            item = movie.copy()
            item["personalized_score"] = round(score, 4)
            results.append(item)

    return sorted(
        results,
        key=lambda m: m["personalized_score"],
        reverse=True
    )[:limit]


def recommend_cooccurrence(user_id, limit=10):
    prepare_ranking_models()
    connection = get_connection()
    try:
        rows = connection.execute("""
            SELECT user_id, movie_id
            FROM rating WHERE rating >= 3.5
        """).fetchall()
        seen = {
            row["movie_id"] for row in connection.execute(
                "SELECT movie_id FROM rating WHERE user_id = ?",
                (user_id,)
            ).fetchall()
        }
    finally:
        connection.close()

    user_movies = {}
    for row in rows:
        user_movies.setdefault(row["user_id"], set()).add(row["movie_id"])

    target = user_movies.get(user_id, set())
    if not target:
        return []

    similar_users = {
        uid for uid, movies in user_movies.items()
        if uid != user_id and movies.intersection(target)
    }

    counts = {}
    for uid in similar_users:
        for mid in user_movies[uid]:
            if mid not in seen:
                counts[mid] = counts.get(mid, 0) + 1

    lookup = {m["id"]: m for m in _movies_cache}
    results = []
    for mid, count in sorted(
        counts.items(), key=lambda x: x[1], reverse=True
    )[:limit]:
        if mid in lookup:
            item = lookup[mid].copy()
            item["cooccurrence_count"] = count
            results.append(item)
    return results



def recommend_jaccard(user_id, limit=10, min_common_users=5):
    """
    Recommend unseen movies using pairwise Jaccard similarity.

    Jaccard(A, B) = intersection / union
    A and B are sets of users who positively rated two movies.
    """

    if limit <= 0 or min_common_users <= 0:
        return []

    prepare_ranking_models()

    if not _movies_cache:
        return []

    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT user_id, movie_id
            FROM rating
            WHERE rating >= 3.5
        """).fetchall()

        seen_rows = connection.execute("""
            SELECT movie_id
            FROM rating
            WHERE user_id = ?
        """, (user_id,)).fetchall()

    finally:
        connection.close()

    seen = {row["movie_id"] for row in seen_rows}

    movie_users = {}
    user_movies = {}

    for row in rows:
        uid = row["user_id"]
        mid = row["movie_id"]

        movie_users.setdefault(mid, set()).add(uid)
        user_movies.setdefault(uid, set()).add(mid)

    target_movies = user_movies.get(user_id, set())

    if not target_movies:
        return []

    candidate_scores = {}

    # Count common users without repeatedly calculating set intersections.
    for target_id in target_movies:

        target_users = movie_users.get(target_id, set())
        intersection_counts = {}

        for uid in target_users:
            for candidate_id in user_movies.get(uid, ()):

                if candidate_id in seen:
                    continue

                intersection_counts[candidate_id] = (
                    intersection_counts.get(candidate_id, 0) + 1
                )

        # Calculate Jaccard similarity for each candidate.
        for candidate_id, intersection in intersection_counts.items():

            if intersection < min_common_users:
                continue

            candidate_user_count = len(
                movie_users.get(candidate_id, ())
            )

            union = (
                len(target_users)
                + candidate_user_count
                - intersection
            )

            if union <= 0:
                continue

            similarity = intersection / union

            current = candidate_scores.get(candidate_id, 0)

            if similarity > current:
                candidate_scores[candidate_id] = similarity

    ranked = sorted(
        candidate_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )[:limit]

    lookup = {
        movie["id"]: movie
        for movie in _movies_cache
    }

    results = []

    for mid, similarity in ranked:

        movie = lookup.get(mid)

        if movie is None:
            continue

        item = movie.copy()
        item["jaccard_similarity"] = round(similarity, 4)
        results.append(item)

    return results
