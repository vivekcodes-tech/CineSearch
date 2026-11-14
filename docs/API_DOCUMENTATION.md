# CineSearch API Documentation

## 1. Project Overview

CineSearch is a movie search and recommendation system developed using Python Flask, SQLite and frontend web technologies.

The application provides movie search, autocomplete, movie details, ratings, search history and multiple recommendation algorithms through REST APIs.

**Base URL:** `http://127.0.0.1:5000`

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | REST API development |
| SQLite | Database management |
| NumPy | Numerical operations |
| Scikit-learn | TF-IDF vectorization and cosine similarity |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend functionality and API communication |
| Pytest | Automated testing |
| Git and GitHub | Version control and collaboration |

## 3. API Endpoints

### 3.1 Health Check

**Endpoint:** `GET /api/health`

**Purpose:** Checks whether the backend server is running.

Example:

```http
GET /api/health
```

### 3.2 Search Movies

**Endpoint:** `GET /api/search?q=movie_name`

**Purpose:** Searches movies using the integrated inverted index.

**Query Parameters:**

| Parameter | Required | Description |
|---|---|---|
| `q` | Yes | Movie search query |
| `mode` | No | Search mode: `and` or `or`. Default is `and`. |

**Boolean Search Modes:**

- **AND (`mode=and`):** Returns movies containing all query terms.
- **OR (`mode=or`):** Returns movies containing at least one query term.

Example:

```http
GET /api/search?q=Interstellar
```

Boolean OR example:

```http
GET /api/search?q=interstellar%20inception&mode=or
```

The search service uses movie titles for indexed search.

### 3.3 Movie Autocomplete

**Endpoint:** `GET /api/autocomplete?q=movie_name`

**Purpose:** Returns movie suggestions while the user types.

Example:

```http
GET /api/autocomplete?q=In
```

The autocomplete functionality uses the integrated Trie data structure.

### 3.4 Get Movie Details

**Endpoint:** `GET /api/movies/<movie_id>`

**Purpose:** Retrieves details of a movie using its ID.

Example:

```http
GET /api/movies/1
```

### 3.5 Get Movie Ratings

**Endpoint:** `GET /api/movies/<movie_id>/ratings`

**Purpose:** Retrieves rating information for a movie.

Example:

```http
GET /api/movies/1/ratings
```

### 3.6 Save Search History

**Endpoint:** `POST /api/search-log`

**Purpose:** Saves a user's search query during the current application runtime.

Request body:

```json
{
  "user_id": 101,
  "query": "Interstellar"
}
```

### 3.7 Get User Search History

**Endpoint:** `GET /api/users/<user_id>/history`

**Purpose:** Retrieves previous searches of a particular user.

Example:

```http
GET /api/users/101/history
```

### 3.8 Clear User Search History

**Endpoint:** `DELETE /api/users/<user_id>/history`

**Purpose:** Deletes the search history of a particular user.

Example:

```http
DELETE /api/users/101/history
```

**Important:** Search history is currently stored in memory and resets when the Flask application restarts.

## 4. Recommendation APIs

CineSearch provides five recommendation methods through dedicated REST endpoints.

### 4.1 Popular Recommendations

**Endpoint:** `GET /api/recommendations/popular?limit=5`

**Purpose:** Returns popular movies ranked using rating count and average rating.

Example:

```http
GET /api/recommendations/popular?limit=5
```

### 4.2 Genre-Based Recommendations

**Endpoint:** `GET /api/recommendations/genre/<genre>?limit=5`

**Purpose:** Returns movies belonging to the selected genre, ranked using composite scores.

Example:

```http
GET /api/recommendations/genre/Comedy?limit=5
```

### 4.3 Genre-Affinity Recommendations

**Endpoint:** `GET /api/recommendations/user/<user_id>/genre-affinity?limit=5`

**Purpose:** Builds a user genre profile using positively rated movies and recommends unseen movies based on genre affinity.

Example:

```http
GET /api/recommendations/user/94272/genre-affinity?limit=5
```

### 4.4 User Co-occurrence Recommendations

**Endpoint:** `GET /api/recommendations/user/<user_id>/cooccurrence?limit=5`

**Purpose:** Uses overlapping positive ratings between users to identify potential movie recommendations.

Example:

```http
GET /api/recommendations/user/94272/cooccurrence?limit=5
```

### 4.5 Jaccard Similarity Recommendations

**Endpoint:** `GET /api/recommendations/user/<user_id>/jaccard?limit=5`

**Purpose:** Calculates Jaccard similarity between movie rating user sets and recommends similar unseen movies.

Example:

```http
GET /api/recommendations/user/94272/jaccard?limit=5
```

### Recommendation Response Structure

Recommendation endpoints return JSON containing fields such as:

- `count`
- `recommendations`
- `user_id` or `genre`, where applicable

Movie recommendation objects include:

- `id`
- `title`
- `year`
- `release_year`
- `genre` / `genres`
- `average_rating`
- `rating_count`

The exact additional fields depend on the endpoint.

## 5. Database Integration

The project uses SQLite.

**Database path:**

`database/cinesearch.db`

The database contains:

- `movie`
- `genre`
- `movie_genre`
- `app_user`
- `rating`
- `tag_event`
- `movie_stats`

The MovieLens 32M dataset was used. A deterministic sample of approximately one million ratings was imported rather than the entire ratings dataset.

The `movie_stats` table stores precomputed rating counts and average ratings for recommendation calculations.

## 6. HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created, where applicable |
| 400 | Invalid request |
| 404 | Resource not found |
| 500 | Internal server error |

## 7. Frontend Integration

The frontend communicates with the Flask backend using JavaScript Fetch API requests.

Implemented features include:

- Movie search
- Autocomplete suggestions
- Genre and minimum-rating filters
- Movie details popup
- Recent search history
- Popular recommendations
- Genre-based recommendations
- Genre-affinity recommendations
- User co-occurrence recommendations
- Jaccard similarity recommendations

The recommendation cards display movie titles, release years, genres, average ratings and rating counts.

When personalized recommendations are unavailable, the frontend displays informative empty-state messages.

## 8. Team Integration Responsibilities

| Team Member | Responsibility | Integration Point |
|---|---|---|
| Student 1 | Search algorithms | Search service |
| Student 2 | Database management | SQLite database |
| Student 3 | Ranking and recommendations | Ranking service |
| Student 4 | Backend APIs, frontend and integration | Flask routes and frontend |

## 9. Testing Results

The latest combined automated test execution reported:

| Testing Category | Total Tests | Passed | Failed |
|---|---:|---:|---:|
| Backend API tests | 28 | 28 | 0 |
| Frontend tests | 11 | 11 | 0 |
| **Total** | **39** | **39** | **0** |

The recommendation APIs were also manually checked through HTTP requests, and the frontend recommendation sections were manually verified.

## 10. Running the Project

Open PowerShell in the project root.

**Start the backend:**

```powershell
python backend/app.py
```

Keep this terminal running.

**Start the frontend in another terminal:**

```powershell
Set-Location frontend
python -m http.server 5500
```

**Open the frontend:**

`http://127.0.0.1:5500`

**Backend API:**

`http://127.0.0.1:5000`

## 11. Current Implementation Notes

- Movie search uses the integrated title-based inverted index.
- Autocomplete uses a Trie.
- Recommendation algorithms are integrated into the Flask backend.
- Search history is stored in memory and is not persistent across server restarts.
- Personalized recommendation results depend on the selected user's rating history.
- User 101 currently has no rating history in the imported database; user 94272 was used for personalized recommendation testing.
- The latest combined automated test suite passed all 39 tests.