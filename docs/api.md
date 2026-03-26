# API Documentation – Movie Recommendation System

This document describes all FastAPI endpoints used in the Movie Recommendation System.  
Everything is structured to support the deployed system (Phase 5).

---

## 1. Base Information

| Key            | Value                |
|----------------|----------------------|
| Base URL       | `http://localhost:8000` |
| API Framework  | FastAPI              |
| Documentation  | `/docs` (Swagger UI) |
| Format         | JSON                 |
| Authentication | None (public local API) |

---

## 2. Endpoints Overview

| Endpoint                      | Method | Description                                 |
|------------------------------|--------|---------------------------------------------|
| `/recommendations/{user_id}` | GET    | Returns top movie recommendations for a user |
| `/movies/{movie_id}/stats`   | GET    | Returns statistical information about a movie |
| `/feedback`                  | POST   | Records user feedback (like/dislike/rating) |
| `/sentiment`                 | POST   | Runs sentiment analysis on a text input      |
| `/health`                    | GET    | Health check of the API                      |

---

## 3. GET `/recommendations/{user_id}`

### ✔️ Description  
Returns a list of recommended movies for a specific user.


| Parameter | Type | Description           | Example |
|-----------|------|-----------------------|---------|
| user_id   | int  | Unique user ID        | 148     |

### ✔️ Success Response

```json
{
  "user_id": 148,
  "recommendations": [
    { "movie_id": 296, "title": "Pulp Fiction (1994)", "score": 0.987 },
    { "movie_id": 318, "title": "The Shawshank Redemption (1994)", "score": 0.965 }
  ]
}



