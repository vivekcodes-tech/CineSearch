
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "project": "CineSearch",
        "message": "Backend is running successfully!"
    })


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "CineSearch API"
    })


if __name__ == "__main__":
    app.run(debug=True)

movies = [
    {
        "id": 1,
        "title": "Toy Story",
        "year": 1995,
        "genre": "Animation, Comedy"
    },
    {
        "id": 2,
        "title": "Interstellar",
        "year": 2014,
        "genre": "Adventure, Sci-Fi"
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "year": 2008,
        "genre": "Action, Drama"
    },
    {
        "id": 4,
        "title": "Inception",
        "year": 2010,
        "genre": "Action, Sci-Fi"
    }
]


@app.route("/api/search")
def search_movies():
    from flask import request

    query = request.args.get("q", "").strip().lower()

    if not query:
        return jsonify({
            "error": "Please enter a movie name"
        }), 400

    results = [
        movie for movie in movies
        if query in movie["title"].lower()
    ]

    return jsonify({
        "query": query,
        "total_results": len(results),
        "results": results
    })