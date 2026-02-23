"""
Spark Ingestion Script - Movies
Step 3.2.1: Read movies.csv into Spark DataFrame
"""

from pyspark.sql import SparkSession
import os

# Create Spark session
spark = SparkSession.builder \
    .appName("MovieIngestion") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

# Define path
movies_path = os.path.join("data", "raw", "movies.csv")

print("="*50)
print("📥 SPARK INGESTION - MOVIES")
print("="*50)

# Read CSV with schema inference
df_movies = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(movies_path)

# Show basic info
print(f"\n✅ Movies loaded: {df_movies.count():,} rows")
print(f"\n📋 Schema:")
df_movies.printSchema()

print(f"\n👀 First 5 rows:")
df_movies.show(5, truncate=False)

print("\n📊 Statistics:")
df_movies.describe().show()

# Stop Spark session
spark.stop()