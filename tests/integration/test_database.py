# tests/integration/test_database.py
# Tests d'intégration : vérifier la connexion à la base de données

import os
import sys
import pytest
import mysql.connector
from mysql.connector import errorcode

# Ajouter le chemin du projet pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Chemin de la racine du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDatabaseConnection:
    """Test database connection and operations"""

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

    def test_connection(self, db_config):
        """Test that we can connect to MySQL"""
        try:
            conn = mysql.connector.connect(**db_config)
            assert conn.is_connected()
            conn.close()
        except mysql.connector.Error as err:
            pytest.fail(f"Connection failed: {err}")

    def test_database_exists(self, db_config):
        """Test that the database exists"""
        # Se connecter sans base spécifique
        config_no_db = {k: v for k, v in db_config.items() if k != 'database'}
        conn = mysql.connector.connect(**config_no_db)
        cursor = conn.cursor()
        
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        assert db_config['database'] in databases, f"Database {db_config['database']} not found"
        
        cursor.close()
        conn.close()

    def test_tables_exist(self, db_config):
        """Test that required tables exist"""
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        expected_tables = ['movies', 'ratings']
        for table in expected_tables:
            assert table in tables, f"Table {table} not found"
        
        cursor.close()
        conn.close()

    def test_movies_table_schema(self, db_config):
        """Test that movies table has correct columns"""
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("DESCRIBE movies")
        columns = {row[0]: row[1] for row in cursor.fetchall()}
        
        expected_columns = {
            'movieId': ['int', 'bigint'],
            'title': ['varchar', 'text', 'char'],
            'genres': ['varchar', 'text', 'char']
        }
        
        for col, expected_types in expected_columns.items():
            assert col in columns, f"Column {col} missing"
            col_type = columns[col].lower()
            assert any(expected_type in col_type for expected_type in expected_types), \
                f"Column {col} wrong type: {col_type}"
        
        cursor.close()
        conn.close()

    def test_ratings_table_schema(self, db_config):
        """Test that ratings table has correct columns"""
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("DESCRIBE ratings")
        columns = {row[0]: row[1] for row in cursor.fetchall()}
        
        expected_columns = {
            'userId': ['int', 'bigint'],
            'movieId': ['int', 'bigint'],
            'rating': ['float', 'double', 'decimal'],
            'timestamp': ['int', 'bigint']
        }
        
        for col, expected_types in expected_columns.items():
            assert col in columns, f"Column {col} missing"
            col_type = columns[col].lower()
            assert any(expected_type in col_type for expected_type in expected_types), \
                f"Column {col} wrong type: {col_type}"
        
        cursor.close()
        conn.close()

    def test_movies_count(self, db_config):
        """Test that movies table has data"""
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM movies")
        count = cursor.fetchone()[0]
        
        assert count > 0, "Movies table is empty"
        assert count == 9742, f"Expected 9742 movies, got {count}"
        
        cursor.close()
        conn.close()

    def test_ratings_count(self, db_config):
        """Test that ratings table has data"""
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM ratings")
        count = cursor.fetchone()[0]
        
        assert count > 0, "Ratings table is empty"
        assert count == 100836, f"Expected 100836 ratings, got {count}"
        
        cursor.close()
        conn.close()