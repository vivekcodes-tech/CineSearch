
from flask import Blueprint, jsonify

from services.search_service import (
    get_movie_by_id,
    get_movie_ratings
)

rating_bp = Blueprint("ratings", __name__)


@rating_bp.route(
    "/api/movies/<int:movie_id>/ratings",
    methods=["GET"]
)
def movie_ratings(movie_id):

    movie = get_movie_by_id(movie_id)

    if movie is None:
        return jsonify({
            "error": "Movie not found"
        }), 404

    ratings = get_movie_ratings(movie_id)

    average = (
        sum(item["rating"] for item in ratings) / len(ratings)
        if ratings else 0
    )

    return jsonify({
        "movie_id": movie_id,
        "movie_title": movie["title"],
        "total_ratings": len(ratings),
        "average_rating": round(average, 2),
        "ratings": ratings
    }), 200

