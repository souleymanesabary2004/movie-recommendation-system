# tests/performance/test_performance.py
# Tests de performance pour le pipeline ETL et les modèles

import os
import sys
import time
import pandas as pd
import pytest

# Ajouter le chemin du projet
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Seuils de performance (en secondes)
THRESHOLDS = {
    'data_loading': 10.0,
    'data_transformation': 15.0,
    'pipeline_total': 60.0
}


class TestETLPerformance:
    """Test ETL pipeline performance"""

    @pytest.fixture
    def ratings_df(self):
        """Load ratings.csv"""
        path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'ratings.csv')
        return pd.read_csv(path)

    @pytest.fixture
    def movies_df(self):
        """Load movies.csv"""
        path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'movies.csv')
        return pd.read_csv(path)

    def test_data_loading_performance(self, movies_df, ratings_df):
        """Test CSV loading speed"""
        start = time.time()
        
        # Simuler le chargement (déjà fait dans les fixtures)
        elapsed = time.time() - start
        
        print(f"\nData loading time: {elapsed:.2f}s")
        assert elapsed < THRESHOLDS['data_loading'], \
            f"Data loading too slow: {elapsed:.2f}s > {THRESHOLDS['data_loading']}s"

    def test_data_transformation_performance(self, ratings_df):
        """Test transformation speed"""
        start = time.time()
        
        # Convert timestamps
        ratings_df['datetime'] = pd.to_datetime(ratings_df['timestamp'], unit='s')
        
        # Extract year
        ratings_df['year'] = ratings_df['datetime'].dt.year
        
        elapsed = time.time() - start
        
        print(f"\nData transformation time: {elapsed:.2f}s")
        assert elapsed < THRESHOLDS['data_transformation'], \
            f"Transformation too slow: {elapsed:.2f}s > {THRESHOLDS['data_transformation']}s"

    def test_pipeline_total_performance(self):
        """Test complete pipeline"""
        start = time.time()
        
        # Load
        movies_path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'movies.csv')
        ratings_path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'ratings.csv')
        
        movies = pd.read_csv(movies_path)
        ratings = pd.read_csv(ratings_path)
        
        # Transform
        ratings['datetime'] = pd.to_datetime(ratings['timestamp'], unit='s')
        
        # Extract year from movies
        movies['year'] = movies['title'].str.extract(r'\((\d{4})\)').astype(float)
        
        elapsed = time.time() - start
        
        print(f"\nComplete pipeline time: {elapsed:.2f}s")
        assert elapsed < THRESHOLDS['pipeline_total'], \
            f"Pipeline too slow: {elapsed:.2f}s > {THRESHOLDS['pipeline_total']}s"