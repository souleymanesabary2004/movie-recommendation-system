"""
ALS Model Training Script (with SVD instead of NMF)
Phase 4.2: Matrix Factorization with TruncatedSVD
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error
import joblib
import os

def load_data():
    """Load pre-computed matrices"""
    print("Loading data...")
    
    # Charger la matrice normalisée
    matrix_path = 'data/processed/user_movie_matrix_norm.csv'
    if os.path.exists(matrix_path):
        user_movie_matrix = pd.read_csv(matrix_path, index_col=0)
        # Remplacer les NaN par 0
        user_movie_matrix = user_movie_matrix.fillna(0)
        print(f"Loaded normalized matrix: {user_movie_matrix.shape}")
        print(f"NaN values replaced with 0")
    else:
        # Fallback: créer la matrice depuis les ratings
        print("Normalized matrix not found, creating from ratings...")
        ratings_path = 'data/raw/ratings.csv'
        df_ratings = pd.read_csv(ratings_path)
        user_movie_matrix = df_ratings.pivot_table(
            index='userId', 
            columns='movieId', 
            values='rating'
        ).fillna(0)
        print(f"Created matrix: {user_movie_matrix.shape}")
    
    # Vérifier qu'il n'y a plus de NaN
    assert not user_movie_matrix.isnull().any().any(), "Matrix still contains NaN values"
    
    return user_movie_matrix

def train_svd(matrix, n_factors=20, n_iter=10):
    """Train SVD model"""
    print(f"\nTraining SVD model with {n_factors} factors...")
    
    # Convertir en numpy array
    R = matrix.values
    
    # Créer et entraîner le modèle SVD
    model = TruncatedSVD(
        n_components=n_factors,
        n_iter=n_iter,
        random_state=42
    )
    
    # Factorisation
    W = model.fit_transform(R)  # Users × factors
    H = model.components_        # Factors × movies
    
    # Reconstruire la matrice
    R_pred = np.dot(W, H)
    
    print(f"   User factors shape: {W.shape}")
    print(f"   Movie factors shape: {H.shape}")
    print(f"   Explained variance: {model.explained_variance_ratio_.sum():.4f}")
    
    return model, W, H, R_pred

def evaluate(model, R, R_pred):
    """Evaluate the model"""
    print("\nEvaluating model...")
    
    # RMSE sur les notes connues (là où R != 0)
    mask = (R != 0)
    true_ratings = R[mask]
    pred_ratings = R_pred[mask]
    
    if len(true_ratings) > 0:
        rmse = np.sqrt(mean_squared_error(true_ratings, pred_ratings))
        mae = np.mean(np.abs(true_ratings - pred_ratings))
        
        print(f"   RMSE: {rmse:.4f}")
        print(f"   MAE: {mae:.4f}")
        print(f"   Evaluated on {len(true_ratings):,} known ratings")
    else:
        rmse, mae = 0, 0
        print("   No ratings to evaluate")
    
    return rmse, mae

def save_model(model, params, metrics, filename='svd_model.pkl'):
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
    print("SVD MODEL TRAINING")
    print("="*50)
    
    # Paramètres
    params = {
        'n_factors': 20,
        'n_iter': 10
    }
    
    print("\nParameters:")
    for k, v in params.items():
        print(f"   {k}: {v}")
    
    # Charger les données
    matrix = load_data()
    R = matrix.values
    
    print(f"\nMatrix stats:")
    print(f"   Shape: {R.shape}")
    print(f"   Non-zero entries: {(R != 0).sum():,}")
    print(f"   Fill rate: {(R != 0).sum() / R.size * 100:.2f}%")
    
    # Entraîner
    model, W, H, R_pred = train_svd(
        matrix, 
        n_factors=params['n_factors'],
        n_iter=params['n_iter']
    )
    
    # Évaluer
    rmse, mae = evaluate(model, R, R_pred)
    metrics = {'rmse': rmse, 'mae': mae}
    
    # Sauvegarder
    save_model(model, params, metrics)
    
    print("\n" + "="*50)
    print("TRAINING COMPLETE")
    print("="*50)
    
    return model, W, H

if __name__ == "__main__":
    model, W, H = main()