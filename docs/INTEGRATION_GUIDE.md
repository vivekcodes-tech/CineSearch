# CineSearch — Team Integration Guide

## 1. Purpose

This document describes the architecture, responsibilities and integration of all four team members in the CineSearch application.

The project integrates movie search algorithms, SQLite database management, ranking and recommendation algorithms, Flask REST APIs and frontend functionality.

The objective is to maintain a modular application where individual components work together without disturbing existing functionality.

## 2. Final Project Architecture

```text
                 FRONTEND
          HTML + CSS + JavaScript
                     |
                     | HTTP / JSON
                     |
                     v
               FLASK BACKEND
                 app.py
                     |
          +----------+----------+
          |          |          |
          v          v          v
     SEARCH API   MOVIE API   USER API
          |          |          |
          v          v          v
     SEARCH       DATABASE    LOGGING
     SERVICE      SERVICES    SERVICE
          |
          v
    INVERTED INDEX
    TRIE AUTOCOMPLETE
    TOP-K ALGORITHM

          RECOMMENDATION API
                     |
                     v
             RANKING SERVICE
                     |
          +----------+----------+
          |          |          |
          v          v          v
       POPULAR    GENRE       PERSONALIZED
                  BASED       RECOMMENDATIONS
                               |
                       +-------+-------+
                       |       |       |
                       v       v       v
                    GENRE   COOCCUR.  JACCARD

                     |
                     v
               SQLITE DATABASE
              cinesearch.db
```

## 3. Student 1 — Search Algorithm Integration

### Responsibilities

Student 1 developed the search-related algorithms and data structures.

### Integrated Components

- Text preprocessing and tokenization.
- Inverted index.
- Trie-based autocomplete.
- Boolean AND/OR search.
- Top-K result selection.

### Integration Files

```text
search/
    __init__.py
    preprocessing.py
    inverted_index.py
    trie.py
    topk.py

backend/services/
    search_service.py
```

### Integration Points

The search service connects the algorithms to Flask endpoints.

- `GET /api/search?q=Interstellar`
- `GET /api/autocomplete?q=In`

The search index currently uses movie titles as indexed text.

## 4. Student 2 — Database Integration

### Responsibilities

Student 2 handled:

- SQLite database creation.
- Movie and genre storage.
- MovieLens dataset import.
- Rating and tag storage.
- Database queries and indexing.
- Data validation.
- Precomputed movie statistics.

### Database Location

`database/cinesearch.db`

### Database Tables

| Table | Purpose |
|---|---|
| movie | Stores movie information |
| genre | Stores genre information |
| movie_genre | Maps movies to genres |
| app_user | Stores user identifiers |
| rating | Stores user ratings |
| tag_event | Stores movie tags |
| movie_stats | Stores precomputed movie statistics |

### Integration Files

```text
database/
    schema.sql
    import_data.py
    indexes.sql
    queries.py
    movie_stats.py
    performance.py
    scalability.py
    transactions.py
    validation.py
```

### Dataset Integration

The project uses the MovieLens 32M dataset.

A deterministic sample of approximately one million ratings was imported instead of the complete 32-million-rating dataset.

The database is connected to the search and recommendation services.

## 5. Student 3 — Ranking and Recommendation Integration

### Responsibilities

Student 3 developed the ranking and recommendation algorithms.

### Integrated Recommendation Methods

#### 5.1 Popular Recommendations

Ranks movies using rating count and average rating through a composite score.

#### 5.2 Genre-Based Recommendations

Filters movies by genre and ranks matching movies using composite scores.

#### 5.3 Genre-Affinity Recommendations

Builds a user genre profile from positively rated movies and recommends unseen movies based on genre affinity.

#### 5.4 User Co-occurrence Recommendations

Identifies users with overlapping positive movie ratings and recommends unseen movies using their positive ratings.

#### 5.5 Jaccard Similarity Recommendations

Calculates similarity between movie rating user sets and recommends similar unseen movies.

### Integration Files

```text
backend/services/
    ranking_service.py

backend/routes/
    recommendation_routes.py
```

### Recommendation APIs

- `/api/recommendations/popular`
- `/api/recommendations/genre/<genre>`
- `/api/recommendations/user/<user_id>/genre-affinity`
- `/api/recommendations/user/<user_id>/cooccurrence`
- `/api/recommendations/user/<user_id>/jaccard`

## 6. Student 4 — Backend and Frontend Integration

