"""
Quality Checks Script
Step 3.3: Validate data integrity, schemas, and detect anomalies
"""

import pandas as pd
import os
from datetime import datetime

# Configuration
DATA_PATHS = {
    "raw_movies": "data/raw/movies.csv",
    "raw_ratings": "data/raw/ratings.csv",
    "processed_movies": "data/processed/movies_enriched.csv",
    "processed_user_stats": "user_stats.csv",
    "processed_movie_stats": "movie_stats.csv"
}

def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "OK" if exists else "MISSING"
    print(f"[{status}] {description}: {filepath}")
    return exists

def check_movies_schema(df):
    """Validate movies schema"""
    expected_columns = ['movieId', 'title', 'genres']
    actual_columns = list(df.columns)
    
    print(f"\nExpected columns: {expected_columns}")
    print(f"Found columns: {actual_columns}")
    
    missing = set(expected_columns) - set(actual_columns)
    extra = set(actual_columns) - set(expected_columns)
    
    if missing:
        print(f"ERROR - Missing columns: {missing}")
    if extra:
        print(f"WARNING - Extra columns: {extra}")
    if not missing and not extra:
        print("OK - Movies schema valid")

def check_ratings_schema(df):
    """Validate ratings schema"""
    expected_columns = ['userId', 'movieId', 'rating', 'timestamp']
    actual_columns = list(df.columns)
    
    print(f"\nExpected columns: {expected_columns}")
    print(f"Found columns: {actual_columns}")
    
    missing = set(expected_columns) - set(actual_columns)
    extra = set(actual_columns) - set(expected_columns)
    
    if missing:
        print(f"ERROR - Missing columns: {missing}")
    if extra:
        print(f"WARNING - Extra columns: {extra}")
    if not missing and not extra:
        print("OK - Ratings schema valid")

def check_missing_values(df, name):
    """Check for missing values"""
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    
    if len(missing) == 0:
        print(f"OK - {name}: no missing values")
    else:
        print(f"WARNING - {name}: missing values detected")
        for col, count in missing.items():
            print(f"   - {col}: {count} missing ({count/len(df)*100:.2f}%)")

def main():
    """Main quality checks function"""
    print("="*60)
    print("QUALITY CHECKS - DATA VALIDATION")
    print("="*60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 1. Check file existence
    print("\nCHECKING FILE EXISTENCE")
    print("-" * 40)
    
    all_files_exist = True
    for key, path in DATA_PATHS.items():
        if not check_file_exists(path, key):
            all_files_exist = False
    
    if not all_files_exist:
        print("\nERROR: Some files are missing. Stopping checks.")
        return
    
    # 2. Load data
    print("\nLOADING DATA")
    print("-" * 40)
    
    df_raw_movies = pd.read_csv(DATA_PATHS["raw_movies"])
    df_raw_ratings = pd.read_csv(DATA_PATHS["raw_ratings"])
    
    print(f"OK - Raw movies: {len(df_raw_movies):,} rows")
    print(f"OK - Raw ratings: {len(df_raw_ratings):,} rows")
    
    # 3. Validate schemas
    print("\nSCHEMA VALIDATION")
    print("-" * 40)
    check_movies_schema(df_raw_movies)
    check_ratings_schema(df_raw_ratings)
    
    # 4. Check missing values
    print("\nMISSING VALUES CHECK")
    print("-" * 40)
    check_missing_values(df_raw_movies, "Raw movies")
    check_missing_values(df_raw_ratings, "Raw ratings")
    
    # 5. Check duplicates
    print("\nDUPLICATES CHECK")
    print("-" * 40)
    
    movies_duplicates = df_raw_movies.duplicated().sum()
    print(f"Movies - duplicates: {movies_duplicates}")
    
    ratings_duplicates = df_raw_ratings.duplicated().sum()
    print(f"Ratings - duplicates: {ratings_duplicates}")
    
    # 6. Check value ranges
    print("\nRANGE VALIDATION")
    print("-" * 40)
    
    # Ratings between 0.5 and 5.0
    invalid_ratings = df_raw_ratings[(df_raw_ratings['rating'] < 0.5) | (df_raw_ratings['rating'] > 5.0)]
    print(f"Ratings out of range (0.5-5.0): {len(invalid_ratings)}")
    
    # Movie years if available
    if 'year' in df_raw_movies.columns:
        invalid_years = df_raw_movies[(df_raw_movies['year'] < 1900) | (df_raw_movies['year'] > 2026)]
        print(f"Invalid years: {len(invalid_years)}")
    
    # 7. Summary
    print("\n" + "="*60)
    print("QUALITY CHECKS COMPLETED")
    print("="*60)

if __name__ == "__main__":
    main()