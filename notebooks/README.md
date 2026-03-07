# Notebooks - Data Exploration & Machine Learning

This folder contains Jupyter notebooks for data analysis and model development.

---

## 📚 Available Notebooks

| Notebook | Description | Status | Libraries |
|----------|-------------|--------|-----------|
| `01_exploration_pandas.ipynb` | Initial data exploration with Pandas | ✅ Complete | pandas, matplotlib, seaborn |
| `02_feature_engineering.ipynb` | Feature engineering and ML model development | ✅ Complete | pandas, numpy, scikit-learn, mlflow |

---

## 📊 Notebook 01: `01_exploration_pandas.ipynb`

### 🎯 Objectives
- Load and explore the MovieLens dataset
- Understand data structure and quality
- Perform initial visualizations
- Prepare for ETL pipeline

### 📝 Contents
1. **Import libraries** - pandas, numpy, matplotlib, seaborn
2. **Load CSV files** - movies.csv and ratings.csv
3. **Data inspection** - info(), shape, missing values
4. **Descriptive statistics** - describe(), value_counts()
5. **Visualizations** - histograms, bar charts
6. **Genre analysis** - split genres, count frequencies
7. **Timestamp conversion** - Unix to datetime
8. **ETL readiness check** - validate before loading

### 🔍 Key Findings
| Metric                | Value   |
|----------------       |-------  |
| **Movies**            | 9,742   |
| **Ratings**           | 100,836 |
| **Missing values**    | 0       |
| **Average rating**    | 3.53 |
| **Most common genre** | Drama (5,032 movies) |
| **Most rated movie**  | Forrest Gump (341 ratings) |
| **Date range**        | 1996-03-29 to 2018-09-24 |

---

## 📊 Notebook 02: `02_feature_engineering.ipynb`

### 🎯 Objectives
Transform raw data into features and train machine learning models for movie recommendations.

### 🔧 Libraries Used
| Library           | Purpose |
|---------          |---------|
| **pandas, numpy** | Data manipulation |
| **scikit-learn**  | Machine learning models and metrics |
| **mlflow**        |Experiment tracking |
| **joblib**        | Model serialization |

### 📝 Contents

| Cellules | Topic                |            Description                   |
|----------|----------------------|------------------------------------------|
| 1-3      | Setup & Data Loading | Import libraries, load pre-processed data |
| 4-5      | Feature Engineering | Create user-movie matrix, normalize ratings |
| 6        | Genre Encoding      | One-hot encoding with `MultiLabelBinarizer` |
| 7-8      | Movie Features      | Combine all movie features |
| 9        | Complete Dataset    | Merge all features for ML |
| 10-11    | KNN Model           | Collaborative filtering with KNN |
| 12-13    | Content-based Model | Cosine similarity between movies |
| 14       | Hybrid Model        | Combine collaborative and content-based |
| 15-19    | Evaluation          | Precision, recall, RMSE, Hit Rate |
| 20-26    | MLFlow Tracking     | Log experiments, save models |
| 27       | Update requirements | Save dependencies |
| 28-29    | Git & Results       | Commit changes, display summary |
 
### 📊 Key Results

| Model       | RMSE  | MAE   | Similarity | Hit Rate@10 |
|-------------|-------|-----  |------------|-------------|
| **SVD**     | 0.746 | 0.530 | -          | -          |
| **KNN**     | -     | -     | 0.157      | 93.4%      |
| **Content** | -     | -     | 1.000      | -          |
| **Hybrid**  | -     | -     | -          | -          |

### 💾 Generated Files

| File                           | Location          | Description |
|--------------------------------|-------------------|-------------|
| `movie_features.csv`           | `data/processed/` | Final feature matrix |
| `user_movie_matrix.csv`        | `data/processed/` | Raw user-movie matrix |
| `user_movie_matrix_norm.csv`   | `data/processed/` | Normalized matrix |
| `svd_model.pkl`                | Root              | Trained SVD model |
| `knn_model.pkl`                | Root              | Trained KNN model |
| `content_model.pkl`            | Root              | Content-based model |
| `hybrid_model.pkl`             | Root              | Hybrid model |
| `model_evaluation_results.csv` | Root              | Model comparison |
| `mlruns/`                      | Root              | MLFlow experiments |

---

## 🚀 How to Run

```bash
# From project root
jupyter notebook
# Navigate to notebooks/01_exploration_pandas.ipynb
# or notebooks/02_feature_engineering.ipynb