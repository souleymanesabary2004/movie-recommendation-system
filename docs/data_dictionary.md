# Data Dictionary - Movie Recommendation System

## 📂 Data Structure

data/
│
├── raw/ # Raw CSV files (MovieLens)
│ ├── movies.csv
│ ├── ratings.csv
│ ├── tags.csv
│ └── links.csv
│
└── processed/ # Cleaned and enriched data
├── movies_clean.csv
├── movies_enriched.csv
├── genre_counts.csv
├── movie_features.csv
├── user_movie_matrix.csv
└── user_movie_matrix_norm.csv


---

## 📊 Raw Data Files

### `movies.csv`
| Column    | Type | Description                     | Example                                    |
|-----------|------|---------------------------------|--------------------------------------------|
| movieId   | int  | Unique movie ID                 | 1                                          |
| title     | str  | Movie title with year           | Toy Story (1995)                           |
| genres    | str  | Pipe-separated genres           | Adventure\|Animation\|Children\|Comedy\|Fantasy |

### `ratings.csv`
| Column    | Type  | Description                     | Example      |
|-----------|-------|---------------------------------|--------------|
| userId    | int   | Unique user ID                  | 1            |
| movieId   | int   | References movies.csv           | 1            |
| rating    | float | 0.5 to 5.0 (0.5 steps)          | 4.0          |
| timestamp | int   | Unix timestamp                  | 964982703    |

### `tags.csv`
| Column    | Type  | Description                     | Example         |
|-----------|-------|---------------------------------|-----------------|
| userId    | int   | User who created the tag        | 1               |
| movieId   | int   | Movie being tagged               | 1               |
| tag       | str   | Free-text tag                   | funny animation |
| timestamp | int   | Unix timestamp                  | 964982703       |

### `links.csv`
| Column    | Type  | Description                     |
|-----------|-------|---------------------------------|
| movieId   | int   | MovieLens movie ID              |
| imdbId    | int   | IMDB movie ID                   |
| tmdbId    | int   | TMDB movie ID                   |

---

## 📈 Dataset Statistics

| Metric                 | Value                     |
|------------------------|---------------------------|
| Total movies           | 9,742                     |
| Total ratings          | 100,836                   |
| Total users            | 610                       |
| Average rating         | 3.53                      |
| Most common genre      | Drama (5,032 movies)      |
| Most rated movie       | Forrest Gump (341 ratings)|
| Date range             | 1996-03-29 to 2018-09-24  |

---

## 🔧 Transformations (Phase 1-2-3)

| Transformation          | Description                                | Libraries          |
|-------------------------|--------------------------------------------|--------------------|
| Timestamp conversion    | Unix → datetime: `pd.to_datetime(timestamp, unit='s')` | pandas             |
| Movie year extraction   | Regex `r'\((\d{4})\)'` from title          | pandas             |
| Genre splitting         | Split pipe-separated genres with `str.split('|')` | pandas             |
| Missing value handling  | `fillna()` for NULL values                 | pandas, Spark      |
| Duplicate removal       | `dropDuplicates()` for clean data          | Spark              |

---

## 📁 Generated Files - Phase 3 (Spark ETL)

### `movies_clean.csv` (in `data/processed/`)
| Column       | Type | Description               | Example                                        |
|--------------|------|---------------------------|------------------------------------------------|
| movieId      | int  | Movie ID                  | 1                                              |
| title        | str  | Movie title               | Toy Story (1995)                               |
| genres       | str  | Cleaned genres            | Adventure\|Animation\|Children\|Comedy\|Fantasy |
| title_length | int  | Length of title string    | 16                                             |
| genre_count  | int  | Number of genres          | 5                                              |

### `user_stats.csv` (in project root)
| Column       | Type  | Description                       | Example |
|--------------|-------|-----------------------------------|---------|
| userId       | int   | Unique user ID                    | 148     |
| rating_count | int   | Number of ratings by this user    | 48      |
| avg_rating   | float | Average rating given by this user | 3.74    |
| std_rating   | float | Standard deviation of ratings     | 0.68    |
| min_rating   | float | Minimum rating given              | 1.5     |
| max_rating   | float | Maximum rating given              | 5.0     |

### `movie_stats.csv` (in project root)
| Column       | Type  | Description                       | Example |
|--------------|-------|-----------------------------------|---------|
| movieId      | int   | Unique movie ID                   | 356     |
| rating_count | int   | Number of ratings received        | 329     |
| avg_rating   | float | Average rating                    | 4.16    |
| std_rating   | float | Standard deviation of ratings     | 0.83    |
| min_rating   | float | Minimum rating received           | 0.5     |
| max_rating   | float | Maximum rating received           | 5.0     |

### `top_movies.csv` (in project root)
| Column       | Type  | Description               |
|--------------|-------|---------------------------|
| movieId      | int   | Movie ID                  |
| rating_count | int   | Number of ratings         |
| avg_rating   | float | Average rating            |
| std_rating   | float | Standard deviation        |
| min_rating   | float | Minimum rating            |
| max_rating   | float | Maximum rating            |

