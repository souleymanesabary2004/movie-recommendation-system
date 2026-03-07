"""
Prediction Script
Phase 4.4: Generate recommendations using trained models
"""

import pandas as pd
import numpy as np
import joblib
import os

def load_models():
    """Load all trained models"""
    print("Loading trained models...")
    
    models = {}
    
    # SVD Model
    if os.path.exists('svd_model.pkl'):
        svd_data = joblib.load('svd_model.pkl')
        models['svd'] = svd_data['model']
        print("   SVD model loaded")
    
    # KNN Model
    if os.path.exists('knn_model.pkl'):
        knn_data = joblib.load('knn_model.pkl')
        models['knn'] = knn_data['model']
        print("   KNN model loaded")
    
    # Content-based Model
    if os.path.exists('content_model.pkl'):
        content_data = joblib.load('content_model.pkl')
        models['content'] = content_data
        print("   Content-based model loaded")
    
    # Hybrid Model (just the config)
    if os.path.exists('hybrid_model.pkl'):
        hybrid_data = joblib.load('hybrid_model.pkl')
        models['hybrid_config'] = hybrid_data
        print("   Hybrid config loaded")
    
    return models

def load_data():
    """Load necessary data"""
    print("\nLoading data...")
    
    # User-movie matrix
    matrix_path = 'data/processed/user_movie_matrix_norm.csv'
    if os.path.exists(matrix_path):
        user_movie_matrix = pd.read_csv(matrix_path, index_col=0).fillna(0)
        print(f"   User-movie matrix loaded: {user_movie_matrix.shape}")
    else:
        user_movie_matrix = None
        print("   User-movie matrix not found")
    
    # Movie features
    features_path = 'data/processed/movie_features.csv'
    if os.path.exists(features_path):
        movie_features = pd.read_csv(features_path)
        print(f"   Movie features loaded: {movie_features.shape}")
    else:
        movie_features = None
        print("   Movie features not found")
    
    return user_movie_matrix, movie_features

def predict_svd(user_id, model, matrix, movie_features, n_recommendations=10):
    """Generate recommendations using SVD"""
    print(f"\nSVD Recommendations for user {user_id}:")
    
    try:
        # Get user index
        user_idx = matrix.index.get_loc(user_id)
        
        # Get user vector
        user_vector = matrix.iloc[[user_idx]].values
        
        # Predict all ratings
        pred_ratings = model.transform(user_vector) @ model.components_
        
        # Get movies not seen by user
        seen_movies = matrix.loc[user_id][matrix.loc[user_id] != 0].index
        all_movies = matrix.columns
        unseen_movies = [m for m in all_movies if m not in seen_movies]
        
        # Get predictions for unseen movies
        predictions = []
        for movie_id in unseen_movies:
            movie_idx = list(all_movies).index(movie_id)
            pred_score = pred_ratings[0, movie_idx]
            predictions.append((movie_id, pred_score))
        
        # Sort by predicted score
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        # Get movie titles
        results = []
        for movie_id, score in predictions[:n_recommendations]:
            title = movie_features[movie_features['movieId'] == movie_id]['title'].values
            movie_title = title[0] if len(title) > 0 else f"Movie {movie_id}"
            results.append((movie_id, movie_title, score))
        
        return results
    
    except Exception as e:
        print(f"   Error: {e}")
        return []

def predict_knn(user_id, model, matrix, movie_features, n_recommendations=10):
    """Generate recommendations using KNN"""
    print(f"\nKNN Recommendations for user {user_id}:")
    
    try:
        # Find similar users
        user_idx = matrix.index.get_loc(user_id)
        user_vector = matrix.iloc[[user_idx]].values
        
        distances, indices = model.kneighbors(user_vector, n_neighbors=11)
        neighbor_ids = [matrix.index[i] for i in indices[0][1:]]
        
        # Collect movies liked by neighbors
        seen_movies = matrix.loc[user_id][matrix.loc[user_id] != 0].index
        candidate_scores = {}
        
        for neighbor_id in neighbor_ids:
            neighbor_ratings = matrix.loc[neighbor_id]
            liked = neighbor_ratings[neighbor_ratings > 0].index
            for movie_id in liked:
                if movie_id not in seen_movies:
                    if movie_id not in candidate_scores:
                        candidate_scores[movie_id] = []
                    candidate_scores[movie_id].append(neighbor_ratings[movie_id])
        
        # Average scores
        predictions = []
        for movie_id, scores in candidate_scores.items():
            if len(scores) >= 2:
                avg_score = np.mean(scores)
                predictions.append((movie_id, avg_score))
        
        # Sort and return
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for movie_id, score in predictions[:n_recommendations]:
            title = movie_features[movie_features['movieId'] == movie_id]['title'].values
            movie_title = title[0] if len(title) > 0 else f"Movie {movie_id}"
            results.append((movie_id, movie_title, score))
        
        return results
    
    except Exception as e:
        print(f"   Error: {e}")
        return []

