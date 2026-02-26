"""
Spark Ingestion Script - Ratings
Step 3.2.1: Read ratings.csv into Spark DataFrame
"""

from pyspark.sql import SparkSession
import os

# Create Spark session
spark = SparkSession.builder \
    .appName("RatingIngestion") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

# Define path
ratings_path = os.path.join("data", "raw", "ratings.csv")

print("="*50)
print("SPARK INGESTION - RATINGS")
print("="*50)

# Read CSV with schema inference
df_ratings = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(ratings_path)

# Show basic info
print(f"\nRatings loaded: {df_ratings.count():,} rows")
print(f"\nSchema:")
df_ratings.printSchema()

print(f"\nFirst 5 rows:")
df_ratings.show(5, truncate=False)

print("\nStatistics:")
df_ratings.describe().show()

# Stop Spark session
spark.stop()