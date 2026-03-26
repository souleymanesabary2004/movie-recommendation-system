

# System Architecture – Movie Recommendation System

This document provides a full architecture overview of the Movie Recommendation System, including data flow, ETL processes, machine learning components, serving layers, and deployment infrastructure.

---

## 1. High-Level Architecture

```text
              ┌──────────────────────┐
              │    Raw Data (CSV)    │
              └───────────┬──────────┘
                          │
              ┌───────────▼──────────┐
              │ ETL Level 1 (Pandas)  │
              │  Cleaning & Wrangling │
              └───────────┬──────────┘
                          │
              ┌───────────▼──────────┐
              │ ETL Level 2 (Spark)   │
              │ Distributed Processing│
              └───────────┬──────────┘
                          │
              ┌───────────▼──────────┐
              │   MySQL Warehouse     │
              │      (Gold Layer)     │
              └───────────┬──────────┘
                          │
      ┌───────────────────┴────────────────────┐
      │                                        │
      ▼                                        ▼
┌───────────────┐                      ┌────────────────┐
│ FastAPI (REST)│                      │ Streamlit (UI) │
└───────┬───────┘                      └───────┬────────┘
        │                                         │
        └─────────────────────────────────────────┘
                          │
                          ▼
             ┌───────────────────────────────┐
             │   Machine Learning Models      │
             │ ALS/SVD · KNN · Content-based  │
             │            Hybrid              │
             └───────────────────────────────┘


             ## 2. Data Flow Overview

| Stage           | Description                                                                        |
|-----------------|------------------------------------------------------------------------------------|
| Raw Data        | Original MovieLens CSV files stored under `data/raw/`                              |
| ETL Level 1     | Pandas performs cleaning, formatting, validation, early transformation             |
| ETL Level 2     | Spark ingests data, cleans at scale, and performs distributed joins & aggregations |
| Warehouse Layer | MySQL stores Gold Layer tables (movies, ratings, stats)                            |
| Feature Layer   | Engineered CSVs (movie_features, user/movie matrices)                              |
| ML Layer        | ALS/SVD, KNN, Content-based, and Hybrid models                                     |
| API Layer       | FastAPI exposes recommendation and analytics endpoints                             |
| UI Layer        | Streamlit renders user-facing dashboard                                            |
| Infra Layer     | Docker Compose orchestrates all application services                               |


3. ETL Layer
Level 1 — Pandas
Tasks:

Early data inspection
Basic cleaning (NaN, formatting)
Light transformations
Small-scale features

Level 2 — Spark
Tasks:

Distributed ingestion
Cleaning & validation at scale
Joining multiple datasets
Generating aggregates
Writing to MySQL (Gold Layer)


##4. Tables Stored (Gold Layer)

| Table         | Description                                       |
|---------------|---------------------------------------------------|
| movies        | Metadata of all movies (title, year, genres)      |
| ratings       | User → movie ratings (0.5 to 5.0 scale)           |
| movie_stats   | Aggregated statistics for each movie              |
| user_stats    | Aggregated statistics for each user               |

This is the Gold Layer, clean and analytics‑ready.

5. Feature Engineering Layer
Outputs include:

One‑hot encoded genre vectors
Statistical features (counts, averages, std)
TF‑IDF vectors (tags)
Sparse user–movie interaction matrix
Normalized interaction matrix

Main files:

movie_features.csv
user_movie_matrix.csv
user_movie_matrix_norm.csv


6. Machine Learning Layer

## Models Implemented

| Model         | Type                     | Description                                  |
|---------------|---------------------------|----------------------------------------------|
| ALS/SVD       | Matrix factorization      | Learns latent factors from user–item matrix  |
| KNN           | Collaborative filtering   | Uses nearest neighbors for recommendations   |
| Content-based | Feature similarity        | Recommends movies based on metadata vectors  |
| Hybrid        | Combined approach         | Aggregates multiple model predictions        |

MLflow tracks:

metrics (RMSE, MAE, NDCG, HitRate@10)
parameters
serialized models (*.pkl)
environment (conda, dependencies)


7. Deployment Architecture

Docker Compose Orchestration
 ┌─────────────────────────────────────────────────────┐
 │                                                     │
 │   ┌──────────────┐       ┌──────────────────────┐   │
 │   │   FastAPI     │◀────▶│     Streamlit UI     │   │
 │   │ (Backend)     │       │  (Dashboard)         │   │
 │   └───────┬───────┘       └──────────┬───────────┘   │
 │           │                            │            │
 │           ▼                            ▼            │
 │     ┌──────────┐                ┌──────────────┐    │
 │     │  Models  │                │    MLflow     │    │
 │     └──────────┘                └──────────────┘    │
 │           ▲                            ▲            │
 │           │                            │            │
 │     ┌──────────────┐                   │            │
 │     │    MySQL     │◀──────────────────┘            │
 │     └──────────────┘                                │
 └──────────────────────────────────────────────────────┘

 8. Project Structure Summary

 📦 movie-recommendation-system
 ┣ 📂 src
 ┃ ┣ 📂 api
 ┃ ┣ 📂 models
 ┃ ┣ 📂 ingestion
 ┃ ┣ 📂 processing
 ┃ ┣ 📂 features
 ┃ ┗ etl_pipeline.py
 ┣ 📂 data
 ┣ 📂 docker
 ┣ 📂 docs
 ┣ 📂 notebooks
 ┣ 📂 tests
 ┣ 📂 models
 ┣ docker-compose.yml
 ┣ run_pipeline.py
 ┣ requirements.txt
 ┣ LICENSE
 ┗ README.md

 ## 9. Component Interactions

| Source     | Target     | Description                                           |
|------------|------------|-------------------------------------------------------|
| Streamlit  | FastAPI    | Sends user requests for recommendations and analytics |
| FastAPI    | MySQL      | Reads movies, ratings, statistics (Gold Layer)        |
| FastAPI    | Models     | Loads trained `.pkl` models for inference             |
| FastAPI    | MLflow     | Fetches experiment metadata & best model parameters   |
| Spark      | MySQL      | Writes cleaned & transformed tables (ETL Level 2)     |
| Pandas     | Raw CSV    | Performs early cleaning before Spark ingestion        |

10. Notes

Architecture reflects Phase 1 → Phase 5 completion.
ASCII diagrams render correctly on GitHub.
All layers follow a standard Data Engineering → Machine Learning → Deployment workflow.

