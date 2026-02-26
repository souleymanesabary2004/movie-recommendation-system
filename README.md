# Movie Recommendation System

An End-to-End Big Data & Machine Learning project using Docker, MySQL, and Python.

---

## 🏗️ Architecture

- **Language:** Python 3.10
- **Database:** MySQL 8.0 (Dockerized)
- **ETL (Level 1):** Pandas & SQLAlchemy
- **ETL (Level 2):** Apache Spark (PySpark)
- **Infrastructure:** Docker (Manual Management)

---

## 📂 Project Structure

movie-recommendation-system/
│
├── src/
│   ├── __init__.py
│   ├── init_db.py
│   ├── etl_pipeline.py
│   ├── quality_checks.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── ingest_movies.py
│   │   └── ingest_ratings.py
│   │
│   └── processing/
│       ├── __init__.py
│       ├── clean_movies.py
│       ├── clean_ratings.py
│       ├── transform_movies.py
│       └── transform_ratings.py
│
├── data/
│   ├── raw/
│   │   ├── movies.csv
│   │   ├── ratings.csv
│   │   ├── tags.csv
│   │   └── links.csv
│   │
│   └── processed/
│       ├── movies_clean.csv
│       ├── movies_enriched.csv
│       └── genre_counts.csv
│
├── notebooks/
│   ├── 01_exploration_pandas.ipynb
│   └── README.md
│
├── docs/
│   └── data_dictionary.md
│
├── docker/
│
├── tests/
│   └── __init__.py
│
├── run_pipeline.py
├── user_stats.csv
├── movie_stats.csv
├── top_movies.csv
├── .env.example
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md

## ✅ Current Status (February 2026)

### Completed
- ✅ Docker container with MySQL
- ✅ Database schema (movies, ratings tables)
- ✅ Secure credentials with `.env`
- ✅ Data exploration in Jupyter
- ✅ ETL with Pandas (Level 1)
- ✅ **ETL with Spark (Level 2) - COMPLETE**
  - ✅ Ingestion scripts (`ingest_movies.py`, `ingest_ratings.py`)
  - ✅ Cleaning scripts (`clean_movies.py`, `clean_ratings.py`)
  - ✅ Transformation scripts (`transform_movies.py`, `transform_ratings.py`)
  - ✅ Pipeline orchestrator (`run_pipeline.py`)
  - ✅ Quality checks (`quality_checks.py`)

### Generated Files
- `user_stats.csv` - User statistics (610 users, rating count, average, etc.)
- `movie_stats.csv` - Movie statistics from ratings (9,724 movies)
- `top_movies.csv` - Top 20 most rated movies
- `data/processed/movies_enriched.csv` - Movies with genres, year, and statistics
- `data/processed/genre_counts.csv` - Number of movies per genre

### In Progress
- ⏳ Machine Learning models (Phase 4)

### Planned
- ⏳ FastAPI REST API
- ⏳ Streamlit dashboard

---

## 📊 Dataset: MovieLens

- **Movies:** 9,742
- **Ratings:** 100,836
- **Users:** 610
- **Average rating:** 3.53
- **Most common genre:** Drama (4,361 movies)
- **Date range:** 1996-2018

---

## ⚡ Quick Start

```bash
# Clone
git clone https://github.com/souleymanesabary2004/movie-recommendation-system.git
cd movie-recommendation-system

# Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Start MySQL
docker run --name mysql-movies -e MYSQL_ROOT_PASSWORD=your_password -v mysql_data:/var/lib/mysql -p 2004:3306 -d mysql:8.0

# Initialize database
python src/init_db.py

# Run ETL (Pandas)
python src/etl_pipeline.py

# Run complete Spark pipeline (ingestion → cleaning → transformation)
python run_pipeline.py

# Run quality checks
python src/quality_checks.py

# Try individual Spark scripts
python src/ingestion/ingest_movies.py
python src/processing/clean_movies.py
python src/processing/transform_ratings.py

📚 Documentation
See docs/data_dictionary.md for detailed data documentation including all generated files.

📄 License
MIT License - see LICENSE file.

👤 Author
SOULEYMANE SOUMAHORO
GitHub: @souleymanesabary2004
LinkedIn: www.linkedin.com/in/souleymane-soumahoro-b980b438b

