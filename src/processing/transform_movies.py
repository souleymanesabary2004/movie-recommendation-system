"""
Spark Transformations Script - Movies
Step 3.2.3: Advanced transformations on movies data
- Extract features from genres
- Calculate statistics from ratings (using ratings data)
- Join with ratings statistics
- Save results to CSV using Pandas
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, explode, count, avg, stddev, min, max, length, when, size, regexp_extract
import pandas as pd
import os

# Create processed folder if it doesn't exist
os.makedirs("data/processed", exist_ok=True)

# Create Spark session
spark = SparkSession.builder \
    .appName("MovieTransformations") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

print("="*50)
print("SPARK TRANSFORMATIONS - MOVIES")
print("="*50)

# Define paths
movies_path = os.path.join("data", "raw", "movies.csv")
ratings_path = os.path.join("data", "raw", "ratings.csv")

# Load movies data
print("\nLoading movies data...")
df_movies = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(movies_path)

print(f"   Movies loaded: {df_movies.count():,} rows")

# Load ratings data (for statistics)
print("\nLoading ratings data...")
df_ratings = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(ratings_path)

print(f"   Ratings loaded: {df_ratings.count():,} rows")

# ============================================
# 1. CALCULATE MOVIE STATISTICS FROM RATINGS
# ============================================

print("\n" + "="*50)
print("1. CALCULATING MOVIE STATISTICS FROM RATINGS")
print("="*50)

movie_stats = df_ratings.groupBy("movieId").agg(
    count("rating").alias("rating_count"),
    avg("rating").alias("avg_rating"),
    stddev("rating").alias("std_rating"),
    min("rating").alias("min_rating"),
    max("rating").alias("max_rating")
)

print(f"   Movies with ratings: {movie_stats.count():,}")
print("\nSample movie statistics:")
movie_stats.show(10)

# ============================================
# 2. EXTRACT GENRE FEATURES
# ============================================

print("\n" + "="*50)
print("2. EXTRACTING GENRE FEATURES")
print("="*50)

# Split genres into array
df_movies = df_movies.withColumn("genre_array", split(col("genres"), "\|"))

# Count number of genres per movie
df_movies = df_movies.withColumn(
    "genre_count", 
    when(col("genres") == "(no genres listed)", 0)
    .otherwise(size(col("genre_array")))
)

print("\nMovies with genre count:")
df_movies.select("movieId", "title", "genres", "genre_count").show(10)

# Explode genres to get one row per genre (for analysis)
df_genres_exploded = df_movies.select(
    "movieId", 
    "title", 
    explode(col("genre_array")).alias("genre")
)

print("\nGenres exploded (one row per genre):")
df_genres_exploded.show(10)

# Count movies per genre
genre_counts = df_genres_exploded.groupBy("genre").count().orderBy(col("count").desc())
print("\nMovies per genre:")
genre_counts.show(20)

# ============================================
# 3. EXTRACT YEAR FROM TITLE
# ============================================

print("\n" + "="*50)
print("3. EXTRACTING YEAR FROM TITLE")
print("="*50)

# Extract year using regex
df_movies = df_movies.withColumn(
    "year_str", 
    regexp_extract(col("title"), r'\((\d{4})\)', 1)
)

# Count movies with and without year
movies_with_year = df_movies.filter(col("year_str") != "")
movies_without_year = df_movies.filter(col("year_str") == "")

print(f"   Movies with year: {movies_with_year.count():,}")
print(f"   Movies without year: {movies_without_year.count():,}")

# ============================================
# 4. JOIN WITH RATINGS STATISTICS
# ============================================

print("\n" + "="*50)
print("4. JOINING WITH RATINGS STATISTICS")
print("="*50)

# Left join to keep all movies (even those without ratings)
df_movies_enriched = df_movies.join(movie_stats, on="movieId", how="left")

print("\nEnriched movies (with statistics):")
df_movies_enriched.select(
    "movieId", "title", "year_str", "genre_count", "rating_count", "avg_rating"
).show(10)

print(f"   Movies with ratings: {df_movies_enriched.filter(col('rating_count').isNotNull()).count():,}")
print(f"   Movies without ratings: {df_movies_enriched.filter(col('rating_count').isNull()).count():,}")

# Fill null values in statistics (for movies without ratings)
df_movies_final = df_movies_enriched.fillna({
    "rating_count": 0,
    "avg_rating": 0.0,
    "std_rating": 0.0,
    "min_rating": 0.0,
    "max_rating": 0.0
})

# ============================================
# 5. SAVING RESULTS WITH PANDAS
# ============================================

print("\n" + "="*50)
print("5. SAVING RESULTS WITH PANDAS")
print("="*50)

# Convert to Pandas
print("\nConverting to Pandas...")
movies_enriched_pd = df_movies_final.toPandas()
genre_counts_pd = genre_counts.toPandas()

print(f"   Enriched movies: {len(movies_enriched_pd)} rows")
print(f"   Genre counts: {len(genre_counts_pd)} rows")

# Save to CSV
print("\nSaving to CSV...")

movies_enriched_pd.to_csv("data/processed/movies_enriched.csv", index=False)
print("   Movies enriched saved to data/processed/movies_enriched.csv")

genre_counts_pd.to_csv("data/processed/genre_counts.csv", index=False)
print("   Genre counts saved to data/processed/genre_counts.csv")

print("\nAll files saved successfully!")

# Stop Spark session
spark.stop()