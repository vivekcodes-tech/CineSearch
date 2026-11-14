
const API = "http://127.0.0.1:5000";
const USER_ID = 101;

const $ = id => document.getElementById(id);

let currentMovies = [];
let timer;

function genresOf(movie) {
  const value = movie.genre ?? movie.genres ?? [];
  return Array.isArray(value)
    ? value
    : String(value).split(/[,|]/).map(x => x.trim()).filter(Boolean);
}

function ratingOf(movie) {
  const value = movie.rating ?? movie.vote_average;
  return value === undefined || value === null || value === ""
    ? null : Number(value);
}

function safe(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;",
    '"': "&quot;", "'": "&#39;"
  }[c]));
}

async function search(query) {
  const response = await fetch(
    `${API}/api/search?q=${encodeURIComponent(query)}`
  );
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return Array.isArray(data.results) ? data.results : [];
}

async function autocomplete(query) {
  const response = await fetch(
    `${API}/api/autocomplete?q=${encodeURIComponent(query)}`
  );
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return Array.isArray(data.suggestions) ? data.suggestions : [];
}

async function getMovieRatings(movieId) {
  const response = await fetch(`${API}/api/movies/${movieId}/ratings`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data;
}

async function getMovieDetails(movieId) {
  const response = await fetch(`${API}/api/movies/${movieId}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data.movie ?? data;
}

// Save a successful search in backend history
async function saveSearch(query) {
  const response = await fetch(`${API}/api/search-log`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: USER_ID,
      query: query
    })
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Could not save search");
  }

  return data;
}

// Load search history
async function loadHistory() {
  $("historyStatus").textContent = "Loading search history...";

  try {
    const response = await fetch(
      `${API}/api/users/${USER_ID}/history`
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Could not load history");
    }

    renderHistory(data.history || []);

    $("historyStatus").textContent =
      `${data.total_searches} saved search${data.total_searches === 1 ? "" : "es"}`;

  } catch (error) {
    console.error("History error:", error);
    $("historyStatus").textContent =
      "Could not load search history. Check the backend.";
  }
}

// Display search history
function renderHistory(history) {
  if (!history.length) {
    $("historyList").innerHTML =
      '<div class="history-empty">No recent searches yet. Start exploring movies!</div>';
    return;
  }

  $("historyList").innerHTML = history.map(item => {
    const date = new Date(item.timestamp);

    const formattedDate = Number.isNaN(date.getTime())
      ? "Date unavailable"
      : date.toLocaleString();

    return `
      <div class="history-item">
        <div>
          <div class="history-query"
               data-query="${safe(item.query)}"
               tabindex="0"
               role="button">
            ${safe(item.query)}
          </div>
          <div class="history-time">${safe(formattedDate)}</div>
        </div>
        <span class="history-open">Search again →</span>
      </div>
    `;
  }).join("");

  $("historyList").querySelectorAll(".history-query").forEach(item => {
    const repeatSearch = () => {
      $("searchInput").value = item.dataset.query;
      runSearch();
      window.scrollTo({ top: 0, behavior: "smooth" });
    };

    item.addEventListener("click", repeatSearch);

    item.addEventListener("keydown", event => {
      if (event.key === "Enter") repeatSearch();
    });
  });
}

// Clear search history through backend DELETE API
async function clearHistory() {
  const confirmed = window.confirm(
    "Are you sure you want to delete your search history?"
  );

  if (!confirmed) return;

  $("historyStatus").textContent = "Clearing history...";

  try {
    const response = await fetch(
      `${API}/api/users/${USER_ID}/history`,
      { method: "DELETE" }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Could not clear history");
    }

    $("historyStatus").textContent =
      `History cleared. ${data.deleted_count} searches deleted.`;

    await loadHistory();

  } catch (error) {
    console.error("Clear history error:", error);
    $("historyStatus").textContent =
      "Could not clear history. Please try again.";
  }
}

// Render movie cards
function render() {
  const genre = $("genreFilter").value.toLowerCase();
  const min = Number($("ratingFilter").value);

  const rows = currentMovies.filter(movie => {
    const genreOK = !genre ||
      genresOf(movie).some(g => g.toLowerCase() === genre);

    const rating = ratingOf(movie);

    const ratingOK = min === 0 ||
      (rating !== null && Number.isFinite(rating) && rating >= min);

    return genreOK && ratingOK;
  });

  $("resultCount").textContent =
    `${rows.length} movie${rows.length === 1 ? "" : "s"}`;

  if (!rows.length) {
    $("results").innerHTML =
      '<div class="empty">No movies match your search and filters.</div>';
    return;
  }

  $("results").innerHTML = rows.map(movie => {
    const rating = ratingOf(movie);

    const tags = genresOf(movie)
      .map(g => `<span>${safe(g)}</span>`)
      .join("");

    return `
      <article class="card" data-movie-id="${safe(movie.id)}" tabindex="0" role="button">
        <h3>${safe(movie.title || "Untitled movie")}</h3>
        <div class="meta">
          ${safe(movie.year ?? movie.release_year ?? "Year unavailable")}
        </div>
        <div class="tags">
          ${tags || "<span>Genre unavailable</span>"}
        </div>
        <div class="rating-text ${rating == null ? "no-rating" : ""}">
          ${rating == null ? "Rating not available" : `★ ${safe(rating)} / 5`}
        </div>
        <div class="meta">Click to view details</div>
      </article>
    `;
  }).join("");
}

// Autocomplete suggestions
function showSuggestions(movies) {
  const titles = [...new Set(
    movies.map(m => typeof m === "string" ? m : m.title).filter(Boolean)
  )].slice(0, 6);

  $("suggestions").innerHTML =
    titles.map(title => `<li tabindex="0">${safe(title)}</li>`).join("");

  $("suggestions").hidden = !titles.length;

  $("suggestions").querySelectorAll("li").forEach(item => {
    const choose = () => {
      $("searchInput").value = item.textContent;
      $("suggestions").hidden = true;
      runSearch();
    };

    item.addEventListener("click", choose);

    item.addEventListener("keydown", event => {
      if (event.key === "Enter") choose();
    });
  });
}

// Search movies and retrieve ratings
async function runSearch() {
  const query = $("searchInput").value.trim();
  $("suggestions").hidden = true;

  if (!query) {
    currentMovies = [];
    render();
    $("apiStatus").textContent = "Enter a movie title to search.";
    return;
  }

  $("apiStatus").textContent = "Searching...";

  try {
    currentMovies = await search(query);

    const ratings = await Promise.all(
      currentMovies.map(async movie => {
        try {
          return await getMovieRatings(movie.id);
        } catch (error) {
          console.error("Ratings error:", error);
          return null;
        }
      })
    );

    currentMovies = currentMovies.map((movie, index) => ({
      ...movie,
      rating: ratings[index]?.average_rating ?? null
    }));

    render();

    $("apiStatus").textContent =
      "Connected to CineSearch backend.";

    // Save search and refresh history
    try {
      await saveSearch(query);
      await loadHistory();
    } catch (error) {
      console.error("Search logging error:", error);
      $("apiStatus").textContent =
        "Search completed, but history could not be saved.";
    }

  } catch (error) {
    console.error("Search error:", error);
    currentMovies = [];
    render();

    $("apiStatus").textContent =
      `Could not reach backend: ${error.message}. Start Flask first.`;
  }
}

// Movie details popup
async function openMovieDetails(movieId) {
  $("movieModal").hidden = false;
  $("movieDetails").innerHTML =
    '<p>Loading movie details...</p>';

  try {
    const [movie, ratings] = await Promise.all([
      getMovieDetails(movieId),
      getMovieRatings(movieId).catch(() => null)
    ]);

    $("movieDetails").innerHTML = `
      <p class="eyebrow">MOVIE DETAILS</p>
      <h2>${safe(movie.title)}</h2>
      <p>Release year: ${safe(movie.year ?? movie.release_year ?? "Unavailable")}</p>
      <p>Genres: ${genresOf(movie).map(safe).join(", ") || "Unavailable"}</p>
      <p class="modal-rating">
        ${ratings ? `★ ${safe(ratings.average_rating)} / 5` : "Rating not available"}
      </p>
      <p>Total ratings: ${safe(ratings?.total_ratings ?? 0)}</p>
    `;

  } catch (error) {
    console.error("Movie details error:", error);
    $("movieDetails").innerHTML =
      "<p>Unable to load movie details.</p>";
  }
}

$("results").addEventListener("click", event => {
  const card = event.target.closest(".card");
  if (card) openMovieDetails(card.dataset.movieId);
});

$("results").addEventListener("keydown", event => {
  if (event.key !== "Enter" && event.key !== " ") return;

  const card = event.target.closest(".card");

  if (card) {
    event.preventDefault();
    openMovieDetails(card.dataset.movieId);
  }
});

// Modal controls
$("closeModal").addEventListener("click", () => {
  $("movieModal").hidden = true;
});

$("movieModal").addEventListener("click", event => {
  if (event.target === $("movieModal")) {
    $("movieModal").hidden = true;
  }
});

document.addEventListener("keydown", event => {
  if (event.key === "Escape") $("movieModal").hidden = true;
});

// Search input autocomplete
$("searchInput").addEventListener("input", () => {
  clearTimeout(timer);

  const query = $("searchInput").value.trim();

  if (!query) {
    $("suggestions").hidden = true;
    currentMovies = [];
    render();
    return;
  }

  timer = setTimeout(async () => {
    try {
      showSuggestions(await autocomplete(query));
    } catch (error) {
      console.error("Autocomplete error:", error);
      $("suggestions").hidden = true;
    }
  }, 250);
});

$("searchButton").addEventListener("click", runSearch);

$("searchInput").addEventListener("keydown", event => {
  if (event.key === "Enter") runSearch();
  if (event.key === "Escape") $("suggestions").hidden = true;
});

document.addEventListener("click", event => {
  if (!event.target.closest(".search")) {
    $("suggestions").hidden = true;
  }
});

// Filters
$("genreFilter").addEventListener("change", render);

$("ratingFilter").addEventListener("input", () => {
  const value = Number($("ratingFilter").value);
  $("ratingValue").textContent = value === 0 ? "Any" : `${value}+`;
  render();
});

$("clearFilters").addEventListener("click", () => {
  $("genreFilter").value = "";
  $("ratingFilter").value = "0";
  $("ratingValue").textContent = "Any";
  render();
});

// History buttons
$("refreshHistory").addEventListener("click", loadHistory);
$("clearHistory").addEventListener("click", clearHistory);

// Initial setup
fetch(`${API}/api/health`)
  .then(response => {
    if (!response.ok) throw new Error("Backend unavailable");
    $("apiStatus").textContent = "Connected to CineSearch backend.";
  })
  .catch(() => {
    $("apiStatus").textContent =
      "Backend not detected. Start Flask at 127.0.0.1:5000.";
  });

loadHistory();

// ==========================================
// CineSearch Recommendation Integration
// ==========================================

async function fetchRecommendations(endpoint) {
  try {
    const response = await fetch(`${API}${endpoint}`);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Recommendation error:", error);
    return { recommendations: [] };
  }
}

function renderRecommendations(containerId, movies, emptyMessage) {
  const container = $(containerId);

  if (!container) return;

  if (!movies || movies.length === 0) {
    container.innerHTML = `
      <div class="empty">${safe(emptyMessage)}</div>
    `;
    return;
  }

  container.innerHTML = movies.map(movie => {
    const genres = movie.genres || movie.genre || [];
    const rating = Number(movie.average_rating);
    const year = movie.release_year || movie.year || "Year unknown";

    return `
      <article class="card recommendation-card"
        data-movie-id="${Number(movie.id)}"
        tabindex="0"
        role="button"
        aria-label="View ${safe(movie.title)}">

        <h3>${safe(movie.title)}</h3>

        <p class="meta">${safe(year)}</p>

        <div class="tags">
          ${genres.map(genre =>
            `<span>${safe(genre)}</span>`
          ).join("")}
        </div>

        <p class="rating-text">
          ★ ${Number.isFinite(rating) ? rating.toFixed(2) : "N/A"} / 5
        </p>

        <p class="meta">
          ${Number(movie.rating_count || 0).toLocaleString()} ratings
        </p>
      </article>
    `;
  }).join("");
}

async function loadPopularRecommendations() {
  const data = await fetchRecommendations(
    "/api/recommendations/popular?limit=6"
  );

  renderRecommendations(
    "popularRecommendations",
    data.recommendations,
    "No popular movies available."
  );
}

async function loadGenreRecommendations(genre = "Comedy") {
  const data = await fetchRecommendations(
    `/api/recommendations/genre/${encodeURIComponent(genre)}?limit=6`
  );

  renderRecommendations(
    "genreRecommendations",
    data.recommendations,
    "No genre recommendations available."
  );
}

async function loadPersonalizedRecommendations() {
  const endpoints = [
    {
      url: `/api/recommendations/user/${USER_ID}/genre-affinity?limit=5`,
      container: "genreAffinityRecommendations",
      message: "Rate some movies to get genre-based recommendations."
    },
    {
      url: `/api/recommendations/user/${USER_ID}/cooccurrence?limit=5`,
      container: "cooccurrenceRecommendations",
      message: "Recommendations based on similar users will appear after you rate movies."
    },
    {
      url: `/api/recommendations/user/${USER_ID}/jaccard?limit=5`,
      container: "jaccardRecommendations",
      message: "Rate some movies to discover similar movies using Jaccard similarity."
    }
  ];

  await Promise.all(endpoints.map(async item => {
    const data = await fetchRecommendations(item.url);

    renderRecommendations(
      item.container,
      data.recommendations,
      item.message
    );
  }));
}

// Open recommendation movie cards using existing movie details popup.
function setupRecommendationClicks() {
  ["popularRecommendations", "genreRecommendations",
   "genreAffinityRecommendations", "cooccurrenceRecommendations",
   "jaccardRecommendations"].forEach(containerId => {

    const container = $(containerId);
    if (!container) return;

    container.addEventListener("click", event => {
      const card = event.target.closest("[data-movie-id]");
      if (card) {
        openMovieDetails(Number(card.dataset.movieId));
      }
    });

    container.addEventListener("keydown", event => {
      if (event.key !== "Enter" && event.key !== " ") return;

      const card = event.target.closest("[data-movie-id]");
      if (card) {
        event.preventDefault();
        openMovieDetails(Number(card.dataset.movieId));
      }
    });
  });
}

// Load recommendation sections when the page starts.
async function initializeRecommendations() {
  setupRecommendationClicks();

  await Promise.all([
    loadPopularRecommendations(),
    loadGenreRecommendations("Comedy"),
    loadPersonalizedRecommendations()
  ]);
}

initializeRecommendations();
