# Movie Recommendation System

An End-to-End Big Data & Machine Learning project using Docker, MySQL, Python, Apache Spark, Scikit-learn, and MLFlow.

---

## 🏗️ Architecture

### Technologies Used
| Category                | Technologies |
|-------------------------|--------------|
| **Language**            | Python 3.10 |
| **Database**            | MySQL 8.0 (Dockerized) |
| **ETL (Level 1)**       | Pandas, NumPy, SQLAlchemy |
| **ETL (Level 2)**       | Apache Spark (PySpark) |
| **Machine Learning**    | Scikit-learn (SVD, KNN, metrics, preprocessing), Joblib |
| **Experiment Tracking** | MLFlow |
| **Data Analysis**       | Jupyter Notebook, Matplotlib, Seaborn |
| **Infrastructure**      | Docker (Manual Management) |
| **Version Control**     | Git, GitHub |
| **Dependencies**        | See `requirements.txt` |

### Key Libraries Used
- **scikit-learn**: Machine learning algorithms (SVD, KNN, metrics, preprocessing)
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib/seaborn**: Data visualization
- **mlflow**: Experiment tracking and model versioning
- **joblib**: Model serialization
- **pyspark**: Distributed data processing
- **sqlalchemy**: Database connection
- **mysql-connector-python**: MySQL driver

---

## 📂 Project Structure
movie-recommendation-system/
│
├── src/
│ ├── init.py
│ ├── init_db.py # Database initialization
│ ├── etl_pipeline.py # ETL with Pandas (Level 1)
│ ├── quality_checks.py # Data quality validation
│ │
│ ├── ingestion/ # Spark ingestion scripts
│ │ ├── ingest_movies.py
│ │ └── ingest_ratings.py
│ │
│ ├── processing/ # Spark processing scripts
│ │ ├── clean_movies.py
│ │ ├── clean_ratings.py
│ │ ├── transform_movies.py
│ │ └── transform_ratings.py
│ │
│ ├── features/ # Feature engineering
│ │ └── build_features.py
│ │
│ └── models/ # Machine Learning models
│ ├── train_svd.py
│ ├── train_knn.py
│ ├── train_content.py
│ ├── train_hybrid.py
│ ├── evaluate.py
│ └── predict.py
│
├── data/
│ ├── raw/ # Raw CSV files (MovieLens)
│ │ ├── movies.csv
│ │ ├── ratings.csv
│ │ ├── tags.csv
│ │ └── links.csv
│ │
│ └── processed/ # Cleaned and enriched data
│ ├── movies_enriched.csv
│ ├── genre_counts.csv
│ ├── movie_features.csv
│ ├── user_movie_matrix.csv
│ └── user_movie_matrix_norm.csv
│
├── notebooks/
│ ├── 01_exploration_pandas.ipynb # EDA with Pandas
│ └── 02_feature_engineering.ipynb # ML feature engineering
│
├── docs/
│ └── data_dictionary.md # Complete data documentation
│
├── mlruns/ # MLFlow experiment tracking
├── run_pipeline.py # Pipeline orchestrator
├── user_stats.csv # User statistics
├── movie_stats.csv # Movie statistics
├── top_movies.csv # Top 20 most rated movies
├── svd_model.pkl # Trained SVD model (scikit-learn)
├── knn_model.pkl # Trained KNN model (scikit-learn)
├── content_model.pkl # Content-based model
├── hybrid_model.pkl # Hybrid model config
├── model_evaluation_results.csv # Model comparison
├── .env.example # Environment variables template
├── .gitignore # Git ignore file
├── requirements.txt # Python dependencies
├── LICENSE # MIT License
└── README.md # This file


---

## ✅ Current Status (March 2026)

### Phase 1-2: Infrastructure & Exploration
- ✅ Docker container with MySQL (persistent volume)
- ✅ Database schema (movies, ratings tables)
- ✅ Secure credentials with `.env`
- ✅ Data exploration in Jupyter (EDA, visualizations)

### Phase 3: Data Engineering - COMPLETE
- ✅ **ETL with Pandas (Level 1)**
  - Extract from CSV, transform, load into MySQL
