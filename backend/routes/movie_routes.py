
from flask import Blueprint, jsonify

from services.search_service import get_movie_by_id

movie_bp = Blueprint("movies", __name__)


@movie_bp.route("/api/movies/<int:movie_id>", methods=["GET"])
def movie_details(movie_id):

    movie = get_movie_by_id(movie_id)

    if movie is None:
        return jsonify({
            "error": "Movie not found"
        }), 404

    return jsonify({
        "movie": movie
    }), 200
