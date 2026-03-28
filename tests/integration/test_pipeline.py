# tests/integration/test_pipeline.py
# Tests d'intégration : vérifier que le pipeline ETL complet fonctionne

import os
import sys
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


class TestETLPipeline:
    """Test the complete ETL pipeline"""

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

    def test_data_extraction(self, movies_df, ratings_df):
        """Test that data extraction loads correct number of rows"""
        # Vérifier le nombre de films
        assert len(movies_df) == 9742, f"Expected 9742 movies, got {len(movies_df)}"
        
        # Vérifier le nombre de notes
        assert len(ratings_df) == 100836, f"Expected 100836 ratings, got {len(ratings_df)}"
        
        # Vérifier les colonnes
        assert 'movieId' in movies_df.columns
        assert 'userId' in ratings_df.columns

    def test_data_transformation(self, ratings_df):
        """Test data transformation functions"""
        # Test conversion timestamp en datetime
        df = ratings_df.copy()
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Vérifier que la conversion fonctionne
        assert 'datetime' in df.columns
        assert pd.api.types.is_datetime64_any_dtype(df['datetime'])
        
        # Vérifier une date spécifique
        first_date = df.loc[0, 'datetime']
        assert first_date.year >= 1995
        assert first_date.year <= 2005

    def test_statistics_calculation(self, ratings_df, movies_df):
        """Test that statistics are calculated correctly"""
        # Calculer les stats utilisateurs
        user_stats = ratings_df.groupby('userId').agg({
            'rating': ['count', 'mean', 'std', 'min', 'max']
        }).round(2)
        
        user_stats.columns = ['rating_count', 'avg_rating', 'std_rating', 'min_rating', 'max_rating']
        
        # Vérifier que les stats sont valides
        assert len(user_stats) > 0
        assert user_stats['avg_rating'].min() >= 0.5
        assert user_stats['avg_rating'].max() <= 5.0
        
        # Calculer les stats films
        movie_stats = ratings_df.groupby('movieId').agg({
            'rating': ['count', 'mean', 'std', 'min', 'max']
        }).round(2)
        
        movie_stats.columns = ['rating_count', 'avg_rating', 'std_rating', 'min_rating', 'max_rating']
        
        # Vérifier que les stats films sont valides
        assert len(movie_stats) > 0
        assert movie_stats['rating_count'].max() > 0

    def test_database_insertion_consistency(self, db_config):
        """Test that database data matches CSV data"""
        # Charger les données CSV
        movies_csv = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'raw', 'movies.csv'))
        ratings_csv = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'raw', 'ratings.csv'))
        
        # Se connecter à la base de données
        conn = mysql.connector.connect(**db_config)
        
        # Vérifier le nombre de films
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM movies")
        db_movies_count = cursor.fetchone()[0]
        assert db_movies_count == len(movies_csv), f"Movies count mismatch: DB={db_movies_count}, CSV={len(movies_csv)}"
        
        # Vérifier le nombre de notes
        cursor.execute("SELECT COUNT(*) FROM ratings")
        db_ratings_count = cursor.fetchone()[0]
        assert db_ratings_count == len(ratings_csv), f"Ratings count mismatch: DB={db_ratings_count}, CSV={len(ratings_csv)}"
        
        # Vérifier quelques films spécifiques
        cursor.execute("SELECT movieId, title FROM movies WHERE movieId=1")
        movie_1 = cursor.fetchone()
        assert movie_1 is not None
        assert "Toy Story" in movie_1[1]
        
        cursor.close()
        conn.close()

    def test_etl_workflow(self, movies_df, ratings_df, db_config):
        """Test the complete ETL workflow with temporary tables"""
        # Simuler le workflow ETL complet
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Créer une table temporaire pour les tests
        cursor.execute("""
            CREATE TEMPORARY TABLE IF NOT EXISTS test_stats (
                userId INT,
                rating_count INT,
                avg_rating FLOAT,
                std_rating FLOAT,
                min_rating FLOAT,
                max_rating FLOAT
            )
        """)
        
        # Calculer les stats
        user_stats = ratings_df.groupby('userId').agg({
            'rating': ['count', 'mean', 'std', 'min', 'max']
        }).round(2)
        
        user_stats.columns = ['rating_count', 'avg_rating', 'std_rating', 'min_rating', 'max_rating']
        user_stats = user_stats.reset_index()
        
        # Insérer dans la table temporaire
        for _, row in user_stats.iterrows():
            cursor.execute("""
                INSERT INTO test_stats (userId, rating_count, avg_rating, std_rating, min_rating, max_rating)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['userId'], row['rating_count'], row['avg_rating'], 
                  row['std_rating'], row['min_rating'], row['max_rating']))
        
        conn.commit()
        
        # Vérifier que les données ont été insérées
        cursor.execute("SELECT COUNT(*) FROM test_stats")
        count = cursor.fetchone()[0]
        assert count == len(user_stats)
        
        # Vérifier un utilisateur spécifique
        cursor.execute("SELECT * FROM test_stats WHERE userId=1")
        user_1 = cursor.fetchone()
        assert user_1 is not None
        assert user_1[1] > 0  # rating_count > 0
        
        cursor.close()
        conn.close()

    def test_data_quality(self, db_config):
        """Test data quality in database"""
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Vérifier qu'il n'y a pas de notes en dehors de 0.5-5.0
        cursor.execute("""
            SELECT COUNT(*) FROM ratings 
            WHERE rating < 0.5 OR rating > 5.0
        """)
        invalid_ratings = cursor.fetchone()[0]
        assert invalid_ratings == 0, f"Found {invalid_ratings} invalid ratings"
        
        # Vérifier que tous les films ont un titre non vide
        cursor.execute("""
            SELECT COUNT(*) FROM movies 
            WHERE title IS NULL OR title = ''
        """)
        empty_titles = cursor.fetchone()[0]
        assert empty_titles == 0, f"Found {empty_titles} movies with empty titles"
        
        # Vérifier l'intégrité référentielle
        cursor.execute("""
            SELECT COUNT(*) FROM ratings r
            LEFT JOIN movies m ON r.movieId = m.movieId
            WHERE m.movieId IS NULL
        """)
        orphaned_ratings = cursor.fetchone()[0]
        assert orphaned_ratings == 0, f"Found {orphaned_ratings} ratings without corresponding movies"
        
        cursor.close()
        conn.close()