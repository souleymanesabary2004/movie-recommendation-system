# Data Dictionary – Movie Recommendation System

This document describes the raw dataset, processed files, engineered features, and model artifacts used in the project.

---

## Data Structure

data/
│
├── raw/ # Raw CSV files (MovieLens)
│ ├── movies.csv
│ ├── ratings.csv
│ ├── tags.csv
│ └── links.csv
│
└── processed/ # Cleaned & enriched data
├── movies_clean.csv
├── movies_enriched.csv
├── genre_counts.csv
├── movie_features.csv
├── user_movie_matrix.csv
└── user_movie_matrix_norm.csv



---

## Raw Data Files

### movies.csv

| Column  | Type   | Description                      | Example                              |
|---------|--------|----------------------------------|--------------------------------------|
| movieId | int    | Unique movie identifier          | 1                                    |
| title   | str    | Movie title (with year)          | Toy Story (1995)                     |
| genres  | str    | Pipe-separated genres            | Adventure|Animation|Children|Comedy    |

### ratings.csv

| Column    | Type   | Description                      | Example      |
|-----------|--------|----------------------------------|--------------|
| userId    | int    | User identifier                  | 1            |
| movieId   | int    | Reference to movies.csv          | 1            |
| rating    | float  | Rating from 0.5 to 5.0           | 4.0          |
| timestamp | int    | Unix timestamp                   | 964982703    |

### tags.csv

| Column    | Type   | Description                      | Example         |
|-----------|--------|----------------------------------|-----------------|
| userId    | int    | User who created the tag         | 1               |
| movieId   | int    | Movie being tagged               | 1               |
| tag       | str    | Free-text tag                    | funny animation |
| timestamp | int    | Unix timestamp                   | 964982703       |

### links.csv

| Column  | Type   | Description                      |
|---------|--------|----------------------------------|
| movieId | int    | MovieLens ID                     |
| imdbId  | int    | IMDb ID                          |
| tmdbId  | int    | TMDB ID                          |

---

## Core Transformations

| Transformation      | Description                         | Tool           |
|---------------------|-------------------------------------|----------------|
| Timestamp conversion| Unix to datetime                    | pandas         |
| Year extraction     | From title using regex              | pandas         |
| Genre parsing       | Split pipe-separated genres         | pandas         |
| Missing values      | fillna / typed defaults             | pandas, Spark  |
| Duplicate removal   | drop_duplicates / dropDuplicates    | pandas, Spark  |

---

## Processed Files

### movies_clean.csv

| Column       | Type   | Description                          |
|--------------|--------|--------------------------------------|
| movieId      | int    | Movie identifier                     |
| title        | str    | Movie title                          |
| genres       | str    | Cleaned genres                       |
| title_length | int    | Title character length               |
| genre_count  | int    | Number of genres                     |

### movies_enriched.csv

| Column       | Type   | Description                          |
|--------------|--------|--------------------------------------|
| movieId      | int    | Movie identifier                     |
| title        | str    | Movie title                          |
| genres       | str    | Pipe-separated genres                |
| year_str     | str    | Extracted year                       |
| genre_count  | int    | Number of genres                     |
| rating_count | int    | Number of ratings received           |
| avg_rating   | float  | Average rating                       |
| std_rating   | float  | Rating standard deviation            |
| min_rating   | float  | Minimum rating                       |
| max_rating   | float  | Maximum rating                       |

### user_stats.csv

| Column       | Type   | Description                          |
|--------------|--------|--------------------------------------|
| userId       | int    | User identifier                      |
| rating_count | int    | Number of ratings                    |
| avg_rating   | float  | Average rating                       |
| std_rating   | float  | Rating standard deviation            |
| min_rating   | float  | Minimum rating                       |
| max_rating   | float  | Maximum rating                       |

### movie_stats.csv

| Column       | Type   | Description                          |
|--------------|--------|--------------------------------------|
| movieId      | int    | Movie identifier                     |
| rating_count | int    | Number of ratings                    |
| avg_rating   | float  | Average rating                       |
| std_rating   | float  | Rating standard deviation            |
| min_rating   | float  | Minimum rating                       |
| max_rating   | float  | Maximum rating                       |

### genre_counts.csv

| Column | Type   | Description                          |
|--------|--------|--------------------------------------|
| genre  | str    | Genre name                           |
| count  | int    | Number of movies in genre            |

---

## ML Features & Matrices

### movie_features.csv

| Column(s)                    | Type    | Description                          |
|------------------------------|---------|--------------------------------------|
| movieId                      | int     | Movie identifier                     |
| title                        | str     | Movie title                          |
| year_str                     | str     | Year extracted                       |
| genre_count                  | int     | Number of genres                     |
| rating_count                 | int     | Number of ratings                    |
| avg_rating                   | float   | Average rating                       |
| std_rating                   | float   | Standard deviation                   |
| genre_Action ... genre_Western| int     | One-hot encoded genres (20 columns)  |
| tag_0 ... tag_49             | float   | TF-IDF features (50 columns)         |

**Shape:** 9,742 rows × 77 columns

### user_movie_matrix.csv

- **Rows:** 610 users
- **Columns:** 9,724 movies
- **Values:** Original ratings (sparse, 1.7% fill rate)

### user_movie_matrix_norm.csv

- **Rows:** 610 users
- **Columns:** 9,724 movies
- **Values:** Normalized ratings (rating - user_mean)
- **Use:** Input for collaborative filtering (ALS/SVD, KNN)

---

## Database Schema (MySQL Gold Layer)

### movies table

| Column   | Type        | Description                          |
|----------|-------------|--------------------------------------|
| movieId  | INT         | Primary key                          |
| title    | VARCHAR     | Movie title                          |
| year     | INT         | Year (nullable)                      |
| genres   | VARCHAR     | Pipe-separated genres (nullable)     |

### ratings table

| Column    | Type        | Description                          |
|-----------|-------------|--------------------------------------|
| userId    | INT         | User identifier                      |
| movieId   | INT         | Foreign key to movies                |
| rating    | DECIMAL(2,1)| Rating from 0.5 to 5.0               |
| timestamp | BIGINT      | Unix timestamp                       |

---

## Model Artifacts

### Saved Models

| File                | Format  | Description                              |
|---------------------|---------|------------------------------------------|
| svd_model.pkl       | joblib  | SVD / Matrix factorization model         |
| knn_model.pkl       | joblib  | KNN collaborative filtering model        |
| content_model.pkl   | joblib  | Content-based similarity model           |
| hybrid_model.pkl    | joblib  | Combined model configuration             |

### Evaluation Results

| File                           | Description                          |
|--------------------------------|--------------------------------------|
| model_evaluation_results.csv   | RMSE, MAE, similarity scores         |

---

## Dataset Statistics (Global)

| Metric              | Value                               |
|---------------------|-------------------------------------|
| Total movies        | 9,742                               |
| Total ratings       | 100,836                             |
| Total users         | 610                                 |
| Average rating      | 3.53                                |
| Most common genre   | Drama (4,361 movies)                |
| Date range          | 1996-03-29 to 2018-09-24            |

---

## Notes

- All CSVs load with `pandas.read_csv()`
- Models load with `joblib.load()`
- `movie_features.csv` is ready for any scikit-learn model
- Raw data files are excluded from Git (`.gitignore`)