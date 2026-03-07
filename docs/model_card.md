# Model Card - Movie Recommendation System

## Model Details

### SVD Model (Matrix Factorization)
- **Algorithm:** TruncatedSVD (scikit-learn)
- **Parameters:** n_factors=20, n_iter=10
- **Input:** User-movie matrix (610 × 9724)
- **Output:** Predicted ratings matrix
- **Performance:** RMSE=0.7456, MAE=0.5296
- **Use case:** Rating prediction, collaborative filtering

### KNN Model (Collaborative Filtering)
- **Algorithm:** NearestNeighbors (scikit-learn)
- **Parameters:** n_neighbors=20, metric='cosine'
- **Input:** User-movie matrix
- **Output:** Similar users
- **Performance:** Average similarity=0.157
- **Use case:** Finding similar users for recommendations

### Content-based Model
- **Algorithm:** Cosine similarity on genre features
- **Features:** One-hot encoded genres (20 columns)
- **Input:** Movie feature vectors
- **Output:** Similarity matrix (9742 × 9742)
- **Performance:** Perfect similarity (1.0) for same-genre movies
- **Use case:** Finding similar movies by content

### Hybrid Model
- **Algorithm:** Combination of KNN + Content-based
- **Weight:** alpha=0.5 (collaborative weight)
- **Input:** User ID + movie features
- **Output:** Ranked recommendations
- **Use case:** Balanced recommendations

---

## Intended Use

This system is designed to recommend movies to users based on:
- Collaborative filtering (what similar users liked)
- Content-based filtering (similar movies by genre)
- Hybrid approach combining both

---

## Training Data

- **Source:** MovieLens dataset (ml-latest-small)
- **Users:** 610
- **Movies:** 9,742
- **Ratings:** 100,836
- **Sparsity:** 1.70%

---

## Evaluation Metrics

| Model     | RMSE  | MAE   | Similarity |
|-----------|-------|-------|------------|
| **SVD**   | 0.746 | 0.530 | -          |
| **KNN**   | -     | -     | 0.157      |
| **Content** | -   | -     | 1.000      |

---

## Limitations

- Cold start problem for new users/movies
- Content-based limited to genre features only
- KNN struggles with sparse matrix (1.7% fill rate)

---

## Trade-offs

| Model          | Advantages                          | Disadvantages                          |
|----------------|-------------------------------------|----------------------------------------|
| **SVD**        | Good for rating prediction          | Less interpretable                     |
| **KNN**        | Interpretable                       | Slow for large datasets                |
| **Content-based** | Fast, no cold start for new movies | Lacks serendipity                      |
| **Hybrid**     | Best balance                        | More complex to implement              |

---

## Model Serialization

All models are saved using `joblib`:
- `svd_model.pkl`
- `knn_model.pkl`
- `content_model.pkl`
- `hybrid_model.pkl`

---

## Experiment Tracking

MLFlow is used to track all experiments:
- **Location:** `mlruns/`
- **View:** Run `mlflow ui` and open http://localhost:5000