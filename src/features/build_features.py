"""
Feature Engineering Script
Phase 4.1: Create features from raw data for machine learning models
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
import os

def load_data():
    """Load all necessary data files"""
    # Chemins des fichiers (corrigés pour exécution depuis la racine)
    movies_path = 'data/processed/movies_enriched.csv'
    ratings_path = 'data/raw/ratings.csv'
    user_stats_path = 'user_stats.csv'
    tags_path = 'data/raw/tags.csv'
    
    print("Loading data...")
    df_movies = pd.read_csv(movies_path)
    df_ratings = pd.read_csv(ratings_path)
    df_user_stats = pd.read_csv(user_stats_path)
    
    # Charger les tags s'ils existent
    try:
        df_tags = pd.read_csv(tags_path)
        print(f"Tags loaded: {len(df_tags)} rows")
    except:
        df_tags = None
        print("No tags file found")
    
    print(f"Movies: {len(df_movies)} rows")
    print(f"Ratings: {len(df_ratings)} rows")
    print(f"User stats: {len(df_user_stats)} rows")
    
    return df_movies, df_ratings, df_user_stats, df_tags

def create_user_movie_matrix(df_ratings):
    """Create user-movie matrix from ratings"""
    print("\nCreating user-movie matrix...")
    matrix = df_ratings.pivot_table(
        index='userId', 
        columns='movieId', 
        values='rating'
    )
    print(f"Matrix shape: {matrix.shape}")
    print(f"Fill rate: {(~matrix.isnull()).sum().sum() / (matrix.shape[0] * matrix.shape[1]) * 100:.2f}%")
    return matrix

def normalize_ratings(matrix):
    """Normalize ratings by subtracting user mean"""
    print("\nNormalizing ratings...")
    user_means = matrix.mean(axis=1)
    normalized = matrix.sub(user_means, axis=0)
    print(f"Normalized matrix shape: {normalized.shape}")
    return normalized, user_means

def create_tag_features(df_tags, df_movies, max_features=50):
    """Create TF-IDF features from tags"""
    if df_tags is None:
        print("\nNo tags available")
        return None
    
    print("\nCreating TF-IDF features from tags...")
    # Grouper les tags par film
    movie_tags = df_tags.groupby('movieId')['tag'].apply(lambda x: ' '.join(x)).reset_index()
    print(f"Movies with tags: {len(movie_tags)}")
    
    # TF-IDF
    tfidf = TfidfVectorizer(max_features=max_features, stop_words='english')
    tag_matrix = tfidf.fit_transform(movie_tags['tag'])
    
    # Convertir en DataFrame
    tag_features = pd.DataFrame(
        tag_matrix.toarray(),
        columns=[f"tag_{i}" for i in range(tag_matrix.shape[1])],
        index=movie_tags['movieId']
    )
    
    print(f"Tag features shape: {tag_features.shape}")
    return tag_features

def create_genre_features(df_movies):
    """Create one-hot encoded genre features"""
    print("\nCreating genre features...")
    
    # Convertir les genres en listes
    df_movies['genres_list'] = df_movies['genres'].str.split('|')
    
    # One-hot encoding
    mlb = MultiLabelBinarizer()
    genre_encoded = mlb.fit_transform(df_movies['genres_list'])
    genre_df = pd.DataFrame(
        genre_encoded, 
        columns=mlb.classes_, 
        index=df_movies['movieId']
    )
    
    print(f"Genre features shape: {genre_df.shape}")
    print(f"Genres found: {list(genre_df.columns)}")
    return genre_df

def prepare_movie_features(df_movies, genre_features, tag_features=None):
    """Combine all movie features"""
    print("\nPreparing movie features...")
    
    # Colonnes de base
    base_cols = ['movieId', 'title', 'year_str', 'genre_count', 
                 'rating_count', 'avg_rating', 'std_rating']
    
    movie_features = df_movies[base_cols].copy()
    
    # Ajouter les features de genres
    for col in genre_features.columns:
        movie_features[col] = genre_features[col].values
    
    # Ajouter les features de tags si disponibles
    if tag_features is not None:
        for col in tag_features.columns:
            # Aligner les index
            movie_features[col] = movie_features['movieId'].map(
                tag_features[col].to_dict()
            ).fillna(0)
    
    print(f"Final movie features shape: {movie_features.shape}")
    return movie_features

def save_features(movie_features, user_movie_matrix, normalized_matrix):
    """Save all features to disk"""
    print("\nSaving features...")
    
    # Créer le dossier processed s'il n'existe pas
    os.makedirs('data/processed', exist_ok=True)
    
    movie_features.to_csv('data/processed/movie_features.csv', index=False)
    print(f"   ✅ Movie features saved: data/processed/movie_features.csv")
    
    user_movie_matrix.to_csv('data/processed/user_movie_matrix.csv')
    print(f"   ✅ User-movie matrix saved: data/processed/user_movie_matrix.csv")
    
    normalized_matrix.to_csv('data/processed/user_movie_matrix_norm.csv')
    print(f"   ✅ Normalized matrix saved: data/processed/user_movie_matrix_norm.csv")
    
    print("\n✅ All features saved successfully")

def main():
    """Main function"""
    print("="*50)
    print("FEATURE ENGINEERING PIPELINE")
    print("="*50)
    
    # 1. Charger les données
    df_movies, df_ratings, df_user_stats, df_tags = load_data()
    
    # 2. Créer la matrice utilisateurs-films
    user_movie_matrix = create_user_movie_matrix(df_ratings)
    
    # 3. Normaliser les notes
    normalized_matrix, user_means = normalize_ratings(user_movie_matrix)
    
    # 4. Créer les features de genres
    genre_features = create_genre_features(df_movies)
    
    # 5. Créer les features de tags (optionnel)
    tag_features = create_tag_features(df_tags, df_movies)
    
    # 6. Préparer les features films finales
    movie_features = prepare_movie_features(df_movies, genre_features, tag_features)
    
    # 7. Sauvegarder les features
    save_features(movie_features, user_movie_matrix, normalized_matrix)
    
    print("\n" + "="*50)
    print("FEATURE ENGINEERING COMPLETE")
    print("="*50)
    
    return movie_features, user_movie_matrix, normalized_matrix, user_means

if __name__ == "__main__":
    movie_features, user_movie_matrix, normalized_matrix, user_means = main()