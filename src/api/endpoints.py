# src/api/endpoints.py
# Définition des routes de l'API

from fastapi import APIRouter, Depends, HTTPException
import pandas as pd
import numpy as np
from typing import List
import time

from . import schemas
from .dependencies import get_models

router = APIRouter()

@router.get("/")
def read_root():
    """Root endpoint - API status"""
    return {
        "status": "online",
        "message": "Movie Recommendation API",
        "version": "1.0.0"
    }

@router.get("/recommendations/{user_id}", response_model=schemas.RecommendationsResponse)
def get_recommendations(user_id: int, models_data=Depends(get_models)):
    """
    Get movie recommendations for a specific user
    """
    models, movie_features, matrix = models_data
    
    if 'knn' not in models:
        raise HTTPException(status_code=503, detail="KNN model not available")
    
    if matrix is None or user_id not in matrix.index:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    try:
        # KNN recommendations
        knn_model = models['knn']
        user_idx = matrix.index.get_loc(user_id)
        user_vector = matrix.iloc[[user_idx]].values
        
        distances, indices = knn_model.kneighbors(user_vector, n_neighbors=11)
        neighbor_ids = [matrix.index[i] for i in indices[0][1:]]
        
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
        
        # Calculate average scores
        recommendations = []
        for movie_id, scores in candidate_scores.items():
            if len(scores) >= 2:
                avg_score = np.mean(scores)
                title = movie_features[movie_features['movieId'] == movie_id]['title'].values
                movie_title = title[0] if len(title) > 0 else f"Movie {movie_id}"
                recommendations.append({
                    "movie_id": int(movie_id),
                    "title": movie_title,
                    "score": float(avg_score)
                })
        
        # Sort by score
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "user_id": user_id,
            "recommendations": recommendations[:10]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@router.get("/movies/{movie_id}/stats", response_model=schemas.MovieStatsResponse)
def get_movie_stats(movie_id: int, models_data=Depends(get_models)):
    """
    Get statistics for a specific movie
    """
    _, movie_features, _ = models_data
    
    if movie_features is None:
        raise HTTPException(status_code=503, detail="Movie features not available")
    
    movie_data = movie_features[movie_features['movieId'] == movie_id]
    
    if len(movie_data) == 0:
        raise HTTPException(status_code=404, detail=f"Movie {movie_id} not found")
    
    return {
        "movie_id": movie_id,
        "title": movie_data.iloc[0]['title'],
        "rating_count": int(movie_data.iloc[0]['rating_count']),
        "avg_rating": float(movie_data.iloc[0]['avg_rating']),
        "std_rating": float(movie_data.iloc[0]['std_rating']),
        "min_rating": 0.0,  # Note minimale possible dans MovieLens
        "max_rating": 5.0    # Note maximale possible dans MovieLens
    }

@router.post("/feedback", response_model=schemas.FeedbackResponse)
def post_feedback(feedback: schemas.FeedbackRequest):
    """
    Collect user feedback for future model improvements
    """
    # Ici on pourrait sauvegarder dans un fichier ou une base
    # Pour l'instant, on simule
    print(f"Feedback received: {feedback}")
    
    return {
        "status": "success",
        "message": "Feedback recorded"
    }

@router.post("/sentiment", response_model=schemas.SentimentResponse)
def analyze_sentiment(request: schemas.SentimentRequest):
    """
    Simple sentiment analysis (placeholder)
    """
    text = request.text.lower()
    
    # Sentiment très basique (juste pour l'exemple)
    positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'wonderful']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'boring']
    
    pos_count = sum(1 for word in positive_words if word in text)
    neg_count = sum(1 for word in negative_words if word in text)
    
    if pos_count > neg_count:
        sentiment = "positive"
        confidence = min(0.5 + 0.1 * (pos_count - neg_count), 0.95)
    elif neg_count > pos_count:
        sentiment = "negative"
        confidence = min(0.5 + 0.1 * (neg_count - pos_count), 0.95)
    else:
        sentiment = "neutral"
        confidence = 0.5
    
    return {
        "text": request.text,
        "sentiment": sentiment,
        "confidence": confidence
    }