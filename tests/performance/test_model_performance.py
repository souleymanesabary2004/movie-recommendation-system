# tests/performance/test_model_performance.py
# Tests de performance : vérifier que les modèles ML s'entraînent et prédisent dans des temps raisonnables

import os
import sys
import time
import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors

# Ajouter le chemin du projet pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Chemin de la racine du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Seuils de performance (en secondes)
PERFORMANCE_THRESHOLDS = {
    'svd_training': 30.0,      # Entraînement SVD
    'knn_training': 10.0,      # Entraînement KNN
    'prediction_per_user': 0.1, # Prédiction par utilisateur
    'similarity_calculation': 5.0, # Calcul de similarité
    'content_training': 20.0   # Entraînement modèle content-based
}


class TestModelPerformance:
    """Test ML model performance"""

    @pytest.fixture
    def ratings_df(self):
        """Load ratings.csv for testing"""
        path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'ratings.csv')
        return pd.read_csv(path)

    @pytest.fixture
    def movies_df(self):
        """Load movies.csv for testing"""
        path = os.path.join(PROJECT_ROOT, 'data', 'raw', 'movies.csv')
        return pd.read_csv(path)

    @pytest.fixture
    def user_movie_matrix(self, ratings_df):
        """Create user-movie matrix for testing"""
        # Prendre un échantillon pour les tests de performance
        sample_users = ratings_df['userId'].nunique()
        sample_movies = ratings_df['movieId'].nunique()
        
        print(f"\nMatrix size: {sample_users} users x {sample_movies} movies")
        
        # Créer la matrice user-movie
        matrix = ratings_df.pivot_table(
            index='userId', 
            columns='movieId', 
            values='rating'
        ).fillna(0)
        
        return matrix

    def test_svd_training_performance(self, user_movie_matrix):
        """Test that SVD training meets performance threshold"""
        start_time = time.time()
        
        # Réduire la taille pour le test de performance
        matrix_sample = user_movie_matrix.iloc[:500, :500]
        
        # Entraîner SVD
        svd = TruncatedSVD(n_components=50, random_state=42)
        svd.fit(matrix_sample)
        
        elapsed_time = time.time() - start_time
        print(f"\nSVD training time: {elapsed_time:.2f} seconds")
        
        assert elapsed_time < PERFORMANCE_THRESHOLDS['svd_training'], \
            f"SVD training too slow: {elapsed_time:.2f}s > {PERFORMANCE_THRESHOLDS['svd_training']}s"
        
        # Vérifier que le modèle a appris
        assert svd.components_.shape[0] == 50

    def test_knn_training_performance(self, user_movie_matrix):
        """Test that KNN training meets performance threshold"""
        start_time = time.time()
        
        # Réduire la taille pour le test de performance
        matrix_sample = user_movie_matrix.iloc[:500, :500]
        
        # Entraîner KNN
        knn = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute')
        knn.fit(matrix_sample)
        
        elapsed_time = time.time() - start_time
        print(f"\nKNN training time: {elapsed_time:.2f} seconds")
        
        assert elapsed_time < PERFORMANCE_THRESHOLDS['knn_training'], \
            f"KNN training too slow: {elapsed_time:.2f}s > {PERFORMANCE_THRESHOLDS['knn_training']}s"
        
        # Vérifier que le modèle a appris
        assert knn.n_samples_fit_ == len(matrix_sample)

    def test_prediction_performance(self, user_movie_matrix):
        """Test that prediction for a single user meets performance threshold"""
        # Prendre un échantillon
        matrix_sample = user_movie_matrix.iloc[:200, :200]
        
        # Entraîner KNN rapidement
        knn = NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='brute')
        knn.fit(matrix_sample)
        
        start_time = time.time()
        
        # Prédire pour le premier utilisateur
        user_vector = matrix_sample.iloc[0:1]
        distances, indices = knn.kneighbors(user_vector)
        
        elapsed_time = time.time() - start_time
        print(f"\nPrediction time per user: {elapsed_time:.4f} seconds")
        
        assert elapsed_time < PERFORMANCE_THRESHOLDS['prediction_per_user'], \
            f"Prediction too slow: {elapsed_time:.4f}s > {PERFORMANCE_THRESHOLDS['prediction_per_user']}s"

    def test_cosine_similarity_performance(self, movies_df):
        """Test that cosine similarity calculation meets performance threshold"""
        # Créer une matrice de features simplifiée
        n_movies = min(1000, len(movies_df))
        feature_matrix = np.random.rand(n_movies, 50)  # 50 features pour 1000 films
        
        start_time = time.time()
        
        # Calculer la similarité cosinus
        similarity = cosine_similarity(feature_matrix)
        
        elapsed_time = time.time() - start_time
        print(f"\nCosine similarity calculation time: {elapsed_time:.2f} seconds")
        
        assert elapsed_time < PERFORMANCE_THRESHOLDS['similarity_calculation'], \
            f"Similarity calculation too slow: {elapsed_time:.2f}s > {PERFORMANCE_THRESHOLDS['similarity_calculation']}s"
        
        # Vérifier la forme de la matrice
        assert similarity.shape == (n_movies, n_movies)

    def test_content_based_training_performance(self, movies_df, ratings_df):
        """Test that content-based model training meets performance threshold"""
        start_time = time.time()
        
        # Simuler l'extraction de features à partir des genres
        # Créer une matrice one-hot encoding des genres
        genres_split = movies_df['genres'].str.get_dummies('|')
        
        # Prendre un échantillon pour les notes
        sample_ratings = ratings_df.head(10000)
        
        # Calculer les notes moyennes par film
        movie_avg_ratings = sample_ratings.groupby('movieId')['rating'].mean()
        
        # Fusionner avec les genres
        genre_features = genres_split.join(movie_avg_ratings, how='inner')
        
        elapsed_time = time.time() - start_time
        print(f"\nContent-based training time: {elapsed_time:.2f} seconds")
        
        assert elapsed_time < PERFORMANCE_THRESHOLDS['content_training'], \
            f"Content-based training too slow: {elapsed_time:.2f}s > {PERFORMANCE_THRESHOLDS['content_training']}s"
        
        # Vérifier que les features ont été créées
        assert genre_features.shape[1] > 0

    def test_batch_prediction_performance(self, user_movie_matrix):
        """Test batch prediction performance for multiple users"""
        # Prendre un échantillon
        matrix_sample = user_movie_matrix.iloc[:100, :100]
        
        # Entraîner KNN
        knn = NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='brute')
        knn.fit(matrix_sample)
        
        start_time = time.time()
        
        # Prédire pour tous les utilisateurs
        distances, indices = knn.kneighbors(matrix_sample)
        
        elapsed_time = time.time() - start_time
        print(f"\nBatch prediction time for {len(matrix_sample)} users: {elapsed_time:.2f} seconds")
        print(f"Average time per user: {elapsed_time/len(matrix_sample):.4f} seconds")
        
        # Vérifier que les prédictions sont faites
        assert distances.shape[0] == len(matrix_sample)