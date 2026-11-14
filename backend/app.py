
import sys
from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS

# Add the CineSearch project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from routes.movie_routes import movie_bp
from routes.search_routes import search_bp
from routes.rating_routes import rating_bp
from routes.user_routes import user_bp
from routes.recommendation_routes import recommendation_bp

# Initialize Flask application
app = Flask(__name__)

# Enable frontend communication
CORS(app)

# Register API routes
app.register_blueprint(search_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(rating_bp)
app.register_blueprint(user_bp)
app.register_blueprint(recommendation_bp)

# Home API
@app.route("/")
def home():
    return jsonify({
        "project": "CineSearch",
        "message": "Backend is running successfully!"
    })


# Health check API
@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "CineSearch API"
    })


# Start server
if __name__ == "__main__":
    app.run(debug=True)
