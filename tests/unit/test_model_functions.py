# tests/unit/test_model_functions.py
# Tests unitaires pour les fonctions des modèles ML

import os
import sys
import numpy as np
import pandas as pd
import pytest

# Ajouter le chemin du projet pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Chemin de la racine du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestModelHelpers:
    """Test helper functions used in ML models"""

    @pytest.fixture
    def sample_ratings_matrix(self):
        """Create a small sample user-movie matrix for testing"""
        # 3 users, 4 movies
        data = {
            1: [4.0, 5.0, 0, 3.0],      # User 1
            2: [5.0, 4.0, 3.0, 0],      # User 2
            3: [0, 3.0, 4.0, 5.0],      # User 3
        }
        df = pd.DataFrame(data, index=[1, 2, 3, 4]).T
        return df

    def test_normalization(self, sample_ratings_matrix):
        """Test that user-wise normalization works"""
        matrix = sample_ratings_matrix.copy()
        
        # Remplacer les 0 par NaN (simuler les notes manquantes)
        matrix = matrix.replace(0, np.nan)
        
        # Calculer la moyenne par utilisateur
        user_means = matrix.mean(axis=1)
        
        # Normaliser
        normalized = matrix.sub(user_means, axis=0)
        
        # Vérifier que la moyenne après normalisation est proche de 0
        # Pour User 1: notes [4.0, 5.0, 3.0], moyenne 4.0
        # Normalisées: [0.0, 1.0, -1.0] → moyenne = 0.0
        user_1_norm = normalized.loc[1].dropna()
        assert abs(user_1_norm.mean()) < 0.01
        
        # Vérifier que les valeurs sont centrées
        assert user_1_norm.values[0] == 0.0  # 4.0 - 4.0 = 0
        assert user_1_norm.values[1] == 1.0  # 5.0 - 4.0 = 1

    def test_cosine_similarity(self):
        """Test that cosine similarity calculation works"""
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Deux vecteurs identiques
        v1 = np.array([1, 0, 0])
        v2 = np.array([1, 0, 0])
        sim = cosine_similarity([v1], [v2])[0][0]
        assert sim == pytest.approx(1.0, abs=1e-6)
        
        # Deux vecteurs orthogonaux
        v1 = np.array([1, 0, 0])
        v2 = np.array([0, 1, 0])
        sim = cosine_similarity([v1], [v2])[0][0]
        assert sim == pytest.approx(0.0, abs=1e-6)
        
        # Deux vecteurs opposés
        v1 = np.array([1, 1])
        v2 = np.array([-1, -1])
        sim = cosine_similarity([v1], [v2])[0][0]
        assert sim == pytest.approx(-1.0, abs=1e-6)


class TestRecommendationLogic:
    """Test the logic behind recommendations"""

    def test_hit_rate_calculation(self):
        """Test that hit rate calculation works correctly"""
        # Simuler des recommandations
        recommended = [1, 2, 3, 4, 5]
        liked = [1, 3, 6, 7, 8]
        
        # Compter les hits (films recommandés qui sont aimés)
        hits = len(set(recommended) & set(liked))
        
        # Hit Rate = hits / nombre de recommandations
        hit_rate = hits / len(recommended)
        
        assert hits == 2  # Films 1 et 3
        assert hit_rate == 0.4  # 2/5 = 0.4

    def test_precision_recall(self):
        """Test precision and recall calculation"""
        # Simuler des recommandations
        recommended = [1, 2, 3, 4, 5]  # 5 films recommandés
        liked = [1, 3, 6, 7, 8]        # 5 films aimés en tout
        
        # Précision = films aimés dans recommandations / total recommandations
        hits = len(set(recommended) & set(liked))  # = 2
        precision = hits / len(recommended)  # 2/5 = 0.4
        
        # Rappel = films aimés dans recommandations / total films aimés
        recall = hits / len(liked)  # 2/5 = 0.4
        
        assert precision == 0.4
        assert recall == 0.4


class TestModelLoading:
    """Test that model loading works correctly"""

    def test_model_file_exists(self):
        """Check that model files exist"""
        models = ['svd_model.pkl', 'knn_model.pkl', 'content_model.pkl']
        for model_name in models:
            path = os.path.join(PROJECT_ROOT, model_name)
            if os.path.exists(path):
                assert os.path.getsize(path) > 0
            else:
                # Si le fichier n'existe pas, on le note mais on ne fait pas échouer le test
                # car les modèles peuvent ne pas être encore entraînés
                pytest.skip(f"Model not found: {model_name}")