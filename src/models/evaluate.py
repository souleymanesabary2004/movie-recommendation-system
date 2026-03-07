"""
Evaluation Script
Phase 4.3: Compare all models with standard metrics
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error

def load_all_models():
    """Load all trained models"""
    print("Loading trained models...")
    
    models = {}
    metrics = {}
    
    # 1. SVD Model
    if os.path.exists('svd_model.pkl'):
        svd_data = joblib.load('svd_model.pkl')
        models['svd'] = svd_data['model']
        metrics['svd'] = svd_data.get('metrics', {})
        print("   SVD model loaded")
    
    # 2. KNN Model
    if os.path.exists('knn_model.pkl'):
        knn_data = joblib.load('knn_model.pkl')
        models['knn'] = knn_data['model']
        metrics['knn'] = knn_data.get('metrics', {})
        print("   KNN model loaded")
    
    # 3. Content-based Model
    if os.path.exists('content_model.pkl'):
        content_data = joblib.load('content_model.pkl')
        models['content'] = content_data
        metrics['content'] = content_data.get('metrics', {})
        print("   Content-based model loaded")
    
    # 4. Hybrid Model
    if os.path.exists('hybrid_model.pkl'):
        hybrid_data = joblib.load('hybrid_model.pkl')
        models['hybrid'] = hybrid_data
        print("   Hybrid model loaded")
    
    return models, metrics

def load_test_data():
    """Load data for evaluation"""
    print("\nLoading test data...")
    
    # Load user-movie matrix
    matrix_path = 'data/processed/user_movie_matrix_norm.csv'
    if os.path.exists(matrix_path):
        user_movie_matrix = pd.read_csv(matrix_path, index_col=0).fillna(0)
        print(f"   User-movie matrix loaded: {user_movie_matrix.shape}")
    else:
        user_movie_matrix = None
        print("   User-movie matrix not found")
    
    # Load movie features
    features_path = 'data/processed/movie_features.csv'
    if os.path.exists(features_path):
        movie_features = pd.read_csv(features_path)
        print(f"   Movie features loaded: {movie_features.shape}")
    else:
        movie_features = None
        print("   Movie features not found")
    
    return user_movie_matrix, movie_features

def evaluate_svd(model, matrix):
    """Evaluate SVD model"""
    print("\nSVD MODEL EVALUATION")
    print("-" * 40)
    
    R = matrix.values
    R_pred = model.transform(R) @ model.components_
    
    # RMSE and MAE on known ratings
    mask = (R != 0)
    true_ratings = R[mask]
    pred_ratings = R_pred[mask]
    
    rmse = np.sqrt(mean_squared_error(true_ratings, pred_ratings))
    mae = mean_absolute_error(true_ratings, pred_ratings)
    
    print(f"   RMSE: {rmse:.4f}")
    print(f"   MAE: {mae:.4f}")
    print(f"   Explained variance: {model.explained_variance_ratio_.sum():.4f}")
    
    return {'rmse': rmse, 'mae': mae, 'explained_variance': model.explained_variance_ratio_.sum()}

def evaluate_knn(model, matrix):
    """Evaluate KNN model"""
    print("\nKNN MODEL EVALUATION")
    print("-" * 40)
    
    # Average similarity between users
    n_test = min(100, matrix.shape[0])
    test_users = np.random.choice(matrix.index, size=n_test, replace=False)
    
    similarities = []
    for user_id in test_users:
        user_idx = matrix.index.get_loc(user_id)
        user_vector = matrix.iloc[[user_idx]].values
        
        distances, indices = model.kneighbors(user_vector, n_neighbors=6)
        avg_sim = np.mean(1 - distances[0][1:])
        similarities.append(avg_sim)
    
    avg_similarity = np.mean(similarities)
    print(f"   Average user similarity: {avg_similarity:.4f}")
    
    return {'avg_similarity': avg_similarity}

def evaluate_content(model_data, movie_features):
    """Evaluate content-based model"""
    print("\nCONTENT-BASED MODEL EVALUATION")
    print("-" * 40)
    
    similarity_matrix = model_data['similarity_matrix']
    
    # Average similarity between similar movies
    n_test = min(100, similarity_matrix.shape[0])
    test_indices = np.random.choice(similarity_matrix.shape[0], size=n_test, replace=False)
    
    similarities = []
    for idx in test_indices:
        sim_scores = similarity_matrix[idx]
        top_similar = np.sort(sim_scores)[-5:-1]  # Top 4 (exclude itself)
        similarities.append(np.mean(top_similar))
    
    avg_similarity = np.mean(similarities)
    print(f"   Average similarity between similar movies: {avg_similarity:.4f}")
    
    return {'avg_similarity': avg_similarity}

def evaluate_hybrid(model_data, user_movie_matrix, movie_features):
    """Evaluate hybrid model (simulation)"""
    print("\nHYBRID MODEL EVALUATION")
    print("-" * 40)
    
    # Simple simulation
    print("   Hybrid model combines collaborative and content-based")
    print("   Performance depends on component models")
    
    return {'status': 'combined'}

def generate_summary(all_metrics):
    """Generate a summary table of all metrics"""
    print("\n" + "="*50)
    print("MODEL COMPARISON SUMMARY")
    print("="*50)
    
    # Create DataFrame for comparison
    summary = []
    
    for model_name, metrics in all_metrics.items():
        row = {'Model': model_name.upper()}
        row.update(metrics)
        summary.append(row)
    
    df_summary = pd.DataFrame(summary)
    print(df_summary.to_string(index=False))
    
    return df_summary

def main():
    """Main evaluation function"""
    print("="*50)
    print("MODEL EVALUATION - PHASE 4.3")
    print("="*50)
    
    # Load models
    models, saved_metrics = load_all_models()
    
    # Load data
    user_movie_matrix, movie_features = load_test_data()
    
    if user_movie_matrix is None:
        print("\nCannot evaluate without data")
        return
    
    # Evaluate each model
    all_metrics = {}
    
    if 'svd' in models:
        all_metrics['svd'] = evaluate_svd(models['svd'], user_movie_matrix)
    
    if 'knn' in models:
        all_metrics['knn'] = evaluate_knn(models['knn'], user_movie_matrix)
    
    if 'content' in models and movie_features is not None:
        all_metrics['content'] = evaluate_content(models['content'], movie_features)
    
    if 'hybrid' in models:
        all_metrics['hybrid'] = evaluate_hybrid(models['hybrid'], user_movie_matrix, movie_features)
    
    # Generate summary
    summary = generate_summary(all_metrics)
    
    # Save results
    summary.to_csv('model_evaluation_results.csv', index=False)
    print("\nEvaluation results saved to model_evaluation_results.csv")
    
    print("\n" + "="*50)
    print("EVALUATION COMPLETE")
    print("="*50)
    
    return all_metrics

if __name__ == "__main__":
    all_metrics = main()