### Responsibilities

Student 4 handled:

- Flask application development.
- REST API integration.
- Search and autocomplete integration.
- SQLite connectivity.
- Recommendation API integration.
- Frontend integration.
- Search logging and history.
- API validation and error handling.
- Automated testing.
- Team module integration.

### Backend Structure

```text
backend/
    app.py

    integrations/
        __init__.py
        database_adapter.py
        ranking_adapter.py
        search_adapter.py

    routes/
        __init__.py
        search_routes.py
        movie_routes.py
        rating_routes.py
        user_routes.py
        recommendation_routes.py

    services/
        __init__.py
        search_service.py
        ranking_service.py
        logging_service.py
```

### Frontend Structure

```text
frontend/
    index.html
    style.css
    script.js
```

### Frontend Features

- Movie search.
- Autocomplete suggestions.
- Genre and rating filters.
- Movie details popup.
- Recent search history.
- Popular movie recommendations.
- Genre-based recommendations.
- Genre-affinity recommendations.
- User co-occurrence recommendations.
- Jaccard similarity recommendations.

The frontend communicates with the Flask backend using JavaScript Fetch API requests.

## 7. Shared Data Contract

The integrated application uses consistent movie and user information.

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique movie ID |
| title | String | Movie title |
| year | Integer | Release year |
| release_year | Integer | Release year |
| genre | Array/String | Movie genres, depending on API |
| genres | Array | Movie genres |
| average_rating | Number | Average movie rating |
| rating_count | Integer | Number of ratings |
| user_id | Integer | User identifier |
| rating | Number | Movie rating |

Recommendation APIs return structured JSON responses containing recommendation counts and movie information.

## 8. Integration and Testing Sequence

### Phase 1 — Search Integration

- Integrated preprocessing and tokenization.
- Connected inverted index.
- Connected Trie autocomplete.
- Integrated Boolean AND/OR search.
- Tested Top-K functionality.

### Phase 2 — Database Integration

- Created SQLite database.
- Imported MovieLens data.
- Created database indexes.
- Generated movie statistics.
- Validated database records and foreign keys.

### Phase 3 — Ranking Integration

- Integrated composite popularity scoring.
- Integrated genre recommendations.
- Integrated genre-affinity recommendations.
- Integrated co-occurrence recommendations.
- Integrated Jaccard similarity recommendations.

### Phase 4 — Frontend Integration

- Connected frontend search APIs.
- Integrated autocomplete.
- Connected movie details and ratings.
- Integrated search history interface.
- Added recommendation sections.
- Connected recommendation sections to Flask APIs.

### Phase 5 — Final Testing

- Tested backend APIs.
- Tested frontend functionality.
- Tested recommendation endpoints.
- Verified database connectivity.
- Checked application integration.

**Latest combined automated test result: 39 passed, 0 failed.**

## 9. Git Collaboration Rules

- Each student should work on their assigned feature branch.
- Avoid unnecessary modifications to another student's modules.
- Review code changes before integration.
- Test integrated modules before committing.
- Avoid committing large datasets, local databases, cache folders and temporary files.
- Keep backup files outside the final submission.
- Review the final Git status before staging or pushing changes.

## 10. Current Project Status

| Component | Status |
|---|---|
| Student 1 — Search algorithms | Integrated |
| Student 2 — SQLite database | Integrated |
| Student 3 — Ranking and recommendations | Integrated |
| Student 4 — Flask backend | Integrated |
| Student 4 — Frontend integration | Integrated |
| Recommendation frontend sections | Integrated |
| API testing | 28 tests passed |
| Frontend testing | 11 tests passed |
| Combined testing | 39 tests passed |
| Technical documentation | Updated |
| API documentation | Updated |
| Testing report | Updated |
| Final Git submission | Pending |

## 11. Known Limitations

- The database contains a deterministic sample of MovieLens ratings rather than the complete dataset.
- Search history is currently stored in memory and resets when the Flask application restarts.
- Frontend user ID 101 currently has no rating history in the imported database.
- User 94272 was used for personalized recommendation testing.
- Final team-wide verification and Git submission preparation remain.

## 12. Conclusion

The CineSearch project integrates search algorithms, SQLite database management, ranking and recommendation methods, Flask REST APIs and frontend functionality.

All four students' core modules have been integrated into the application.

The latest combined automated test execution completed successfully with 39 passing tests and zero failures.

The project is ready for final team review, submission preparation and presentation.