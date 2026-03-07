"""
Content-Based Model Training Script
Phase 4.2: Recommend similar movies based on content features
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

def load_movie_features():
    """Load movie features"""
    print("Loading movie features...")
    
    features_path = 'data/processed/movie_features.csv'
    if os.path.exists(features_path):
        df = pd.read_csv(features_path)
        print(f"Loaded movie features: {df.shape}")
        return df
    else:
        print("ERROR: movie_features.csv not found")
        return None

def prepare_feature_matrix(df):
    """Prepare feature matrix for similarity computation"""
    print("\nPreparing feature matrix...")
    
    # Identifier les colonnes de features (tout sauf movieId, title)
    feature_cols = [col for col in df.columns if col not in ['movieId', 'title']]
    
    # Créer la matrice et remplacer les NaN par 0
    feature_matrix = df[feature_cols].fillna(0).values
    
    print(f"Feature matrix shape: {feature_matrix.shape}")
    print(f"Number of features: {len(feature_cols)}")
    print(f"NaN values replaced with 0")
    
    return feature_matrix, feature_cols

def compute_similarity_matrix(feature_matrix):
    """Compute cosine similarity between all movies"""
    print("\nComputing similarity matrix...")
    print("   This may take a few minutes for 9742 movies...")
    
    similarity = cosine_similarity(feature_matrix)
    
    print(f"Similarity matrix shape: {similarity.shape}")
    
    return similarity

def get_movie_indices(df):
    """Create mapping from movieId to index"""
    movie_to_idx = {row['movieId']: idx for idx, row in df.iterrows()}
    idx_to_movie = {idx: row['movieId'] for idx, row in df.iterrows()}
    
    print(f"Number of movies mapped: {len(movie_to_idx)}")
    
    return movie_to_idx, idx_to_movie

def evaluate_model(similarity_matrix, df, n_test=50):
    """Quick evaluation of the model"""
    print("\nEvaluating model...")
    
    # Tester sur quelques films aléatoires
    test_indices = np.random.choice(len(df), size=min(n_test, len(df)), replace=False)
    
    total_similarity = 0
    
    for idx in test_indices:
        # Similarités pour ce film (exclure lui-même)
        similarities = similarity_matrix[idx]
        top_similar = np.sort(similarities)[-5:-1]  # Top 4 (exclure le film lui-même)
        total_similarity += np.mean(top_similar)
    
    avg_similarity = total_similarity / len(test_indices)
    print(f"   Average similarity between top similar movies: {avg_similarity:.4f}")
    
    return {'avg_similarity': avg_similarity}

def save_model(similarity_matrix, movie_to_idx, idx_to_movie, params, metrics, filename='content_model.pkl'):
    """Save the trained model"""
    model_data = {
        'similarity_matrix': similarity_matrix,
        'movie_to_idx': movie_to_idx,
        'idx_to_movie': idx_to_movie,
        'params': params,
        'metrics': metrics,
        'version': '1.0'
    }
    joblib.dump(model_data, filename)
    print(f"\n✅ Model saved to {filename}")

def main():
    """Main training function"""
    print("="*50)
    print("CONTENT-BASED MODEL TRAINING")
    print("="*50)
    
    # Paramètres
    params = {
        'metric': 'cosine',
        'feature_source': 'movie_features.csv',
        'nan_handling': 'fillna(0)'
    }
    
    print("\nParameters:")
    for k, v in params.items():
        print(f"   {k}: {v}")
    
    # Charger les features
    df = load_movie_features()
    if df is None:
        return
    
    # Préparer la matrice
    feature_matrix, feature_cols = prepare_feature_matrix(df)
    
    # Calculer la similarité
    similarity_matrix = compute_similarity_matrix(feature_matrix)
    
    # Créer les mappings
    movie_to_idx, idx_to_movie = get_movie_indices(df)
    
    # Évaluer
    metrics = evaluate_model(similarity_matrix, df)
    
    # Sauvegarder
    save_model(similarity_matrix, movie_to_idx, idx_to_movie, params, metrics)
    
    # Exemple de recommandation
    print("\n" + "="*50)
    print("EXAMPLE RECOMMENDATIONS")
    print("="*50)
    
    # Prendre un film exemple (Toy Story)
    example_movie = 1
    if example_movie in movie_to_idx:
        idx = movie_to_idx[example_movie]
        movie_title = df[df['movieId'] == example_movie]['title'].values[0]
        
        print(f"\nMovie: {movie_title}")
        print("Top 5 similar movies:")
        
        # Trouver les films les plus similaires
        similarities = similarity_matrix[idx]
        top_indices = np.argsort(similarities)[-6:-1][::-1]  # Top 5 (exclure lui-même)
        
        for i, sim_idx in enumerate(top_indices, 1):
            sim_movie_id = idx_to_movie[sim_idx]
            sim_title = df[df['movieId'] == sim_movie_id]['title'].values[0]
            sim_score = similarities[sim_idx]
            print(f"   {i}. {sim_title} (similarity: {sim_score:.4f})")
    
    print("\n" + "="*50)
    print("CONTENT-BASED TRAINING COMPLETE")
    print("="*50)
    
    return similarity_matrix, movie_to_idx, idx_to_movie

if __name__ == "__main__":
    similarity_matrix, movie_to_idx, idx_to_movie = main()