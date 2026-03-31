# tests/data/test_data_schema.py
# Test des schémas : vérifier que les colonnes sont correctes

import os
import pandas as pd
import pytest

# Chemin de la racine du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Vérifier si les données existent
DATA_AVAILABLE = os.path.exists(os.path.join(PROJECT_ROOT, 'data', 'raw', 'movies.csv'))

@pytest.mark.skipif(not DATA_AVAILABLE, reason="Data files not available in CI")
class TestDataSchema:
    """Verify that data files have the correct columns"""

    @pytest.fixture
    def movies_df(self):
        """Load movies.csv for testing"""
        path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'movies.csv')
        return pd.read_csv(path)

    @pytest.fixture
    def ratings_df(self):
        """Load ratings.csv for testing"""
        path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'ratings.csv')
        return pd.read_csv(path)

    @pytest.fixture
    def user_stats_df(self):
        """Load user_stats.csv for testing"""
        path = os.path.join(PROJECT_ROOT, 'user_stats.csv')
        return pd.read_csv(path)

    @pytest.fixture
    def movie_stats_df(self):
        """Load movie_stats.csv for testing"""
        path = os.path.join(PROJECT_ROOT, 'movie_stats.csv')
        return pd.read_csv(path)


class TestMoviesSchema(TestDataSchema):
    """Test movies.csv schema"""

    def test_columns_exist(self, movies_df):
        """Check that all expected columns are present"""
        expected = {'movieId', 'title', 'genres'}
        actual = set(movies_df.columns)
        assert expected.issubset(actual), f"Missing columns: {expected - actual}"

    def test_movieId_is_integer(self, movies_df):
        """Check that movieId is integer"""
        assert movies_df['movieId'].dtype in ['int64', 'int32'], "movieId should be integer"

    def test_title_is_string(self, movies_df):
        """Check that title is string"""
        assert movies_df['title'].dtype == 'object', "title should be string"

    def test_genres_is_string(self, movies_df):
        """Check that genres is string"""
        assert movies_df['genres'].dtype == 'object', "genres should be string"


class TestRatingsSchema(TestDataSchema):
    """Test ratings.csv schema"""

    def test_columns_exist(self, ratings_df):
        """Check that all expected columns are present"""
        expected = {'userId', 'movieId', 'rating', 'timestamp'}
        actual = set(ratings_df.columns)
        assert expected.issubset(actual), f"Missing columns: {expected - actual}"

    def test_userId_is_integer(self, ratings_df):
        """Check that userId is integer"""
        assert ratings_df['userId'].dtype in ['int64', 'int32'], "userId should be integer"

    def test_movieId_is_integer(self, ratings_df):
        """Check that movieId is integer"""
        assert ratings_df['movieId'].dtype in ['int64', 'int32'], "movieId should be integer"

    def test_rating_is_float(self, ratings_df):
        """Check that rating is float"""
        assert ratings_df['rating'].dtype in ['float64', 'float32'], "rating should be float"

    def test_timestamp_is_integer(self, ratings_df):
        """Check that timestamp is integer"""
        assert ratings_df['timestamp'].dtype in ['int64', 'int32'], "timestamp should be integer"


class TestUserStatsSchema(TestDataSchema):
    """Test user_stats.csv schema"""

    def test_columns_exist(self, user_stats_df):
        """Check that all expected columns are present"""
        expected = {'userId', 'rating_count', 'avg_rating', 'std_rating', 'min_rating', 'max_rating'}
        actual = set(user_stats_df.columns)
        assert expected.issubset(actual), f"Missing columns: {expected - actual}"


class TestMovieStatsSchema(TestDataSchema):
    """Test movie_stats.csv schema"""

    def test_columns_exist(self, movie_stats_df):
        """Check that all expected columns are present"""
        expected = {'movieId', 'rating_count', 'avg_rating', 'std_rating', 'min_rating', 'max_rating'}
        actual = set(movie_stats_df.columns)
        assert expected.issubset(actual), f"Missing columns: {expected - actual}"