# Movie Recommendation System

An End-to-End Big Data & Machine Learning project using Docker, MySQL, Python, and Apache Spark.

---

## 🏗️ Architecture

### Technologies Used
- **Language:** Python 3.10
- **Database:** MySQL 8.0 (Dockerized)
- **ETL (Level 1):** Pandas, NumPy, SQLAlchemy
- **ETL (Level 2):** Apache Spark (PySpark)
- **Data Analysis:** Jupyter Notebook, Matplotlib, Seaborn
- **Infrastructure:** Docker (Manual Management)
- **Version Control:** Git, GitHub

---

## 📂 Project Structure

movie-recommendation-system/
├── src/
│ ├── init_db.py # Database initialization
│ ├── etl_pipeline.py # ETL with Pandas (Level 1)
│ ├── quality_checks.py # Data quality validation
│ ├── ingestion/ # Spark ingestion scripts
│ │ ├── ingest_movies.py
│ │ └── ingest_ratings.py
│ └── processing/ # Spark processing scripts
│ ├── clean_movies.py
│ ├── clean_ratings.py
│ ├── transform_movies.py
│ └── transform_ratings.py
├── data/
│ ├── raw/ # Raw CSV files (MovieLens)
│ │ ├── movies.csv
│ │ └── ratings.csv
│ └── processed/ # Cleaned and enriched data
│ ├── movies_enriched.csv
│ └── genre_counts.csv
├── notebooks/
│ └── 01_exploration_pandas.ipynb # EDA with Pandas
├── docs/
│ └── data_dictionary.md # Data documentation
├── run_pipeline.py # Pipeline orchestrator
├── user_stats.csv # User statistics
├── movie_stats.csv # Movie statistics
├── top_movies.csv # Top 20 most rated movies
├── .env.example # Environment variables template
├── .gitignore # Git ignore file
├── requirements.txt # Python dependencies
├── LICENSE # MIT License
└── README.md # This file


---

## ✅ Current Status (February 2026)

### Completed
- ✅ **Infrastructure**
  - Docker container with MySQL
  - Persistent volume for data
  - Database schema (movies, ratings)
  - Secure credentials with `.env`

- ✅ **Data Exploration (Pandas)**
  - Jupyter notebook with EDA
  - Data inspection and cleaning
  - Visualizations (Matplotlib, Seaborn)
  - Timestamp conversion

- ✅ **ETL with Pandas (Level 1)**
  - Extract from CSV
  - Transform (clean, convert)
  - Load into MySQL

- ✅ **ETL with Spark (Level 2) - COMPLETE**
  - Ingestion scripts (movies, ratings)
  - Cleaning scripts (NULL handling, duplicates)
  - Transformation scripts (features, statistics)
  - Pipeline orchestrator (`run_pipeline.py`)
  - Quality checks automation

- ✅ **Data Products Generated**
  - `user_stats.csv`: User behavior statistics (610 users)
  - `movie_stats.csv`: Movie popularity metrics (9,724 movies)
  - `top_movies.csv`: Top 20 most rated films
  - `movies_enriched.csv`: Films with genres, year, and ratings
  - `genre_counts.csv`: Distribution of genres

### Next Steps (Phase 4)
- ⏳ Machine Learning models
  - Collaborative filtering
  - Content-based filtering
  - Hybrid models
- ⏳ Model evaluation (precision, recall, RMSE)
- ⏳ MLFlow tracking
- ⏳ FastAPI REST API
- ⏳ Streamlit dashboard

---

## 📊 Dataset: MovieLens

- **Source:** [GroupLens Research](https://grouplens.org/datasets/movielens/)
- **Version:** ml-latest-small
- **Movies:** 9,742
- **Ratings:** 100,836
- **Users:** 610
- **Rating scale:** 0.5 to 5.0 (0.5 steps)
- **Average rating:** 3.53
- **Most common genre:** Drama (4,361 movies)
- **Date range:** 1996-03-29 to 2018-09-24

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Docker
- Git

### Installation

```bash
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

# 7. Run ETL with Pandas
python src/etl_pipeline.py

# 8. Run complete Spark pipeline (ingestion → cleaning → transformation)
python run_pipeline.py

# 9. Run quality checks
python src/quality_checks.py

# 10. Explore data with Jupyter
jupyter notebook
# Open notebooks/01_exploration_pandas.ipynb


---

## ✅ Current Status (February 2026)

### Completed
- ✅ **Infrastructure**
  - Docker container with MySQL
  - Persistent volume for data
  - Database schema (movies, ratings)
  - Secure credentials with `.env`

- ✅ **Data Exploration (Pandas)**
  - Jupyter notebook with EDA
  - Data inspection and cleaning
  - Visualizations (Matplotlib, Seaborn)
  - Timestamp conversion

- ✅ **ETL with Pandas (Level 1)**
  - Extract from CSV
  - Transform (clean, convert)
  - Load into MySQL

- ✅ **ETL with Spark (Level 2) - COMPLETE**
  - Ingestion scripts (movies, ratings)
  - Cleaning scripts (NULL handling, duplicates)
  - Transformation scripts (features, statistics)
  - Pipeline orchestrator (`run_pipeline.py`)
  - Quality checks automation

- ✅ **Data Products Generated**
  - `user_stats.csv`: User behavior statistics (610 users)
  - `movie_stats.csv`: Movie popularity metrics (9,724 movies)
  - `top_movies.csv`: Top 20 most rated films
  - `movies_enriched.csv`: Films with genres, year, and ratings
  - `genre_counts.csv`: Distribution of genres

### Next Steps (Phase 4)
- ⏳ Machine Learning models
  - Collaborative filtering
  - Content-based filtering
  - Hybrid models
- ⏳ Model evaluation (precision, recall, RMSE)
- ⏳ MLFlow tracking
- ⏳ FastAPI REST API
- ⏳ Streamlit dashboard

---

## 📊 Dataset: MovieLens

- **Source:** [GroupLens Research](https://grouplens.org/datasets/movielens/)
- **Version:** ml-latest-small
- **Movies:** 9,742
- **Ratings:** 100,836
- **Users:** 610
- **Rating scale:** 0.5 to 5.0 (0.5 steps)
- **Average rating:** 3.53
- **Most common genre:** Drama (4,361 movies)
- **Date range:** 1996-03-29 to 2018-09-24

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Docker
- Git

### Installation

```bash
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

# 7. Run ETL with Pandas
python src/etl_pipeline.py

# 8. Run complete Spark pipeline (ingestion → cleaning → transformation)
python run_pipeline.py

# 9. Run quality checks
python src/quality_checks.py

# 10. Explore data with Jupyter
jupyter notebook

# Open notebooks/01_exploration_pandas.ipynb

📊 Sample Results

Top 5 Most Rated Movies
Movie ID	Rating Count	Average Rating
356	329	4.16
318	317	4.43
296	307	4.20
593	279	4.16
2571	278	4.19

Genre Distribution
Genre	Number of Movies
Drama	4,361
Comedy	3,756
Thriller	1,894
Action	1,828
Romance	1,596

📚 Documentation
docs/data_dictionary.md - Complete data documentation

notebooks/01_exploration_pandas.ipynb - EDA notebook

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👤 Author
SOULEYMANE SOUMAHORO

GitHub: @souleymanesabary2004

LinkedIn: Souleymane Soumahoro

🙏 Acknowledgments
GroupLens Research for the MovieLens dataset

Apache Spark for distributed processing

Pandas for data manipulation

All open-source contributors

⭐ Support
If you find this project useful, please give it a star on GitHub!