# tests/data/test_data_integrity.py
# Test d'intégrité des données : vérifier que les fichiers existent et ne sont pas vides

import os
import pytest

# Chemin de la racine du projet (remonte de 3 dossiers depuis ce fichier)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDataIntegrity:
    """Verify that all data files exist and are not empty"""

    @pytest.fixture
    def file_paths(self):
        """Return the list of files to test"""
        return {
            'movies.csv': os.path.join(PROJECT_ROOT, 'data', 'raw', 'movies.csv'),
            'ratings.csv': os.path.join(PROJECT_ROOT, 'data', 'raw', 'ratings.csv'),
            'user_stats.csv': os.path.join(PROJECT_ROOT, 'user_stats.csv'),
            'movie_stats.csv': os.path.join(PROJECT_ROOT, 'movie_stats.csv'),
        }

    def test_files_exist(self, file_paths):
        """Check that all files exist"""
        for name, path in file_paths.items():
            assert os.path.exists(path), f"Missing file: {name} ({path})"

    def test_files_not_empty(self, file_paths):
        """Check that all files are not empty"""
        for name, path in file_paths.items():
            assert os.path.getsize(path) > 0, f"Empty file: {name}"