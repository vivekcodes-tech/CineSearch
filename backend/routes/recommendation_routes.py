
from flask import Blueprint, jsonify, request

from services.ranking_service import (
    recommend_popular,
    recommend_by_genre,
    recommend_genre_affinity,
    recommend_jaccard,
    recommend_cooccurrence
)

recommendation_bp = Blueprint(
    "recommendations",
    __name__
)


def get_limit():
    """Validate recommendation result limit."""
    try:
        limit = int(request.args.get("limit", 10))
    except (TypeError, ValueError):
        return None

    if not 1 <= limit <= 50:
        return None

    return limit


@recommendation_bp.route(
    "/api/recommendations/popular",
    methods=["GET"]
)
def popular_recommendations():

    limit = get_limit()

    if limit is None:
        return jsonify({
            "error": "Limit must be between 1 and 50"
        }), 400

    movies = recommend_popular(limit)

    return jsonify({
        "count": len(movies),
        "recommendations": movies
    }), 200


@recommendation_bp.route(
    "/api/recommendations/genre/<genre>",
    methods=["GET"]
)
def genre_recommendations(genre):

    limit = get_limit()

    if limit is None:
        return jsonify({
            "error": "Limit must be between 1 and 50"
        }), 400

    movies = recommend_by_genre(genre, limit)

    return jsonify({
        "genre": genre,
        "count": len(movies),
        "recommendations": movies
    }), 200
@recommendation_bp.route(
    "/api/recommendations/user/<int:user_id>/genre-affinity",
    methods=["GET"]
)
def personalized_recommendations(user_id):

    limit = get_limit()

    if limit is None:
        return jsonify({
            "error": "Limit must be between 1 and 50"
        }), 400

    movies = recommend_genre_affinity(user_id, limit)

    return jsonify({
        "user_id": user_id,
        "count": len(movies),
        "recommendations": movies
    }), 200
@recommendation_bp.route(
    "/api/recommendations/user/<int:user_id>/cooccurrence",
    methods=["GET"]
)
def cooccurrence_recommendations(user_id):

    limit = get_limit()

    if limit is None:
        return jsonify({
            "error": "Limit must be between 1 and 50"
        }), 400

    movies = recommend_cooccurrence(user_id, limit)

    return jsonify({
        "user_id": user_id,
        "count": len(movies),
        "recommendations": movies
    }), 200
@recommendation_bp.route(
    "/api/recommendations/user/<int:user_id>/jaccard",
    methods=["GET"]
)
def jaccard_recommendations(user_id):

    limit = get_limit()

    if limit is None:
        return jsonify({
            "error": "Limit must be between 1 and 50"
        }), 400

    movies = recommend_jaccard(user_id, limit)

    return jsonify({
        "user_id": user_id,
        "count": len(movies),
        "recommendations": movies
    }), 200