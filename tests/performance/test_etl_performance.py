# tests/performance/test_etl_performance.py
# Tests de performance : vérifier que l'ETL s'exécute dans des temps raisonnables

import os
import sys
import time
import pandas as pd
import pytest
import mysql.connector
from datetime import datetime

# Ajouter le chemin du projet pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Chemin de la racine du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Seuils de performance (en secondes)
PERFORMANCE_THRESHOLDS = {
    'data_loading': 5.0,      # Chargement des données CSV
    'data_transformation': 3.0, # Transformation des données
    'stats_calculation': 2.0,   # Calcul des statistiques
    'database_write': 10.0,     # Écriture en base de données
    'pipeline_total': 20.0      # Pipeline complet
}


class TestETLPerformance:
    """Test ETL pipeline performance"""

    @pytest.fixture
    def db_config(self):
        """Return database configuration from environment"""
        return {
            'user': 'root',
            'password': os.getenv('MYSQL_ROOT_PASSWORD'),
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', 2004)),
            'database': os.getenv('MYSQL_DATABASE', 'movie_recommendation')
        }

    def test_data_loading_performance(self):
        """Test that loading CSV files meets performance threshold"""
        start_time = time.time()
        
        # Charger les fichiers CSV
        movies_path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'movies.csv')
        ratings_path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'ratings.csv')
        
        movies_df = pd.read_csv(movies_path)
        ratings_df = pd.read_csv(ratings_path)
        
        elapsed_time = time.time() - start_time
        print(f"\nData loading time: {elapsed_time:.2f} seconds")
        
        assert elapsed_time < PERFORMANCE_THRESHOLDS['data_loading'], \
            f"Data loading too slow: {elapsed_time:.2f}s > {PERFORMANCE_THRESHOLDS['data_loading']}s"
        
        # Vérifier que les données sont chargées
        assert len(movies_df) == 9742
        assert len(ratings_df) == 100836

    def test_data_transformation_performance(self):
        """Test that data transformation meets performance threshold"""
        # Charger les données
        ratings_path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'ratings.csv')
        ratings_df = pd.read_csv(ratings_path)
        
        start_time = time.time()
        
        # Simuler les transformations
        # 1. Conversion timestamp en datetime
        ratings_df['datetime'] = pd.to_datetime(ratings_df['timestamp'], unit='s')
        
        # 2. Extraction de l'année (simulée)
        ratings_df['year'] = ratings_df['datetime'].dt.year
        
        # 3. Normalisation des notes (simulée)
        user_means = ratings_df.groupby('userId')['rating'].mean()
        ratings_df['normalized_rating'] = ratings_df.apply(
            lambda x: x['rating'] - user_means[x['userId']], axis=1
        )
        
        elapsed_time = time.time() - start_time
        print(f"\nData transformation time: {elapsed_time:.2f} seconds")
        
        assert elapsed_time < PERFORMANCE_THRESHOLDS['data_transformation'], \
            f"Data transformation too slow: {elapsed_time:.2f}s > {PERFORMANCE_THRESHOLDS['data_transformation']}s"

    def test_statistics_calculation_performance(self):
        """Test that statistics calculation meets performance threshold"""
        # Charger les données
        ratings_path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'ratings.csv')
        ratings_df = pd.read_csv(ratings_path)
        
        start_time = time.time()
        
        # Calculer les statistiques utilisateurs
        user_stats = ratings_df.groupby('userId').agg({
            'rating': ['count', 'mean', 'std', 'min', 'max']
        }).round(2)
        
        # Calculer les statistiques films
        movie_stats = ratings_df.groupby('movieId').agg({
            'rating': ['count', 'mean', 'std', 'min', 'max']
        }).round(2)
        
        elapsed_time = time.time() - start_time
        print(f"\nStatistics calculation time: {elapsed_time:.2f} seconds")
        
        assert elapsed_time < PERFORMANCE_THRESHOLDS['stats_calculation'], \
            f"Statistics calculation too slow: {elapsed_time:.2f}s > {PERFORMANCE_THRESHOLDS['stats_calculation']}s"
        
        # Vérifier les résultats
        assert len(user_stats) > 0
        assert len(movie_stats) > 0

    def test_database_write_performance(self, db_config):
        """Test that database write operations meet performance threshold"""
        # Charger les données
        ratings_path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'ratings.csv')
        ratings_df = pd.read_csv(ratings_path)
        
        # Calculer les stats pour écrire
        user_stats = ratings_df.groupby('userId').agg({
            'rating': ['count', 'mean', 'std', 'min', 'max']
        }).round(2)
        user_stats.columns = ['rating_count', 'avg_rating', 'std_rating', 'min_rating', 'max_rating']
        user_stats = user_stats.reset_index()
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Créer une table temporaire pour le test
        cursor.execute("""
            CREATE TEMPORARY TABLE IF NOT EXISTS perf_test_stats (
                userId INT,
                rating_count INT,
                avg_rating FLOAT,
                std_rating FLOAT,
                min_rating FLOAT,
                max_rating FLOAT
            )
        """)
        
        start_time = time.time()
        
        # Insérer les données
        for _, row in user_stats.iterrows():
            cursor.execute("""
                INSERT INTO perf_test_stats (userId, rating_count, avg_rating, std_rating, min_rating, max_rating)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['userId'], row['rating_count'], row['avg_rating'], 
                  row['std_rating'], row['min_rating'], row['max_rating']))
        
        conn.commit()
        
        elapsed_time = time.time() - start_time
        print(f"\nDatabase write time: {elapsed_time:.2f} seconds")
        
        assert elapsed_time < PERFORMANCE_THRESHOLDS['database_write'], \
            f"Database write too slow: {elapsed_time:.2f}s > {PERFORMANCE_THRESHOLDS['database_write']}s"
        
        cursor.close()
        conn.close()

    def test_pipeline_total_performance(self):
        """Test that complete pipeline meets total performance threshold"""
        start_time = time.time()
        
        # Étape 1: Chargement
        movies_path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'movies.csv')
        ratings_path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'ratings.csv')
        
        movies_df = pd.read_csv(movies_path)
        ratings_df = pd.read_csv(ratings_path)
        
        # Étape 2: Transformations
        ratings_df['datetime'] = pd.to_datetime(ratings_df['timestamp'], unit='s')
        
        # Étape 3: Statistiques
        user_stats = ratings_df.groupby('userId').agg({
            'rating': ['count', 'mean', 'std', 'min', 'max']
        }).round(2)
        
        movie_stats = ratings_df.groupby('movieId').agg({
            'rating': ['count', 'mean', 'std', 'min', 'max']
        }).round(2)
        
        # Étape 4: Sauvegarde locale
        user_stats.to_csv('user_stats_test.csv', index=False)
        movie_stats.to_csv('movie_stats_test.csv', index=False)
        
        elapsed_time = time.time() - start_time
        print(f"\nComplete pipeline time: {elapsed_time:.2f} seconds")
        
        assert elapsed_time < PERFORMANCE_THRESHOLDS['pipeline_total'], \
            f"Complete pipeline too slow: {elapsed_time:.2f}s > {PERFORMANCE_THRESHOLDS['pipeline_total']}s"
        
        # Nettoyer les fichiers de test
        if os.path.exists('user_stats_test.csv'):
            os.remove('user_stats_test.csv')
        if os.path.exists('movie_stats_test.csv'):
            os.remove('movie_stats_test.csv')