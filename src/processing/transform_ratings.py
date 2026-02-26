"""
Spark Transformations Script - Ratings
Step 3.2.3: Advanced transformations on ratings data
- Calculate user statistics (average rating per user)
- Calculate movie statistics (average rating per movie)
- Display top 20 most rated movies
- Save results to CSV using Pandas
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, stddev, min, max
import pandas as pd
import os

# Create processed folder if it doesn't exist
os.makedirs("data/processed", exist_ok=True)

# Create Spark session
spark = SparkSession.builder \
    .appName("RatingTransformations") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

print("="*50)
print("SPARK TRANSFORMATIONS - RATINGS")
print("="*50)

# Define path
ratings_path = os.path.join("data", "raw", "ratings.csv")

# Load raw ratings
print("\nLoading ratings data...")
df_ratings = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(ratings_path)

print(f"   Loaded: {df_ratings.count():,} rows")

# Calculate user statistics
print("\nCalculating user statistics...")

user_stats_spark = df_ratings.groupBy("userId").agg(
    count("rating").alias("rating_count"),
    avg("rating").alias("avg_rating"),
    stddev("rating").alias("std_rating"),
    min("rating").alias("min_rating"),
    max("rating").alias("max_rating")
)

print(f"   Users analyzed: {user_stats_spark.count():,}")
print("\nSample user statistics:")
user_stats_spark.show(10)

# Calculate movie statistics
print("\nCalculating movie statistics...")

movie_stats_spark = df_ratings.groupBy("movieId").agg(
    count("rating").alias("rating_count"),
    avg("rating").alias("avg_rating"),
    stddev("rating").alias("std_rating"),
    min("rating").alias("min_rating"),
    max("rating").alias("max_rating")
)

print(f"   Movies analyzed: {movie_stats_spark.count():,}")
print("\nSample movie statistics:")
movie_stats_spark.show(10)

# Top 20 most rated movies
print("\nTop 20 most rated movies:")
top_movies = movie_stats_spark.orderBy(col("rating_count").desc()).limit(20)
top_movies.show()

# ============================================
# SAVING RESULTS WITH PANDAS
# ============================================

print("\n" + "="*50)
print("SAVING RESULTS WITH PANDAS")
print("="*50)

# Convert Spark DataFrames to Pandas
print("\nConverting to Pandas...")
user_stats_pd = user_stats_spark.toPandas()
movie_stats_pd = movie_stats_spark.toPandas()
top_movies_pd = top_movies.toPandas()

print(f"   User stats: {len(user_stats_pd)} rows")
print(f"   Movie stats: {len(movie_stats_pd)} rows")
print(f"   Top movies: {len(top_movies_pd)} rows")

# Save to CSV (in root directory)
print("\nSaving to CSV...")

user_stats_pd.to_csv("user_stats.csv", index=False)
print("   User statistics saved to user_stats.csv")

movie_stats_pd.to_csv("movie_stats.csv", index=False)
print("   Movie statistics saved to movie_stats.csv")

top_movies_pd.to_csv("top_movies.csv", index=False)
print("   Top movies saved to top_movies.csv")

print("\nAll files saved successfully!")

# Stop Spark session
spark.stop()