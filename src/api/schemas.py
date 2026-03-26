# src/api/schemas.py
# Définition des modèles de données pour l'API

from pydantic import BaseModel
from typing import List, Optional

# Schéma pour une recommandation (film + score)
class Recommendation(BaseModel):
    movie_id: int
    title: str
    score: float

# Schéma pour la réponse de /recommendations/{user_id}
class RecommendationsResponse(BaseModel):
    user_id: int
    recommendations: List[Recommendation]

# Schéma pour la requête de /feedback
class FeedbackRequest(BaseModel):
    user_id: int
    movie_id: int
    rating: Optional[float] = None
    liked: Optional[bool] = None
    timestamp: Optional[int] = None

# Schéma pour la réponse de /feedback
class FeedbackResponse(BaseModel):
    status: str
    message: str

# Schéma pour les statistiques d'un film
class MovieStatsResponse(BaseModel):
    movie_id: int
    title: str
    rating_count: int
    avg_rating: float
    std_rating: float
    min_rating: float
    max_rating: float

# Schéma pour la requête de /sentiment
class SentimentRequest(BaseModel):
    text: str

# Schéma pour la réponse de /sentiment
class SentimentResponse(BaseModel):
    text: str
    sentiment: str  # positive, negative, neutral
    confidence: float