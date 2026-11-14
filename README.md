
# CineSearch

**A Database-Driven Search, Ranking and Recommendation Engine**

CineSearch is a movie discovery application that integrates search algorithms, database management, ranking techniques and personalized movie recommendations.

## 1. Features

- Movie search using an inverted index.
- Boolean AND/OR search.
- Trie-based autocomplete.
- Top-K movie ranking.
- Movie details and ratings.
- Popular movie recommendations.
- Genre-based recommendations.
- Personalized genre-affinity recommendations.
- User co-occurrence recommendations.
- Jaccard similarity recommendations.
- Search history.
- Interactive web frontend.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| API communication | REST API, JSON |
| Database | SQLite |
| Search | Inverted Index, Trie |
| Ranking | TF-IDF, Cosine Similarity |
| Recommendations | Genre Affinity, Co-occurrence, Jaccard Similarity |
| Dataset | MovieLens 32M |
| Testing | Pytest |

## 3. Project Structure

```text
CineSearch/
│
├── backend/
│   ├── app.py
│   ├── integrations/
│   ├── routes/
│   └── services/
│
├── database/
│   ├── schema.sql
│   ├── import_data.py
│   ├── indexes.sql
│   ├── movie_stats.py
│   ├── performance.py
│   ├── queries.py
│   ├── scalability.py
│   ├── transactions.py
│   └── validation.py
│
├── data/
│   └── ml-32m/
│
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── INTEGRATION_GUIDE.md
│   └── Testing_Report.md
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── README.md
│
├── search/
│   ├── preprocessing.py
│   ├── inverted_index.py
│   ├── trie.py
│   └── topk.py
│
├── tests/
│   ├── test_api.py
│   ├── test_frontend.py
│   └── test_search.py
│
├── .gitignore
├── README.md
└── Technical_Documentation.txt
```

## 4. Requirements

- Python 3
- pip
- Git
- Web browser

Python dependencies:

```powershell
pip install Flask flask-cors numpy pandas scikit-learn pytest
```

Install any additional dependencies required by the test environment if necessary.

## 5. Dataset Setup

CineSearch uses the MovieLens 32M dataset.

1. Download the MovieLens 32M dataset.
2. Extract the dataset into the `data/ml-32m/` directory.
3. Ensure that the following files are available:

```text
data/ml-32m/
    movies.csv
    ratings.csv
    tags.csv
    links.csv
```

The database importer uses a deterministic sample of ratings rather than importing the complete 32-million-rating dataset.

## 6. Database Setup

Run these commands from the project root directory.

Create and populate the SQLite database:

```powershell
python database/import_data.py
```

Generate precomputed movie statistics:

```powershell
python database/movie_stats.py
```

The database is created at:

```text
database/cinesearch.db
```

The local database file is excluded from Git. It can be recreated using the database scripts and dataset.

## 7. Run the Application

### Step 1: Open the project directory

```powershell
cd CineSearch
```

### Step 2: Start the Flask backend

```powershell
python backend/app.py
```

Keep this terminal running.

The backend runs locally at:

```text
http://127.0.0.1:5000
```

### Step 3: Start the frontend

Open another terminal from the project root:

```powershell
python -m http.server 5500
```

Open the following address in your browser:

```text
http://127.0.0.1:5500/frontend/
```

Make sure the Flask backend is running before using the frontend.

## 8. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Backend health check |
| GET | `/api/search?q=Interstellar` | Search movies |
| GET | `/api/autocomplete?q=In` | Autocomplete |
| GET | `/api/movies/<movie_id>` | Movie details |
| GET | `/api/movies/<movie_id>/ratings` | Movie ratings |
| POST | `/api/search-log` | Save a search |
| GET | `/api/users/<user_id>/history` | Get search history |
| DELETE | `/api/users/<user_id>/history` | Clear search history |
| GET | `/api/recommendations/popular` | Popular movies |
| GET | `/api/recommendations/genre/Comedy` | Genre recommendations |
| GET | `/api/recommendations/user/<user_id>/genre-affinity` | Genre-affinity recommendations |
| GET | `/api/recommendations/user/<user_id>/cooccurrence` | Co-occurrence recommendations |
| GET | `/api/recommendations/user/<user_id>/jaccard` | Jaccard recommendations |

For complete API details, see `docs/API_DOCUMENTATION.md`.

## 9. Run Tests

Run the combined API and frontend tests:

```powershell
python -m pytest tests/test_api.py tests/test_frontend.py -v
```

Run the search module tests:

```powershell
python -m tests.test_search
```

The latest verified results were:

- API tests: 28 passed.
- Frontend tests: 11 passed.
- Combined tests: 39 passed.
- Search module checks: all passed.

## 10. Important Notes

- Search history is currently stored in memory and resets when the Flask application restarts.
- The frontend currently uses user ID `101` by default.
- Personalized recommendations require suitable user rating history.
- The database uses a sampled subset of MovieLens ratings.
- The local dataset and SQLite database are excluded from Git.

## 11. Documentation

Additional project documentation:

- `Technical_Documentation.txt` — Technical overview and implementation details.
- `docs/API_DOCUMENTATION.md` — API reference.
- `docs/INTEGRATION_GUIDE.md` — Team integration and architecture.
- `docs/Testing_Report.md` — Testing results.

## 12. Team Contributions

The project was developed through four integrated responsibilities:

- **Student 1:** Search algorithms and data structures.
- **Student 2:** Database design, data import and validation.
- **Student 3:** Ranking and recommendation algorithms.
- **Student 4:** Flask backend, frontend integration, API development, logging and testing.

---

**CineSearch — Making movie discovery smarter through search, ranking and recommendations.**