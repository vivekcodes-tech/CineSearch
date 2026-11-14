
import sys
from pathlib import Path

import pytest

# Add the backend directory to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_PATH = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_PATH))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200


def test_health_check(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_movie_search(client):
    response = client.get("/api/search?q=Interstellar")

    assert response.status_code == 200
    assert response.json["total_results"] >= 1
    assert isinstance(response.json["results"], list)


def test_search_without_query(client):
    response = client.get("/api/search")

    assert response.status_code == 400


def test_autocomplete(client):
    response = client.get("/api/autocomplete?q=In")

    assert response.status_code == 200
    assert isinstance(response.json["suggestions"], list)


def test_movie_details(client):
    response = client.get("/api/movies/1")

    assert response.status_code == 200
    assert response.json is not None


def test_movie_not_found(client):
    response = client.get("/api/movies/999999")

    assert response.status_code == 404


def test_movie_ratings(client):
    response = client.get("/api/movies/1/ratings")

    assert response.status_code == 200
    assert response.json is not None


def test_search_history_workflow(client):
    user_id = 987654321

    # Remove any previous test history.
    client.delete(f"/api/users/{user_id}/history")

    # Save a search.
    save_response = client.post(
        "/api/search-log",
        json={
            "user_id": user_id,
            "query": "Interstellar"
        }
    )

    assert save_response.status_code == 201

    # Retrieve search history.
    history_response = client.get(
        f"/api/users/{user_id}/history"
    )

    assert history_response.status_code == 200
    assert history_response.json["total_searches"] == 1
    assert history_response.json["history"][0]["query"] == "Interstellar"

    # Clear search history.
    delete_response = client.delete(
        f"/api/users/{user_id}/history"
    )

    assert delete_response.status_code == 200
    assert delete_response.json["deleted_count"] == 1

    # Verify history is empty.
    final_response = client.get(
        f"/api/users/{user_id}/history"
    )

    assert final_response.status_code == 200
    assert final_response.json["total_searches"] == 0

def test_autocomplete_without_query(client):
    response = client.get("/api/autocomplete")

    assert response.status_code == 400
    assert response.json["error"] == "Please enter a search query"


def test_search_log_without_json(client):
    response = client.post(
        "/api/search-log",
        data="",
        content_type="application/json"
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    "payload",
    [
        {"query": "Interstellar"},
        {"user_id": 0, "query": "Interstellar"},
        {"user_id": -1, "query": "Interstellar"},
        {"user_id": True, "query": "Interstellar"},
        {"user_id": "101", "query": "Interstellar"},
        {"user_id": 101, "query": ""}
    ]
)
def test_invalid_search_log(client, payload):
    response = client.post(
        "/api/search-log",
        json=payload
    )

    assert response.status_code == 400


def test_search_service_empty_query():
    from services.search_service import search_movies

    assert search_movies("") == []
    assert search_movies("   ") == []


def test_autocomplete_service_empty_query():
    from services.search_service import autocomplete_movies

    assert autocomplete_movies("") == []
    assert autocomplete_movies("   ") == []


def test_autocomplete_limit():
    from services.search_service import autocomplete_movies

    results = autocomplete_movies("I", limit=1)

    assert len(results) == 1


def test_movie_without_ratings(client):
    response = client.get("/api/movies/51/ratings")

    assert response.status_code == 200
    assert response.json["total_ratings"] == 0
    assert response.json["average_rating"] == 0


def test_ratings_for_missing_movie(client):
    response = client.get("/api/movies/999999/ratings")

    assert response.status_code == 404
    assert response.json["error"] == "Movie not found"

# --------------------------------------------------
# RECOMMENDATION API TESTS
# --------------------------------------------------

def test_popular_recommendations(client):
    response = client.get("/api/recommendations/popular?limit=5")

    assert response.status_code == 200
    assert response.json["count"] == 5
    assert len(response.json["recommendations"]) == 5


def test_genre_recommendations(client):
    response = client.get("/api/recommendations/genre/Comedy?limit=5")

    assert response.status_code == 200
    assert response.json["genre"] == "Comedy"
    assert response.json["count"] == 5


def test_genre_affinity_recommendations(client):
    response = client.get(
        "/api/recommendations/user/94272/genre-affinity?limit=5"
    )

    assert response.status_code == 200
    assert response.json["user_id"] == 94272
    assert response.json["count"] == 5


def test_cooccurrence_recommendations(client):
    response = client.get(
        "/api/recommendations/user/94272/cooccurrence?limit=5"
    )

    assert response.status_code == 200
    assert response.json["user_id"] == 94272
    assert response.json["count"] == 5


def test_jaccard_recommendations(client):
    response = client.get(
        "/api/recommendations/user/94272/jaccard?limit=5"
    )

    assert response.status_code == 200
    assert response.json["user_id"] == 94272
    assert response.json["count"] == 5

    for movie in response.json["recommendations"]:
        assert "jaccard_similarity" in movie
        assert 0 <= movie["jaccard_similarity"] <= 1


def test_invalid_recommendation_limit(client):
    response = client.get(
        "/api/recommendations/popular?limit=100"
    )

    assert response.status_code == 400
