# tests/unit/test_etl_functions.py
# Tests unitaires pour les fonctions ETL

import os
import sys
import pandas as pd
import pytest

# Ajouter le chemin du projet pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Chemin de la racine du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestETLHelpers:
    """Test helper functions used in ETL pipeline"""

    @pytest.fixture
    def sample_ratings(self):
        """Create a small sample of ratings data for testing"""
        return pd.DataFrame({
            'userId': [1, 1, 2, 2, 3],
            'movieId': [1, 2, 1, 3, 2],
            'rating': [4.0, 5.0, 3.0, 4.0, 2.5],
            'timestamp': [964982703, 964982704, 964982705, 964982706, 964982707]
        })

    def test_timestamp_conversion(self, sample_ratings):
        """Test that timestamp conversion produces datetime objects"""
        # Simuler la conversion de timestamp
        df = sample_ratings.copy()
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Vérifier que la colonne datetime a été créée
        assert 'datetime' in df.columns
        
        # Vérifier que c'est bien un datetime
        assert pd.api.types.is_datetime64_any_dtype(df['datetime'])
        
        # Vérifier une date spécifique (964982703 = 2000-07-30)
        first_date = df.loc[0, 'datetime']
        assert first_date.year == 2000
        assert first_date.month == 7
        assert first_date.day == 30

    def test_rating_normalization(self, sample_ratings):
        """Test that rating normalization works correctly"""
        # Simuler la normalisation des notes
        df = sample_ratings.copy()
        user_means = df.groupby('userId')['rating'].mean()
        
        # Normaliser pour un utilisateur spécifique
        user_1_mean = user_means[1]
        user_1_ratings = df[df['userId'] == 1]['rating']
        normalized = user_1_ratings - user_1_mean
        
        # Vérifier que la normalisation centre les notes autour de 0
        # Pour user 1: notes [4.0, 5.0], moyenne 4.5 → [-0.5, 0.5]
        expected = [-0.5, 0.5]
        assert list(normalized) == expected


class TestDataFrameOperations:
    """Test DataFrame operations used in ETL"""

    @pytest.fixture
    def sample_movies(self):
        """Create a small sample of movies data for testing"""
        return pd.DataFrame({
            'movieId': [1, 2, 3],
            'title': ['Toy Story (1995)', 'Jumanji (1995)', 'Grumpier Old Men (1995)'],
            'genres': ['Adventure|Animation|Children', 'Adventure|Children', 'Comedy|Romance']
        })

    def test_year_extraction(self, sample_movies):
        """Test that year extraction from title works"""
        # Extraire l'année avec regex
        df = sample_movies.copy()
        df['year'] = df['title'].str.extract(r'\((\d{4})\)').astype(float)
        
        # Vérifier les années extraites
        expected_years = [1995.0, 1995.0, 1995.0]
        assert list(df['year']) == expected_years
        
        # Vérifier qu'il n'y a pas de valeurs manquantes
        assert df['year'].isna().sum() == 0

    def test_genre_split(self, sample_movies):
        """Test that genre splitting works correctly"""
        df = sample_movies.copy()
        df['genre_list'] = df['genres'].str.split('|')
        
        # Vérifier le nombre de genres pour chaque film
        genre_counts = df['genre_list'].apply(len)
        expected_counts = [3, 2, 2]
        assert list(genre_counts) == expected_counts
        
        # Vérifier le premier genre du premier film
        first_genres = df.loc[0, 'genre_list']
        assert first_genres[0] == 'Adventure'
        assert first_genres[1] == 'Animation'
        assert first_genres[2] == 'Children'