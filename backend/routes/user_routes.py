
from flask import Blueprint, jsonify
from services.logging_service import (
    get_user_search_history,
    clear_user_search_history
)

user_bp = Blueprint("users", __name__)


@user_bp.route("/api/users/<int:user_id>/history", methods=["GET"])
def user_history(user_id):
    history = get_user_search_history(user_id)

    return jsonify({
        "user_id": user_id,
        "total_searches": len(history),
        "history": history
    }), 200


@user_bp.route("/api/users/<int:user_id>/history", methods=["DELETE"])
def delete_user_history(user_id):
    deleted_count = clear_user_search_history(user_id)

    return jsonify({
        "message": "Search history cleared successfully",
        "user_id": user_id,
        "deleted_count": deleted_count
    }), 200
