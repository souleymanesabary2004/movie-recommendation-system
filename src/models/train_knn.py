"""
KNN Model Training Script
Phase 4.2: Collaborative Filtering with K-Nearest Neighbors
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import joblib
import os

def load_data():
    """Load pre-computed matrices"""
    print("Loading data...")
    
    # Charger la matrice normalisée
    matrix_path = 'data/processed/user_movie_matrix_norm.csv'
    if os.path.exists(matrix_path):
        user_movie_matrix = pd.read_csv(matrix_path, index_col=0)
        user_movie_matrix = user_movie_matrix.fillna(0)
        print(f"Loaded normalized matrix: {user_movie_matrix.shape}")
    else:
        # Fallback
        ratings_path = 'data/raw/ratings.csv'
        df_ratings = pd.read_csv(ratings_path)
        user_movie_matrix = df_ratings.pivot_table(
            index='userId', 
            columns='movieId', 
            values='rating'
        ).fillna(0)
        print(f"Created matrix: {user_movie_matrix.shape}")
    
    return user_movie_matrix

def train_knn(matrix, n_neighbors=20, metric='cosine'):
    """Train KNN model for collaborative filtering"""
    print(f"\nTraining KNN model with {n_neighbors} neighbors...")
    
    # Créer et entraîner le modèle KNN
    model = NearestNeighbors(
        n_neighbors=n_neighbors,
        metric=metric,
        algorithm='brute',
        n_jobs=-1
    )
    
    model.fit(matrix.values)
    
    print(f"   Model trained successfully")
    print(f"   Metric: {metric}")
    print(f"   Number of users: {matrix.shape[0]}")
    
    return model

def evaluate_model(matrix, model, n_test_users=50):
    """Quick evaluation of the model"""
    print("\nEvaluating model...")
    
    # Tester sur quelques utilisateurs aléatoires
    test_users = np.random.choice(matrix.index, size=min(n_test_users, matrix.shape[0]), replace=False)
    
    total_similarity = 0
    n_pairs = 0
    
    for user_id in test_users:
        user_idx = matrix.index.get_loc(user_id)
        user_vector = matrix.iloc[[user_idx]].values
        
        # Trouver les voisins
        distances, indices = model.kneighbors(user_vector, n_neighbors=6)
        
        # Similarité moyenne (exclure soi-même)
        avg_sim = np.mean(1 - distances[0][1:])
        total_similarity += avg_sim
        n_pairs += 1
    
    avg_similarity = total_similarity / n_pairs if n_pairs > 0 else 0
    print(f"   Average similarity between users: {avg_similarity:.4f}")
    
    return {'avg_similarity': avg_similarity}

def save_model(model, params, metrics, filename='knn_model.pkl'):
    """Save the trained model"""
    model_data = {
        'model': model,
        'params': params,
        'metrics': metrics,
        'version': '1.0'
    }
    joblib.dump(model_data, filename)
    print(f"\n✅ Model saved to {filename}")

def main():
    """Main training function"""
    print("="*50)
    print("KNN MODEL TRAINING")
    print("="*50)
    
    # Paramètres
    params = {
        'n_neighbors': 20,
        'metric': 'cosine'
    }
    
    print("\nParameters:")
    for k, v in params.items():
        print(f"   {k}: {v}")
    
    # Charger les données
    matrix = load_data()
    
    print(f"\nMatrix stats:")
    print(f"   Shape: {matrix.shape}")
    print(f"   Users: {matrix.shape[0]}")
    print(f"   Movies: {matrix.shape[1]}")
    
    # Entraîner
    model = train_knn(
        matrix,
        n_neighbors=params['n_neighbors'],
        metric=params['metric']
    )
    
    # Évaluer
    metrics = evaluate_model(matrix, model)
    
    # Sauvegarder
    save_model(model, params, metrics)
    
    print("\n" + "="*50)
    print("KNN TRAINING COMPLETE")
    print("="*50)
    
    return model

if __name__ == "__main__":
    model = main()