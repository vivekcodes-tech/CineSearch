def search_movies(query, movies):
    """
    Adapter for Student 1's movie search algorithm.

    Args:
        query: Movie title or keyword.
        movies: List of movie dictionaries.

    Returns:
        List of matching movie dictionaries.
    """
    if not query or not query.strip():
        return []

    query = query.strip().lower()

    return [
        movie for movie in movies
        if query in movie.get("title", "").lower()
    ]


def autocomplete_movies(query, movies, limit=5):
    """
    Adapter for movie autocomplete.

    Returns:
        List of matching movie titles.
    """
    if not query or not query.strip():
        return []

    query = query.strip().lower()

    suggestions = [
        movie["title"]
        for movie in movies
        if movie.get("title", "").lower().startswith(query)
    ]

    return suggestions[:limit]