### `movies_enriched.csv` (in `data/processed/`)
| Column       | Type  | Description                       | Example                           |
|--------------|-------|-----------------------------------|-----------------------------------|
| movieId      | int   | Movie ID                          | 1                                 |
| title        | str   | Movie title                       | Toy Story (1995)                  |
| genres       | str   | Pipe-separated genres             | Adventure\|Animation\|Children    |
| year_str     | str   | Year extracted from title         | 1995                              |
| genre_count  | int   | Number of genres                  | 5                                 |
| rating_count | int   | Number of ratings received        | 215                               |
| avg_rating   | float | Average rating                    | 3.92                              |
| std_rating   | float | Standard deviation                | 0.83                              |
| min_rating   | float | Minimum rating                    | 0.5                               |
| max_rating   | float | Maximum rating                    | 5.0                               |

### `genre_counts.csv` (in `data/processed/`)
| Column | Type | Description                  | Example |
|--------|------|------------------------------|---------|
| genre  | str  | Genre name                   | Drama   |
| count  | int  | Number of movies in this genre | 4,361   |

---

## 📁 Generated Files - Phase 4 (Machine Learning)

### Feature Files (in `data/processed/`)

#### `movie_features.csv`
| Column(s)                        | Type  | Description                              | Source Library                           |
|----------------------------------|-------|------------------------------------------|------------------------------------------|
| movieId                          | int   | Unique movie identifier                  | -                                        |
| title                            | str   | Movie title                              | -                                        |
| year_str                         | str   | Year extracted from title                | -                                        |
| genre_count                      | int   | Number of genres for this movie          | -                                        |
| rating_count                     | int   | Total number of ratings received         | -                                        |
| avg_rating                       | float | Average rating                           | -                                        |
| std_rating                       | float | Standard deviation of ratings            | -                                        |
| (no genres listed) to Western    | int   | One-hot encoded genre columns (20 total) | `sklearn.preprocessing.MultiLabelBinarizer` |
| tag_0 to tag_49                  | float | TF-IDF features from user tags (50 total)| `sklearn.feature_extraction.text.TfidfVectorizer` |

**Shape:** (9,742 rows, 77 columns)

#### `user_movie_matrix.csv`
- **Rows:** 610 users (userId)
- **Columns:** 9,724 movies (movieId)
- **Values:** Original ratings (0.5 to 5.0)
- **Sparsity:** 1.70%

#### `user_movie_matrix_norm.csv`
- **Rows:** 610 users
- **Columns:** 9,724 movies
- **Values:** (rating - user_mean)
- **Use:** Input for collaborative filtering models

### Model Files (in project root)

| File                | Format | Description                              | Library                                      |
|---------------------|--------|------------------------------------------|----------------------------------------------|
| `svd_model.pkl`     | joblib | Trained SVD matrix factorization model   | `sklearn.decomposition.TruncatedSVD`         |
| `knn_model.pkl`     | joblib | Trained KNN collaborative filtering model| `sklearn.neighbors.NearestNeighbors`         |
| `content_model.pkl` | joblib | Content-based similarity matrix          | `sklearn.metrics.pairwise.cosine_similarity` |
| `hybrid_model.pkl`  | joblib | Hybrid model configuration               | Custom combination                           |

### Evaluation Files (in project root)

| File                           | Description                     | Contents                                      |
|--------------------------------|---------------------------------|----------------------------------------------|
| `model_evaluation_results.csv` | Model comparison                | RMSE, MAE, similarity metrics for all models |

### Experiment Tracking

| Location   | Description                                                |
|------------|------------------------------------------------------------|
| `mlruns/`  | Directory containing all MLFlow experiment data           |
| `mlflow ui`| Command to launch the MLFlow interface at http://localhost:5000 |

---

## 📊 Model Performance Summary

| Model     | RMSE  | MAE   | Similarity | Hit Rate@10 |
|-----------|-------|-------|------------|-------------|
| **SVD**   | 0.746 | 0.530 | -          | -           |
| **KNN**   | -     | -     | 0.157      | 93.4%       |
| **Content**| -    | -     | 1.000      | -           |
| **Hybrid**| -     | -     | -          | -           |

---

## 📚 Related Documentation

| Document            | Location      | Description                             |
|---------------------|---------------|-----------------------------------------|
| `model_card.md`     | `docs/`       | Detailed model information and limitations |
| `README.md`         | Root          | Project overview and quick start        |
| `notebooks/README.md`| `notebooks/`  | Notebook documentation                  |

---

## 🔧 Transformations Summary by Phase

| Phase      | Key Transformations                      | Output Files                                      |
|------------|------------------------------------------|---------------------------------------------------|
| **Phase 1-2** | Docker setup, MySQL, EDA                 | Database tables                                   |
| **Phase 3**   | Spark ETL, cleaning, aggregations        | `user_stats.csv`, `movie_stats.csv`, `movies_enriched.csv` |
| **Phase 4**   | Feature engineering, ML models, evaluation | `movie_features.csv`, model `.pkl` files          |

---

## 📝 Notes

- All CSV files can be loaded with `pandas.read_csv()`
- Model files can be loaded with `joblib.load()`
- MLFlow experiments can be viewed with `mlflow ui`
- The feature matrix `movie_features.csv` is ready for any scikit-learn model