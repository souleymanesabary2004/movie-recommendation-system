"""
Hybrid Model Training Script
Phase 4.2: Combine collaborative and content-based filtering
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity

def load_models():
    """Load pre-trained models"""
    print("Loading pre-trained models...")
    
    models = {}
    
    # Charger le modèle KNN
    if os.path.exists('knn_model.pkl'):
        knn_data = joblib.load('knn_model.pkl')
        models['knn'] = knn_data['model']
        print("   ✅ KNN model loaded")
    
    # Charger le modèle SVD
    if os.path.exists('svd_model.pkl'):
        svd_data = joblib.load('svd_model.pkl')
        models['svd'] = svd_data['model']
        print("   ✅ SVD model loaded")
    
    # Charger le modèle content-based
    if os.path.exists('content_model.pkl'):
        content_data = joblib.load('content_model.pkl')
        models['content'] = {
            'similarity_matrix': content_data['similarity_matrix'],
            'movie_to_idx': content_data['movie_to_idx'],
            'idx_to_movie': content_data['idx_to_movie']
        }
        print("   ✅ Content-based model loaded")
    
    return models

def load_data():
    """Load necessary data"""
    print("\nLoading data...")
    
    # Charger la matrice utilisateurs-films
    matrix_path = 'data/processed/user_movie_matrix_norm.csv'
    if os.path.exists(matrix_path):
        user_movie_matrix = pd.read_csv(matrix_path, index_col=0).fillna(0)
        print(f"   ✅ User-movie matrix loaded: {user_movie_matrix.shape}")
    else:
        user_movie_matrix = None
        print("   ❌ User-movie matrix not found")
    
    # Charger les features films
    features_path = 'data/processed/movie_features.csv'
    if os.path.exists(features_path):
        movie_features = pd.read_csv(features_path)
        print(f"   ✅ Movie features loaded: {movie_features.shape}")
    else:
        movie_features = None
        print("   ❌ Movie features not found")
    
    return user_movie_matrix, movie_features

def hybrid_recommendation(user_id, models, user_movie_matrix, movie_features, n_recommendations=10, alpha=0.5):
    """
    Generate hybrid recommendations
    alpha = weight for collaborative (1-alpha = weight for content-based)
    """
    print(f"\nGenerating hybrid recommendations for user {user_id}...")
    
    recommendations = {}
    
    # Partie 1: Collaborative filtering (KNN)
    if 'knn' in models and user_movie_matrix is not None:
        try:
            user_idx = user_movie_matrix.index.get_loc(user_id)
            user_vector = user_movie_matrix.iloc[[user_idx]].values
            
            # Trouver les voisins
            distances, indices = models['knn'].kneighbors(user_vector, n_neighbors=11)
            neighbor_ids = [user_movie_matrix.index[i] for i in indices[0][1:]]
            
            # Collecter les films aimés par les voisins
            collab_scores = {}
            for neighbor_id in neighbor_ids:
                neighbor_ratings = user_movie_matrix.loc[neighbor_id]
                liked = neighbor_ratings[neighbor_ratings > 0].index
                for movie_id in liked:
                    if movie_id not in user_movie_matrix.loc[user_id][user_movie_matrix.loc[user_id] != 0].index:
                        if movie_id not in collab_scores:
                            collab_scores[movie_id] = []
                        collab_scores[movie_id].append(neighbor_ratings[movie_id])
            
            # Moyenne des scores
            for movie_id, scores in collab_scores.items():
                if len(scores) >= 2:
                    recommendations[movie_id] = alpha * np.mean(scores)
            
            print(f"   Collaborative: {len(recommendations)} candidates")
        except:
            print("   Collaborative filtering failed")
    
    # Partie 2: Content-based
    if 'content' in models and movie_features is not None:
        try:
            # Films déjà vus par l'utilisateur
            if user_movie_matrix is not None and user_id in user_movie_matrix.index:
                seen_movies = user_movie_matrix.loc[user_id][user_movie_matrix.loc[user_id] != 0].index
                
                # Prendre les films aimés par l'utilisateur
                liked_movies = user_movie_matrix.loc[user_id][user_movie_matrix.loc[user_id] > 0].index
                
                content_scores = {}
                for movie_id in liked_movies[:5]:  # Top 5 films aimés
                    if movie_id in models['content']['movie_to_idx']:
                        idx = models['content']['movie_to_idx'][movie_id]
                        similarities = models['content']['similarity_matrix'][idx]
                        
                        # Trouver les films similaires
                        similar_indices = np.argsort(similarities)[-11:-1][::-1]
                        for sim_idx in similar_indices:
                            sim_movie_id = models['content']['idx_to_movie'][sim_idx]
                            if sim_movie_id not in seen_movies:
                                if sim_movie_id not in content_scores:
                                    content_scores[sim_movie_id] = []
                                content_scores[sim_movie_id].append(similarities[sim_idx])
                
                # Ajouter au pool de recommandations
                for movie_id, scores in content_scores.items():
                    if len(scores) >= 2:
                        if movie_id in recommendations:
                            recommendations[movie_id] += (1-alpha) * np.mean(scores)
                        else:
                            recommendations[movie_id] = (1-alpha) * np.mean(scores)
                
                print(f"   Content-based: {len(content_scores)} candidates")
        except:
            print("   Content-based filtering failed")
    
    # Trier et retourner
    sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
    
    # Récupérer les titres des films
    result = []
    for movie_id, score in sorted_recs[:n_recommendations]:
        title = movie_features[movie_features['movieId'] == movie_id]['title'].values
        movie_title = title[0] if len(title) > 0 else f"Movie {movie_id}"
        result.append((movie_id, movie_title, score))
    
    return result

def save_model(models, params, filename='hybrid_model.pkl'):
    """Save the hybrid model configuration"""
    model_data = {
        'models': models,  # Références aux autres modèles
        'params': params,
        'version': '1.0'
    }
    joblib.dump(model_data, filename)
    print(f"\n✅ Hybrid model config saved to {filename}")

def main():
    """Main training function"""
    print("="*50)
    print("HYBRID MODEL TRAINING")
    print("="*50)
    
    # Paramètres
    params = {
        'alpha': 0.5,  # Poids du collaboratif
        'n_neighbors_knn': 10,
        'n_liked_movies': 5
    }
    
    print("\nParameters:")
    for k, v in params.items():
        print(f"   {k}: {v}")
    
    # Charger les modèles pré-entraînés
    models = load_models()
    
    # Charger les données
    user_movie_matrix, movie_features = load_data()
    
    # Sauvegarder la configuration hybride
    save_model(models, params)
    
    # Tester sur quelques utilisateurs
    print("\n" + "="*50)
    print("TESTING HYBRID RECOMMENDATIONS")
    print("="*50)
    
    test_users = [1, 10, 50, 100]
    
    for user_id in test_users:
        if user_movie_matrix is not None and user_id in user_movie_matrix.index:
            recs = hybrid_recommendation(
                user_id, models, user_movie_matrix, movie_features,
                n_recommendations=5, alpha=params['alpha']
            )
            
            print(f"\nUser {user_id} - Top 5 recommendations:")
            for i, (movie_id, title, score) in enumerate(recs, 1):
                print(f"   {i}. {title} (score: {score:.4f})")
    
    print("\n" + "="*50)
    print("HYBRID MODEL TRAINING COMPLETE")
    print("="*50)
    
    return models

if __name__ == "__main__":
    models = main()