# CineSearch — Software Testing Report

## 1. Introduction

This document describes the automated and manual testing performed on the CineSearch application.

The purpose of testing is to verify Flask backend functionality, validate API responses, test frontend interactions, verify database integration and ensure that the application behaves as expected.

Testing covers backend APIs, search algorithms, recommendation services, frontend functionality and database validation.

## 2. Testing Environment

| Component | Technology |
|---|---|
| Programming Language | Python 3.14.10 |
| Backend Framework | Flask |
| Testing Framework | Pytest |
| Frontend Testing | Playwright |
| Database | SQLite |
| Recommendation Algorithms | Python, NumPy, Scikit-learn |
| Frontend | HTML, CSS, JavaScript |
| Operating System | Windows 11 |
| API Format | JSON |
| Browser Testing | Chromium |

## 3. Testing Approach

Three types of verification were performed.

### 3.1 Backend API Testing

Backend testing was performed using Pytest and Flask's built-in test client.

Testing includes:
- Backend health check
- Movie search and autocomplete
- Boolean AND/OR search
- Movie details and ratings
- Search history operations
- Input validation and error handling
- Recommendation API endpoints
- Invalid recommendation limits

### 3.2 Frontend Browser Testing

Frontend testing was performed using Playwright with Chromium.

Testing includes:
- Frontend page loading
- Search input and button
- Search functionality
- Autocomplete suggestions
- Movie details popup
- Popup closing functionality
- Search history section
- Filter controls

### 3.3 Manual Integration Testing

Additional manual verification was performed for:
- SQLite database connectivity
- MovieLens data import
- Search algorithm integration
- Ranking model initialization
- Popular movie recommendations
- Genre-based recommendations
- Personalized recommendation endpoints
- Frontend recommendation display
- Jaccard similarity results

## 4. Backend API Test Cases

A total of 28 automated backend API tests passed.

The tests cover:

- Homepage and health check
- Movie search and empty queries
- Autocomplete and suggestion limits
- Movie details and invalid movie IDs
- Movie ratings and missing movie ratings
- Search history save, retrieval and deletion
- Search-log input validation
- Popular recommendations
- Genre recommendations
- Genre-affinity recommendations
- Co-occurrence recommendations
- Jaccard recommendations
- Invalid recommendation limits

### Recommendation Test Cases

| Test Case | Expected Result |
|---|---|
| Popular recommendations | Movie recommendations returned |
| Genre recommendations | Matching genre movies returned |
| Genre affinity | Valid personalized results or empty results |
| Co-occurrence | Valid recommendations or empty results |
| Jaccard similarity | Recommendations with similarity scores |
| Invalid recommendation limit | Invalid limit handled correctly |

## 5. Frontend Test Cases

A total of 11 automated frontend tests passed using Playwright.

| No. | Test Case | Expected Result |
|---|---|---|
| 1 | Frontend page loading | Page loads successfully |
| 2 | Search input | Search field is available |
| 3 | Search button | Button is available |
| 4 | Filter controls | Filters are visible |
| 5 | Search history section | History section is available |
| 6 | Movie details modal | Modal element exists |
| 7 | Search for Interstellar | Matching movie displayed |
| 8 | Search for Inception | Matching movie displayed |
| 9 | Autocomplete functionality | Suggestions displayed |
| 10 | Movie details popup | Popup opens successfully |
| 11 | Close movie popup | Popup closes successfully |

The recommendation sections were additionally checked manually in the browser.

## 6. Test Execution

### 6.1 Backend API Testing

Command:

```powershell
python -m pytest tests/test_api.py -v
```

Result:

- Total tests: 28
- Passed: 28
- Failed: 0

### 6.2 Frontend Testing

Command:

```powershell
python -m pytest tests/test_frontend.py -v
```

The Flask backend must be running before executing the frontend tests. The Playwright fixture starts its own frontend server.

Result:

- Total tests: 11
- Passed: 11
- Failed: 0

### 6.3 Combined Testing Summary

| Testing Category | Total Tests | Passed | Failed |
|---|---:|---:|---:|
| Backend API Testing | 28 | 28 | 0 |
| Frontend Testing | 11 | 11 | 0 |
| **Total** | **39** | **39** | **0** |

**Latest verified combined execution: 39 passed in 27.90 seconds.**

## 7. Database Validation

The project uses SQLite with the database file:

`database/cinesearch.db`

The database contains:

- Movie records
- Genre records
- Movie-genre relationships
- User records
- Rating records
- Tag records
- Precomputed movie statistics

The MovieLens 32M dataset was used. A deterministic sample of approximately one million ratings was imported instead of the complete ratings dataset.

Database validation included:
- Table creation
- Data import verification
- Record count checks
- Foreign key validation
- Movie statistics validation
- Rating statistics comparison

The movie statistics calculation was benchmarked and showed approximately 49.96x speedup compared with live average calculations in the recorded benchmark.

## 8. Search and Recommendation Verification

### Search

The integrated search implementation uses:
- Text preprocessing and tokenization
- Inverted index
- Boolean AND/OR search
- Trie-based autocomplete
- Top-K result selection

### Recommendations

Five recommendation methods were integrated:

1. Popular recommendations
2. Genre-based recommendations
3. Genre-affinity recommendations
4. User co-occurrence recommendations
5. Jaccard similarity recommendations

The recommendation endpoints were manually tested and automated API tests passed.

The Jaccard implementation returned five recommendations for user 94272 in approximately 4.75 seconds during one recorded test.

## 9. Search History and Current Limitations

Search history operations are currently handled by the in-memory `search_logs` Python list in `backend/services/logging_service.py`.

Therefore:
- Search history can be added, retrieved and cleared during runtime.
- Search history resets when the Flask application restarts.
- Persistent search history storage in SQLite is not currently implemented.

The frontend currently uses user ID 101. This user has no rating history in the imported database, so personalized recommendation sections display informative empty-state messages.

User 94272 was used for personalized recommendation testing.

The imported MovieLens ratings are a sample, not the complete 32-million-rating dataset.

## 10. Code Coverage

The previous testing report recorded 99% backend coverage for an earlier implementation.

That figure has not been re-measured against the latest 28 API tests and should not be treated as the current coverage result.

A fresh coverage run is required before reporting an updated percentage.

## 11. Testing Results

The latest automated test execution confirms:

1. The Flask backend responds successfully.
2. Movie search and autocomplete work.
3. Boolean AND/OR search is integrated.
4. Movie details and ratings APIs work.
5. Search history operations work during runtime.
6. Recommendation APIs return valid responses.
7. Invalid recommendation limits are handled.
8. The frontend loads successfully.
9. Search and autocomplete work through the interface.
10. Movie details popup works.
11. Recommendation sections display results or appropriate empty-state messages.

## 12. Conclusion

CineSearch successfully passed 39 automated tests, including 28 backend API tests and 11 frontend tests.

The project also underwent manual verification of database integration, search algorithms, recommendation services and frontend recommendation display.

The latest combined test execution completed with zero failures.

The application has completed its core backend, database, search, recommendation and frontend integration work. Remaining activities include final team-wide verification, documentation review and Git submission preparation.