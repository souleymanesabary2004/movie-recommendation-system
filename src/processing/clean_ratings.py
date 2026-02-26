"""
Spark Cleaning Script - Ratings
Step 3.2.2: Clean ratings data
- Check for missing values
- Remove duplicates
- Add useful columns (year, month, etc.)
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofmonth, dayofweek
import os

# Create Spark session
spark = SparkSession.builder \
    .appName("RatingCleaning") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

# Define path
ratings_path = os.path.join("data", "raw", "ratings.csv")

print("="*50)
print("SPARK CLEANING - RATINGS")
print("="*50)

# 1. READ RAW DATA
print("\nReading raw ratings...")
df_raw = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(ratings_path)

print(f"   Raw rows: {df_raw.count():,}")

# 2. CHECK FOR MISSING VALUES
print("\nChecking missing values:")
df_raw.select([col(c).isNull().alias(c) for c in df_raw.columns]).show()

# 3. REMOVE DUPLICATES
print("\nRemoving duplicates...")
df_deduplicated = df_raw.dropDuplicates(["userId", "movieId", "timestamp"])
duplicates_removed = df_raw.count() - df_deduplicated.count()
print(f"   Duplicates removed: {duplicates_removed}")
print(f"   Clean rows: {df_deduplicated.count():,}")

# 4. ADD USEFUL COLUMNS (temporal features)
print("\nAdding temporal columns...")

# Convert timestamp to datetime
df_clean = df_deduplicated \
    .withColumn("datetime", (col("timestamp").cast("timestamp"))) \
    .withColumn("year", year("datetime")) \
    .withColumn("month", month("datetime")) \
    .withColumn("day", dayofmonth("datetime")) \
    .withColumn("day_of_week", dayofweek("datetime"))

print(f"   Columns added: year, month, day, day_of_week")

# 5. BASIC STATISTICS
print("\nRating statistics:")
df_clean.describe(["rating"]).show()

print("\nRatings per year:")
df_clean.groupBy("year").count().orderBy("year").show()

print("\nRatings per rating value:")
df_clean.groupBy("rating").count().orderBy("rating").show()

# 6. SHOW SAMPLE
print("\nSample of cleaned data:")
df_clean.select("userId", "movieId", "rating", "year", "month").show(10)

print("\nCleaning complete!")

# Stop Spark session
spark.stop()