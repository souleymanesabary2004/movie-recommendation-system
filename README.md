[![CI - Automated Tests](https://github.com/souleymanesabary2004/movie-recommendation-system/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/souleymanesabary2004/movie-recommendation-system/actions/workflows/ci.yml)

## 📹 Video Demo
- [Full playlist]: https://studio.youtube.com/channel/UCZGYwTpSYxFAuXcNEE-U4Jg/content/playlists?filter=%5B%5D&sort=%7B%22columnType%22%3A%22lastTimeUpdated%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D

- [Project presentation](https://youtu.be/TA62gkSfDuU)

- [Live demo](https://youtu.be/-w4UCkESmNY)

# 🎬 Movie Recommendation System


An end‑to‑end **Big Data & Machine Learning** project that recommends movies to users based on their preferences.
  
**Start date:** 01 January 2026 · **Personal project**


[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://mysql.com)
[![Docker](https://img.shields.io/badge/Docker-24.0-blue.svg)](https://docker.com)
[![Spark](https://img.shields.io/badge/Spark-4.1.1-red.svg)](https://spark.apache.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 **Overview**

This system processes **100,000+ movie ratings** to provide personalized recommendations using multiple approaches:

- **Data Engineering**: Complete ETL pipelines with Pandas (Level 1) and Spark (Level 2)
- **Machine Learning**: 4 models (Collaborative filtering, Content-based, Hybrid, ALS/SVD)
- **Deployment**: REST API with FastAPI and interactive dashboard with Streamlit
- **Infrastructure**: Fully containerized with Docker

The project follows a **professional data architecture** with Bronze/Silver/Gold layers and includes comprehensive testing and monitoring.

---

## 🏗️ **Architecture**

```text
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐
│   Raw Data  │ -> │ETL with(L1/L2)->  │    MySQL     │ -> │API/Dashboard│
│    (CSV)    │    │ Pandas/Spark │    │ (Gold Layer) │    │FastAPI(Rest)│
└─────────────┘    └──────────────┘    └──────────────┘    └─────────────┘
                                                                     │
                                                                     ▼
                                                                ┌─────────────────┐
                                                                │ 4 ML Models      
                                                                │ - KNN           │
                                                                │ - ALS/SVD       │
                                                                │ - Content-based │
                                                                │ - Hybrid        │
                                                                └─────────────────┘

### Technology Stack

| Component            | Technology (Version)                          |
|----------------------|-----------------------------------------------|
| Language             | Python 3.10                                   |
| Database             | MySQL 8.0 (Dockerized)                        |
| ETL (Level 1)        | Pandas 2.3.3 · NumPy · SQLAlchemy 2.0.46      |
| ETL (Level 2)        | Apache Spark (PySpark) 4.1.1                   |
| Machine Learning     | scikit‑learn 1.7.2 · Joblib                    |
| Experiment Tracking  | MLflow 3.10.0                                  |
| Data Analysis        | Jupyter Notebook · Matplotlib · Seaborn        |
| API                  | FastAPI 0.135.1 · Uvicorn 0.41.0               |
| Dashboard            | Streamlit 1.55.0                               |
| Infrastructure       | Docker 24.0 · Docker Compose                   |
| IDE                  | Visual Studio Code                             |
| Version Control      | Git · GitHub                                   |
| Dependencies         | See `requirements.txt`                         |


Key Python Libraries
scikit‑learn (TruncatedSVD/ALS, NearestNeighbors, metrics, preprocessing) · pandas · numpy · matplotlib · seaborn · mlflow · joblib · pyspark · sqlalchemy · mysql‑connector‑python · fastapi · uvicorn · streamlit · jupyter

📂 Project Structure

movie-recommendation-system/
│
├── src/
│   ├── __init__.py
│   ├── init_db.py                     # Database initialization
│   ├── etl_pipeline.py                # Pandas ETL (Level 1)
│   ├── quality_checks.py              # Data validation
│   │
│   ├── ingestion/                     # Spark ingestion
│   │   ├── __init__.py
│   │   ├── ingest_movies.py
│   │   └── ingest_ratings.py
│   │
│   ├── processing/                    # Spark processing
│   │   ├── __init__.py
│   │   ├── clean_movies.py
│   │   ├── clean_ratings.py
│   │   ├── transform_movies.py
│   │   └── transform_ratings.py
│   │
│   ├── features/                      # Feature engineering
│   │   ├── __init__.py
│   │   └── build_features.py
│   │
│   ├── models/                        # ML models training + inference
│   │   ├── __init__.py
│   │   ├── train_als.py               # ALS/SVD model
│   │   ├── train_knn.py               # KNN model
│   │   ├── train_content.py           # Content-based model
│   │   ├── train_hybrid.py            # Hybrid model
│   │   ├── evaluate.py                # Model evaluation
│   │   └── predict.py                 # Prediction API
│   │
│   ├── api/                           # FastAPI backend
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── endpoints.py
│   │   ├── schemas.py
│   │   └── dependencies.py
│   │
│   └── dashboard/                     # Streamlit dashboard
│       ├── __init__.py
│       ├── app.py
│       ├── components.py
│       └── pages.py
│
├── notebooks/                         # Jupyter notebooks
│   ├── 01_exploration_pandas.ipynb
│   └── 02_feature_engineering.ipynb
│
├── data/                              
│   ├── raw/                            # Raw CSV files
│   │   ├── movies.csv
│   │   ├── ratings.csv
│   │   ├── tags.csv
│   │   └── links.csv
│   │
│   └── processed/                      # Cleaned & engineered datasets
│       ├── movies_clean.csv
│       ├── movies_enriched.csv
│       ├── genre_counts.csv
│       ├── movie_features.csv
│       ├── user_movie_matrix.csv
│       └── user_movie_matrix_norm.csv
│
├── docker/                             # Docker build files
│   ├── api/
│   │   └── Dockerfile
│   └── dashboard/
│       └── Dockerfile
│
├── tests/                              # Test suite
│   ├── __init__.py
│   └── test_smoke.py
│
├── docs/                               # FULL updated documentation
│   ├── architecture.md
│   ├── api.md
│   ├── data_dictionary.md
│   ├── contributing.md
│   ├── security.md
│   └── deployment.md
│
├── models/                             # Saved ML models
│   ├── svd_model.pkl
│   ├── knn_model.pkl
│   ├── content_model.pkl
│   └── hybrid_model.pkl
│
├── mlruns/                             # MLflow experiments
│
├── run_pipeline.py                     # ETL Level 2 Orchestrator
├── docker-compose.yml                  # Core infrastructure (API + UI only)
├── .env.example                        # Environment variable template
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md

Notes

data/raw/ and heavy artifacts are ignored via .gitignore.
Docker Compose wires MySQL + API + Dashboard for local runs.


Phase 0: Preparation — ✅ Tools, venv, repo conventions, dataset review( via MoviesLens)

Phase 1-3: Data Engineering (Complete)
✅ Docker container with MySQL and persistent volume

✅ Database schema (movies, ratings tables)

✅ Secure credentials with .env

✅ Data exploration in Jupyter

✅ ETL with Pandas (Level 1)

✅ ETL with Spark (Level 2)

✅ Ingestion scripts (movies, ratings)

✅ Cleaning scripts (movies, ratings)

✅ Transformation scripts (features extraction)

✅ Pipeline orchestrator (run_pipeline.py)

✅ Quality checks automation

Phase 4: Machine Learning (Complete)
✅ Feature Engineering

✅ User features (activity, preferences)

✅ Movie features (genres, popularity, ratings)

✅ Text features (TF-IDF on tags)

✅ 4 Models Implemented

✅ KNN (Collaborative filtering)

✅ ALS/SVD (Matrix factorization)

✅ Content-based (genre similarity)

✅ Hybrid (combining approaches)

✅ Model Evaluation

✅ Precision / Recall

✅ RMSE / MAE (2.53 / 2.18)

✅ Hit Rate@10 (93.4%)

✅ NDCG@10 (0.97)

✅ MLFlow Tracking

✅ Experiment logging (parameters + metrics)

✅ Model artifacts saved

✅ Environment tracked

Phase 5: Deployment (Complete)
✅ FastAPI REST API

✅ Endpoints: /recommendations, /movies, /feedback, /sentiment

✅ Health checks and monitoring

✅ Automatic OpenAPI documentation

✅ Streamlit Dashboard

✅ 4 pages: Recommendations, Statistics, Feedback, Sentiment

✅ Real-time API communication

✅ User-friendly interface

✅ Docker Containerization

✅ Multi-service architecture

✅ Network configuration

✅ Volume management

✅ One-command deployment

### Generated Files

| File                  | Location         | Description                    | Records        |
|----------------------|------------------|--------------------------------|----------------|
| movie_features.csv   | data/processed/  | Movies with engineered features | 9,742 × 77     |
| user_movie_matrix.csv| data/processed/  | Users × movies matrix          | 610 × 9,724    |
| user_stats.csv       | root             | User statistics                | 610            |
| movie_stats.csv      | root             | Movie statistics               | 9,724          |
| svd_model.pkl        | models/          | ALS/SVD model                  | —              |
| knn_model.pkl        | models/          | KNN model                      | —              |
| content_model.pkl    | models/          | Content‑based model            | —              |
| hybrid_model.pkl     | models/          | Hybrid model                   | —              |



## Phase 6: Testing & CI/CD (✅ COMPLETE)


|        Test Type                       | Count  | Status |
|----------------------------------------|--------|--------|
| Data Tests (integrity, schema, values) | 16     | ✅ PASSED |
| Unit Tests (ETL, models)               | 9      | ✅ PASSED |
| Integration Tests (database, pipeline) | 13     | ✅ PASSED |
| Performance Tests (optional)           | 3      | ✅ PASSED |
| **TOTAL**                              | **41** | **✅ ALL PASSED** |

### Test Coverage

✅ **Data Integrity** : Files exist, not empty
✅ **Data Schema** : Correct columns (movieId, title, genres, userId, rating, timestamp)
✅ **Data Values** : Ratings between 0.5-5.0, no negative values, no empty titles
✅ **ETL Functions** : Timestamp conversion, rating normalization, year extraction, genre split
✅ **Model Functions** : User normalization, cosine similarity, hit rate, precision/recall
✅ **Database** : MySQL connection, table schemas, foreign key integrity
✅ **Pipeline** : Complete ETL workflow, data quality checks

### CI/CD Pipeline (GitHub Actions)

✅ **Automated on every push** : All tests run automatically
✅ **Ubuntu runner** with MySQL container
✅ **Data download** : MovieLens dataset fetched automatically
✅ **Test execution** : 41 tests in ~4 seconds
✅ **Status badge** : [![CI - Automated Tests](https://github.com/souleymanesabary2004/movie-recommendation-system/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/souleymanesabary2004/movie-recommendation-system/actions/workflows/ci.yml)

### Monitoring

✅ **Logging configured** : `src/utils/logger.py`
✅ **Three loggers** : app_logger, ml_logger, etl_logger
✅ **Log files** : `logs/` directory with daily rotation
✅ **Console output** : Real-time logging during execution

## Phase 7: Documentation (✅ IN PROGRESS)

### Documentation Files

| File                      | Description                           | Status |
|---------------------------|---------------------------------------|--------|
| `README.md`               | Project overview, installation, usage | ✅ DONE |
| `docs/architecture.md`    | System architecture diagram           | ✅ DONE |
| `docs/api.md`             | API endpoints documentation           | ✅ DONE |
| `docs/data_dictionary.md` | Data schema and fields description    | ✅ DONE |
| `docs/deployment.md`      | Deployment guide                      | ✅ DONE |
| `docs/contributing.md`    | Contribution guidelines               | ✅ DONE |
| `docs/security.md`        | Security best practices               | ✅ DONE |

### Documentation Highlights

✅ **Professional structure** : Clear sections for all audiences
✅ **Badges** : CI status, Python version, license
✅ **Installation guide** : Step-by-step for new users
✅ **API examples** : Curl commands and JSON responses
✅ **Model comparison** : Performance metrics table
✅ **Test commands** : How to run tests locally

## 📊 Project Completion Status

| Phase   | Description      | Status |
|---------|------------------|--------|
| Phase 0 | Preparation      | ✅ DONE |
| Phase 1 | Infrastructure   | ✅ DONE |
| Phase 2 | Data Collection  | ✅ DONE |
| Phase 3 | Data Engineering | ✅ DONE |
| Phase 4 | Machine Learning | ✅ DONE |
| Phase 5 | Deployment       | ✅ DONE |
| Phase 6 | Testing & CI/CD  | ✅ DONE |
| Phase 7 | Documentation    | ✅ DONE |
| Phase 8 | Cloud Deployment | ⏳ PLANNED |


📊 Dataset: MovieLens

The project uses the MovieLens dataset (ml-latest-small).


### Statistics

| Metric              | Value                     | Description                               |
|---------------------|---------------------------|-------------------------------------------|
| Movies              | 9,742                     | Unique movies                             |
| Ratings             | 100,836                   | Total ratings                             |
| Users               | 610                       | Unique users                              |
| Rating scale        | 0.5 – 5.0                 | 0.5 increments                            |
| Average rating      | 3.53                      | Global average                            |
| Most common genre   | Drama                     | 4,361 movies                              |
| Date range          | 1996‑03‑29 → 2018‑09‑24   | 22 years                                   |
| Data Quality        | 100% clean              | No missing values, no duplicates, valid ranges |


Data Quality (100% Clean)

✅ No missing values

✅ No duplicates

✅ All ratings within valid range

✅ All foreign keys validated


🚀 Quick Start Guide

Prerequisites
Python 3.10+

Docker

Git

8GB+ RAM recommended

Installation


# 1. Clone the repository
git clone https://github.com/souleymanesabary2004/movie-recommendation-system.git
cd movie-recommendation-system


# 2. Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
# source .venv/bin/activate


# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your MySQL password


# 5. Start MySQL container
docker run --name mysql-movies \
  -e MYSQL_ROOT_PASSWORD=your_password \
  -v mysql_data:/var/lib/mysql \
  -p 2004:3306 \
  -d mysql:8.0


# 6. Initialize database
python src/init_db.py


# 7. Run complete ETL pipeline
python run_pipeline.py


# 8. Train ML models
python src/models/train_als.py
python src/models/train_knn.py
python src/models/train_content.py
python src/models/train_hybrid.py


# 9. Run quality checks
python src/quality_checks.py

# 10. Launch the full application with Docker Compose
docker-compose up


Access the Application


Service	URL	Description
API	http://localhost:8000	FastAPI backend
API Docs	http://localhost:8000/docs	Interactive API documentation
Dashboard	http://localhost:8501	Streamlit frontend
MySQL	localhost:2004	Database (via any MySQL client)



### Models Comparison

| Model         | RMSE  | Hit Rate@10 | NDCG@10 | Strengths                  | Weaknesses             |
|---------------|-------|-------------|---------|----------------------------|------------------------|
| KNN           | —     | 0%          | —       | Simple, interpretable      | Poor on sparse data    |
| ALS/SVD       | 2.53  | 93.4%       | 0.97    | Excellent recommendations  | High memory usage      |
| Content-based | —     | —           | —       | No cold start              | Limited diversity      |
| Hybrid        | —     | —           | —       | Best of both worlds        | Complex to tune        |


Feature Engineering

User features: rating_count, avg_rating, std_rating, min_rating, max_rating

Movie features: year, genre_count, rating_count, avg_rating, std_rating

Text features: TF-IDF (50 dimensions) on user tags

Interaction features: User-movie matrix (610 × 9724)



### Evaluation Metrics Explained

| Metric      | Formula                     | Interpretation                         | Our Results  |
|-------------|-----------------------------|-----------------------------------------|-------------|
| RMSE        | √(Σ(ŷ − y)² / n)            | Average prediction error (stars)        | 2.53        |
| MAE         | Σ |ŷ − y| / n               | Average absolute error (stars)          | 2.18        |
| Hit Rate    | (users with hit) / total    | % of users receiving a good top‑10 rec   | 93.4%       |
| NDCG        | DCG / IDCG                  | Ranking quality (1.0 = perfect)         | 0.97         |


📈 Sample Results

### Top 5 Most Rated Movies

| Rank | Movie ID | Title                              | Ratings | Avg Rating |
|------|----------|------------------------------------|---------|------------|
| 1    | 356      | Forrest Gump (1994)                | 329     | 4.16       |
| 2    | 318      | Shawshank Redemption, The (1994)   | 317     | 4.43       |
| 3    | 296      | Pulp Fiction (1994)                | 307     | 4.20       |
| 4    | 593      | Silence of the Lambs, The (1991)   | 279     | 4.16       |
| 5    | 2571     | Matrix, The (1999)                 | 278     | 4.19       |

### Genre Distribution

| Genre    | Count | Percentage |
|----------|-------|------------|
| Drama    | 4,361 | 44.8%      |
| Comedy   | 3,756 | 38.6%      |
| Thriller | 1,894 | 19.5%      |
| Action   | 1,828 | 18.8%      |
| Romance  | 1,596 | 16.4%      |



## Docker Services

The application runs as 3 interconnected Docker containers:

```yaml
services:
  mysql:      # Database (manual management)
  api:        # FastAPI backend
  dashboard:  # Streamlit frontend
Useful Commands


```markdown
## Useful Commands

```bash
# Start all services
docker-compose up

# Start only API and dashboard (MySQL manual)
docker-compose up api dashboard

# Stop all services
docker-compose down

# Rebuild after changes
docker-compose build

# View logs
docker-compose logs -f

# Access container shell
docker exec -it movie-api bash

### Test Commands

```bash
# Run all tests (excluding performance)
pytest tests/ -v --ignore=tests/performance/

# Run specific test categories
pytest tests/data/ -v      # Data quality tests
pytest tests/unit/ -v      # Unit tests
pytest tests/integration/ -v  # Integration tests

# Run with coverage
pytest tests/ -v --cov=. --cov-report=term

📚 Documentation

Data Dictionary - Complete data documentation

API Documentation - Interactive API docs (when running)

Notebooks Guide - Exploration notebooks overview


🧪 Testing & Quality (Phase 6 - ✅ COMPLETE)

| Test Type | Count | Status |
|-----------|-------|--------|
| Data Tests | 16 | ✅ PASSED |
| Unit Tests | 9 | ✅ PASSED |
| Integration Tests | 13 | ✅ PASSED |
| Performance Tests | 3 | ⏭️ Optional |
| **TOTAL** | **41** | **✅ ALL PASSED** |

**CI/CD Pipeline:** ✅ GitHub Actions active (all tests run on every push)

**Monitoring:** ✅ Logs configured (`src/utils/logger.py`)



🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

Please ensure your code follows the project's style and includes tests.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👤 Author
Souleymane Soumahoro
https://www.linkedin.com/in/souleymane-soumahoro-b980b438b


https://github.com/souleymanesabary2004

https://github.com/souleymanesabary2004/movie-recommendation-system

🙏 Acknowledgments
GroupLens Research for the MovieLens dataset

Apache Spark for distributed processing

scikit-learn for ML algorithms

FastAPI for the amazing API framework

Streamlit for easy dashboard creation

All open-source contributors

⭐ Support
If you find this project useful, please give it a star on GitHub! ⭐