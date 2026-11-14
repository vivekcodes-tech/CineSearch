
-- CineSearch - Student 2
-- Database Index Optimization
-- Based on the controlled indexing experiment

-- 1. User rating history lookup
CREATE INDEX IF NOT EXISTS idx_rating_user_id
ON rating(user_id);

-- 2. Movie ratings lookup
CREATE INDEX IF NOT EXISTS idx_rating_movie_id
ON rating(movie_id);

-- 3. Composite user-movie lookup
CREATE INDEX IF NOT EXISTS idx_rating_user_movie
ON rating(user_id, movie_id);

-- 4. Movie genre filtering
CREATE INDEX IF NOT EXISTS idx_movie_genre_genre
ON movie_genre(genre_id);

-- 5. Tag movie lookup
CREATE INDEX IF NOT EXISTS idx_tag_event_movie_id
ON tag_event(movie_id);


-- CineSearch - Student 2
-- Database Index Optimization
-- Based on the controlled indexing experiment

-- 1. User rating history lookup
CREATE INDEX IF NOT EXISTS idx_rating_user_id
ON rating(user_id);

-- 2. Movie ratings lookup
CREATE INDEX IF NOT EXISTS idx_rating_movie_id
ON rating(movie_id);

-- 3. Composite user-movie lookup
CREATE INDEX IF NOT EXISTS idx_rating_user_movie
ON rating(user_id, movie_id);

-- 4. Movie genre filtering
CREATE INDEX IF NOT EXISTS idx_movie_genre_genre
ON movie_genre(genre_id);

-- 5. Tag movie lookup
CREATE INDEX IF NOT EXISTS idx_tag_event_movie_id
ON tag_event(movie_id);