- ✅ **ETL with Spark (Level 2)**
  - Ingestion scripts (movies, ratings)
  - Cleaning scripts (NULL handling, duplicates)
  - Transformation scripts (features, statistics)
  - Pipeline orchestrator (`run_pipeline.py`)
  - Quality checks automation
- ✅ **Data Products Generated**
  - `user_stats.csv`: User behavior (610 users)
  - `movie_stats.csv`: Movie popularity (9,724 movies)
  - `movies_enriched.csv`: Films with genres, year, ratings
  - `genre_counts.csv`: Genre distribution

### Phase 4: Machine Learning - COMPLETE
- ✅ **Feature Engineering (scikit-learn)**
  - User features: rating_count, avg_rating, std_rating
  - Movie features: one-hot encoded genres (`MultiLabelBinarizer`)
  - Text features: TF-IDF on tags (`TfidfVectorizer`)
  - Feature matrix: `movie_features.csv` (9742 × 77)

- ✅ **Models Implemented (scikit-learn)**
  - **SVD (Matrix Factorization)**: `TruncatedSVD`, RMSE=0.7456, MAE=0.5296
  - **KNN (Collaborative Filtering)**: `NearestNeighbors`, avg similarity=0.157
  - **Content-based**: Cosine similarity matrix
  - **Hybrid model**: Combining collaborative + content-based

- ✅ **Evaluation (scikit-learn metrics)**
  - RMSE, MAE, explained variance
  - Comprehensive model comparison
  - Results saved in `model_evaluation_results.csv`

- ✅ **Experiment Tracking (MLFlow)**
  - All experiments logged with parameters and metrics
  - Models saved as `.pkl` files via `joblib`

- ✅ **Prediction Pipeline**
  - Generate recommendations using any trained model
  - Support for all 4 model types

-----------
-----------
### Next Steps (Phase 5)
- ⏳ FastAPI REST API
- ⏳ Streamlit dashboard
- ⏳ Model deployment
- ⏳ A/B testing simulation

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

## 📈 Model Performance Summary

| Model       | RMSE  | MAE   | Similarity | Key Libraries |
|-------------|------ |-----  |------------|---------------|
| **SVD**     | 0.746 | 0.530 | -          | `sklearn.decomposition.TruncatedSVD` |
| **KNN**     | -     | -     | 0.157      | `sklearn.neighbors.NearestNeighbors` |
| **Content** | -     | -     | 1.000      | `sklearn.metrics.pairwise.cosine_similarity` |
| **Hybrid**  | -     | -     | -          | Combination of all |

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

# 8. Run complete Spark pipeline
python run_pipeline.py

# 9. Run quality checks
python src/quality_checks.py

# 10. Feature engineering (scikit-learn)
python src/features/build_features.py

# 11. Train models (scikit-learn)
python src/models/train_svd.py
python src/models/train_knn.py
python src/models/train_content.py
python src/models/train_hybrid.py

# 12. Evaluate models (scikit-learn metrics)
python src/models/evaluate.py

# 13. Generate recommendations
python src/models/predict.py

# 14. Explore data with Jupyter
jupyter notebook
# Open notebooks/01_exploration_pandas.ipynb
# Open notebooks/02_feature_engineering.ipynb

# 15. View MLFlow experiments
mlflow ui
# Open http://localhost:5000

📊 Sample Results

Top 5 Most Rated Movies

Movie ID	Rating Count	Average Rating

356	             329	4.16
318	             317	4.43
296	             307	4.20
593	             279	4.16
2571	             278	4.19

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

notebooks/02_feature_engineering.ipynb - ML notebook

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👤 Author
SOULEYMANE SOUMAHORO

GitHub: @souleymanesabary2004

LinkedIn: Souleymane Soumahoro

🙏 Acknowledgments
GroupLens Research for the MovieLens dataset

Apache Spark for distributed processing

Scikit-learn for machine learning algorithms

MLFlow for experiment tracking

Pandas for data manipulation

All open-source contributors

⭐ Support
If you find this project useful, please give it a star on GitHub!