def predict_content(user_id, model_data, matrix, movie_features, n_recommendations=10):
    """Generate recommendations using content-based model"""
    print(f"\nContent-based Recommendations for user {user_id}:")
    
    try:
        # Get movies liked by user
        if user_id not in matrix.index:
            return []
        
        user_ratings = matrix.loc[user_id]
        liked_movies = user_ratings[user_ratings > 0].index[:5]  # Top 5 liked
        
        seen_movies = user_ratings[user_ratings != 0].index
        
        similarity_matrix = model_data['similarity_matrix']
        movie_to_idx = model_data['movie_to_idx']
        idx_to_movie = model_data['idx_to_movie']
        
        candidate_scores = {}
        
        for movie_id in liked_movies:
            if movie_id in movie_to_idx:
                idx = movie_to_idx[movie_id]
                similarities = similarity_matrix[idx]
                
                # Get top similar movies
                top_indices = np.argsort(similarities)[-11:-1][::-1]
                for sim_idx in top_indices:
                    sim_movie_id = idx_to_movie[sim_idx]
                    if sim_movie_id not in seen_movies:
                        if sim_movie_id not in candidate_scores:
                            candidate_scores[sim_movie_id] = []
                        candidate_scores[sim_movie_id].append(similarities[sim_idx])
        
        # Average scores
        predictions = []
        for movie_id, scores in candidate_scores.items():
            if len(scores) >= 2:
                avg_score = np.mean(scores)
                predictions.append((movie_id, avg_score))
        
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for movie_id, score in predictions[:n_recommendations]:
            title = movie_features[movie_features['movieId'] == movie_id]['title'].values
            movie_title = title[0] if len(title) > 0 else f"Movie {movie_id}"
            results.append((movie_id, movie_title, score))
        
        return results
    
    except Exception as e:
        print(f"   Error: {e}")
        return []

def main():
    """Main prediction function"""
    print("="*50)
    print("PREDICTION - GENERATE RECOMMENDATIONS")
    print("="*50)
    
    # Load models and data
    models = load_models()
    matrix, movie_features = load_data()
    
    if matrix is None or movie_features is None:
        print("\nCannot generate predictions without data")
        return
    
    # Test users
    test_users = [1, 10, 50, 100]
    
    for user_id in test_users:
        if user_id not in matrix.index:
            continue
        
        print("\n" + "="*50)
        print(f"RECOMMENDATIONS FOR USER {user_id}")
        print("="*50)
        
        # SVD predictions
        if 'svd' in models:
            svd_recs = predict_svd(user_id, models['svd'], matrix, movie_features, n_recommendations=5)
            for i, (_, title, score) in enumerate(svd_recs, 1):
                print(f"   SVD {i}: {title} (score: {score:.4f})")
        
        # KNN predictions
        if 'knn' in models:
            knn_recs = predict_knn(user_id, models['knn'], matrix, movie_features, n_recommendations=5)
            for i, (_, title, score) in enumerate(knn_recs, 1):
                print(f"   KNN {i}: {title} (score: {score:.4f})")
        
        # Content-based predictions
        if 'content' in models:
            content_recs = predict_content(user_id, models['content'], matrix, movie_features, n_recommendations=5)
            for i, (_, title, score) in enumerate(content_recs, 1):
                print(f"   CONTENT {i}: {title} (score: {score:.4f})")
    
    print("\n" + "="*50)
    print("PREDICTION COMPLETE")
    print("="*50)

if __name__ == "__main__":
    main()