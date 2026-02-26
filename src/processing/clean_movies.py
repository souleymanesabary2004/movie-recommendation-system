"""
Spark Cleaning Script - Movies
Step 3.2.2: Clean movies data
- Handle missing values
- Standardize genres
- Add useful columns
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, length, split, size
import os

# Create Spark session
spark = SparkSession.builder \
    .appName("MovieCleaning") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

# Define path
movies_path = os.path.join("data", "raw", "movies.csv")

print("="*50)
print("SPARK CLEANING - MOVIES")
print("="*50)

# 1. READ RAW DATA
print("\nReading raw movies...")
df_raw = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(movies_path)

print(f"   Raw rows: {df_raw.count():,}")

# 2. CHECK FOR MISSING VALUES
print("\nChecking missing values:")
df_raw.select([col(c).isNull().alias(c) for c in df_raw.columns]).show()

# 3. CLEANING OPERATIONS
print("\nApplying cleaning...")

df_clean = df_raw \
    .fillna({"genres": "(no genres listed)"}) \
    .filter(col("title").isNotNull()) \
    .dropDuplicates(["movieId"])

print(f"   Clean rows: {df_clean.count():,}")

# 4. ADD USEFUL COLUMNS
print("\nAdding computed columns...")

df_clean = df_clean \
    .withColumn("title_length", length(col("title"))) \
    .withColumn("genre_count", 
                when(col("genres") == "(no genres listed)", 0)
                .otherwise(size(split(col("genres"), "\|"))))

# 5. SHOW RESULTS
print("\nClean schema:")
df_clean.printSchema()

print("\nSample of cleaned data:")
df_clean.select("movieId", "title", "genres", "title_length", "genre_count").show(10, truncate=False)

print("\nStatistics after cleaning:")
df_clean.describe(["title_length", "genre_count"]).show()

# Stop Spark session
spark.stop()