\# Movie Recommendation System - Architecture



\## System Overview



This system follows a \*\*layered data architecture\*\* with 3 main layers:



\- \*\*Bronze Layer (Raw Data)\*\* : Original CSV files from MovieLens

\- \*\*Silver Layer (Cleaned Data)\*\* : Data after validation and cleaning

\- \*\*Gold Layer (ML-Ready Data)\*\* : Feature-engineered data ready for models



The application uses a \*\*client-server architecture\*\*:

\- \*\*Streamlit Dashboard\*\* : User interface

\- \*\*FastAPI\*\* : REST API serving ML models

\- \*\*MySQL\*\* : Persistent data storage



\## Technology Stack



| Component              | Technology        | Version | Purpose                            |

|------------------------|-------------------|---------|------------------------------------|

| Language               | Python            | 3.10    | Main programming language          |

| Database               | MySQL             | 8.0     | Data storage                       |

| Containerization       | Docker            | 24.0    | Isolation and deployment           |

| ETL Level 1            | Pandas            | 2.3.3   | Prototyping and small volumes      |

| ETL Level 2            | PySpark           | 4.1.1   | Distributed processing             |

| Machine Learning       | scikit-learn      | 1.7.2   | ML models                          |

| Experiment Tracking    | MLflow            | 3.10.0  | Experiment tracking                |

| API                    | FastAPI           | 0.135.1 | Model serving                      |

| Dashboard              | Streamlit         | 1.55.0  | User interface                     |

| Testing                | pytest            | 9.0.2   | Automated testing                  |

| CI/CD                  | GitHub Actions    | -       | Continuous integration             |



\## Data Flow



\### Layer 1: Bronze (Raw Data)



| Source        | Location           | Format | Description                    |

|---------------|--------------------|--------|--------------------------------|

| movies.csv    | `data/raw/`        | CSV    | Movie catalog (ID, title, genres) |

| ratings.csv   | `data/raw/`        | CSV    | User ratings (user ID, movie ID, rating, timestamp) |

| tags.csv      | `data/raw/`        | CSV    | User-generated tags            |

| links.csv     | `data/raw/`        | CSV    | External links (IMDB, TMDB)    |



\### Layer 2: Silver (Cleaned Data)



| Process                | Tool   | Description                              |

|------------------------|--------|------------------------------------------|

| Schema validation      | Spark  | Verify column names and types            |

| NULL handling          | Spark  | Replace or remove missing values         |

| Deduplication          | Spark  | Remove duplicate records                 |

| Type conversion        | Spark  | Convert timestamps to dates              |

| Year extraction        | Spark  | Extract year from movie titles           |



\### Layer 3: Gold (ML-Ready Data)



| Feature                | Description                              |

|------------------------|------------------------------------------|

| Normalization          | Center ratings by user mean              |

| One-hot encoding       | Convert genres to binary columns (20 genres) |

| TF-IDF                 | Convert tags to 50-dimensional vectors   |

| User-movie matrix      | 610 users × 9724 movies (1.7% fill rate) |



\## Database Schema



\### Table `movies`



| Column   | Type   | Null | Description                            |

|----------|--------|------|----------------------------------------|

| movieId  | bigint | YES  | Unique movie identifier                |

| title    | text   | YES  | Movie title (with year)                |

| genres   | text   | YES  | Pipe-separated genres (`|`)            |

| year     | double | YES  | Year extracted from title              |



\### Table `ratings`



| Column    | Type   | Null | Description                            |

|-----------|--------|------|----------------------------------------|

| userId    | bigint | YES  | Unique user identifier                 |

| movieId   | bigint | YES  | Rated movie identifier                 |

| rating    | double | YES  | Rating from 0.5 to 5.0                 |

| timestamp | bigint | YES  | Unix timestamp of the rating           |



\## System Components



\### 1. ETL Pipeline



| Step         | Tool   | Script                          |

|--------------|--------|---------------------------------|

| Ingestion    | Spark  | `src/ingestion/ingest\_\*.py`     |

| Cleaning     | Spark  | `src/processing/clean\_\*.py`     |

| Transformation| Spark  | `src/processing/transform\_\*.py` |

| Orchestration| Python | `run\_pipeline.py`               |



\### 2. MySQL Database



| Property          | Value                                |

|--------------------|--------------------------------------|

| Container          | Docker with persistent volume        |

| Internal Port      | 3306                                 |

| External Port      | 2004                                 |

| Tables             | movies, ratings                       |

| Security           | `.env` for credentials                |



\### 3. ML Models



| Model         | Type                         | Performance               |

|---------------|------------------------------|---------------------------|

| KNN           | Collaborative filtering      | Hit Rate@10: 93.4%        |

| SVD/ALS       | Matrix factorization         | RMSE: 0.746               |

| Content-based | Genre similarity             | Cosine similarity: 1.0    |

| Hybrid        | Combined approach            | NDCG@10: 0.97             |



\### 4. FastAPI Endpoints



| Endpoint                          | Method | Description                        |

|-----------------------------------|--------|------------------------------------|

| `/recommendations/{user\_id}`      | GET    | Get recommendations for a user     |

| `/movies/{movie\_id}/stats`        | GET    | Get movie statistics               |

| `/feedback`                       | POST   | Submit user feedback               |

| `/sentiment`                      | POST   | Analyze text sentiment             |

| `/health`                         | GET    | API health check                   |



\### 5. Streamlit Dashboard



| Page               | Description                              |

|--------------------|------------------------------------------|

| Recommendations    | Personalized movie recommendations       |

| Statistics         | Movie statistics and distributions       |

| Feedback           | Submit and view user feedback            |

| Sentiment          | Analyze text sentiment                   |



\### 6. GitHub Actions CI/CD



| Property          | Value                                |

|--------------------|--------------------------------------|

| Runner             | ubuntu-latest                        |

| Trigger            | push to main, develop                |

| Tests              | 41 tests executed                    |

| Database           | MySQL container for testing          |



\## Technical Decisions



| Choice                     | Reason                                                               |

|----------------------------|----------------------------------------------------------------------|

| Python 3.10                | Best compatibility with all required libraries                      |

| MySQL                      | Simple, structured data, no need for NoSQL                          |

| Spark + Pandas             | Pandas for quick prototyping, Spark for scalability                 |

| FastAPI                    | High performance, automatic Swagger documentation                   |

| Streamlit                  | Extremely fast development, no frontend code needed                 |

| Docker                     | Reproducibility, easy deployment, isolation                         |

| GitHub Actions             | Free, GitHub-integrated, easy to configure                          |

| scikit-learn               | Uniform API, wide range of algorithms                               |

| MLflow                     | Experiment tracking, model versioning                               |



\## Security Measures



| Measure                         | Description                                              |

|---------------------------------|----------------------------------------------------------|

| `.env` for secrets              | Passwords excluded from version control                  |

| `.gitignore`                    | Protects sensitive files                                 |

| Custom port (2004)              | Avoids conflicts with local MySQL installations          |

| Docker container isolation      | Network isolation between services                       |

| GitHub tokens                   | Secure authentication for pushes                         |

| python-dotenv                   | Secure environment variable loading                      |



