# src/api/dependencies.py
# Dépendances partagées par les endpoints

import joblib
import pandas as pd
import os
from fastapi import HTTPException

# Variable globale pour les modèles (chargés une seule fois)
_models = None
_movie_features = None
_user_movie_matrix = None

def load_models():
    """Load all models and necessary data"""
    global _models, _movie_features, _user_movie_matrix
    
    if _models is not None:
        return _models, _movie_features, _user_movie_matrix
    
    print("Loading models for API...")
    models = {}
    
    # Charger les modèles
    model_files = {
        'svd': 'svd_model.pkl',
        'knn': 'knn_model.pkl',
        'content': 'content_model.pkl',
        'hybrid': 'hybrid_model.pkl'
    }
    
    for name, path in model_files.items():
        if os.path.exists(path):
            data = joblib.load(path)
            # Si c'est un dictionnaire avec 'model', on extrait le modèle
            if isinstance(data, dict) and 'model' in data:
                models[name] = data['model']
                print(f"   {name} model loaded (from dict)")
            else:
                models[name] = data
                print(f"   {name} model loaded")
        else:
            print(f"   {name} model not found")
    
    # Charger les données nécessaires
    movie_features_path = 'data/processed/movie_features.csv'
    if os.path.exists(movie_features_path):
        _movie_features = pd.read_csv(movie_features_path)
        print(f"   Movie features loaded: {_movie_features.shape}")
    else:
        print(f"   Movie features not found")
        _movie_features = None
    
    # Charger la matrice utilisateurs-films et remplacer les NaN par 0
    matrix_path = 'data/processed/user_movie_matrix_norm.csv'
    if os.path.exists(matrix_path):
        _user_movie_matrix = pd.read_csv(matrix_path, index_col=0).fillna(0)
        print(f"   User-movie matrix loaded: {_user_movie_matrix.shape}")
        print(f"   NaN values replaced with 0")
    else:
        print(f"   User-movie matrix not found")
        _user_movie_matrix = None
    
    _models = models
    return models, _movie_features, _user_movie_matrix

def get_models():
    """FastAPI dependency to get models"""
    models, movie_features, matrix = load_models()
    if not models:
        raise HTTPException(status_code=500, detail="Models not loaded")
    return models, movie_features, matrix