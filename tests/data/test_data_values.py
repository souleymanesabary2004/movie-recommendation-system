# tests/data/test_data_values.py
# Test des valeurs : vérifier que les données sont cohérentes

import os
import pandas as pd
import pytest

# Chemin de la racine du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDataValues:
    """Verify that data values are consistent and valid"""

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


class TestRatingsValues(TestDataValues):
    """Test ratings.csv value consistency"""

    def test_rating_range(self, ratings_df):
        """Check that all ratings are between 0.5 and 5.0"""
        min_rating = ratings_df['rating'].min()
        max_rating = ratings_df['rating'].max()
        assert min_rating >= 0.5, f"Rating too low: {min_rating}"
        assert max_rating <= 5.0, f"Rating too high: {max_rating}"

    def test_rating_increments(self, ratings_df):
        """Check that ratings are in 0.5 increments"""
        valid_ratings = {0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0}
        unique_ratings = set(ratings_df['rating'].unique())
        invalid = unique_ratings - valid_ratings
        assert len(invalid) == 0, f"Invalid rating values: {invalid}"

    def test_no_negative_values(self, ratings_df):
        """Check that there are no negative values in numeric columns"""
        numeric_cols = ['userId', 'movieId', 'rating', 'timestamp']
        for col in numeric_cols:
            min_val = ratings_df[col].min()
            assert min_val >= 0, f"Negative value in {col}: {min_val}"


class TestMoviesValues(TestDataValues):
    """Test movies.csv value consistency"""

    def test_movieId_positive(self, movies_df):
        """Check that all movieId are positive"""
        min_id = movies_df['movieId'].min()
        assert min_id >= 1, f"Movie ID too low: {min_id}"

    def test_no_empty_titles(self, movies_df):
        """Check that there are no empty titles"""
        empty_titles = movies_df[movies_df['title'].isna() | (movies_df['title'] == '')]
        assert len(empty_titles) == 0, f"Empty titles found: {len(empty_titles)}"

    def test_genres_format(self, movies_df):
        """Check that genres are properly formatted (no empty strings)"""
        # Les genres peuvent être "(no genres listed)" - c'est valide
        empty_genres = movies_df[movies_df['genres'].isna() | (movies_df['genres'] == '')]
        assert len(empty_genres) == 0, f"Empty genres found: {len(empty_genres)}"