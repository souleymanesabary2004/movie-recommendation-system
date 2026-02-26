\# Data Dictionary - Movie Recommendation System



\## 📂 Data Structure

data/

│

├── raw/ # Raw CSV files

│ ├── movies.csv

│ ├── ratings.csv

│ ├── tags.csv

│ └── links.csv

│

└── processed/ # Cleaned data

└── movies\_clean.csv





\## 📊 File Descriptions



\### `movies.csv`

| Column | Type | Description | Example |

|--------|------|-------------|---------|

| movieId | int | Unique movie ID | 1 |

| title | str | Movie title with year | Toy Story (1995) |

| genres | str | Pipe-separated genres | Adventure\\|Animation\\|Children |



\### `ratings.csv`

| Column | Type | Description | Example |

|--------|------|-------------|---------|

| userId | int | Unique user ID | 1 |

| movieId | int | References movies.csv | 1 |

| rating | float | 0.5 to 5.0 (0.5 steps) | 4.0 |

| timestamp | int | Unix timestamp | 964982703 |



\## 📈 Statistics



| Metric | Value |

|--------|-------|

| Total movies | 9,742 |

| Total ratings | 100,836 |

| Total users | 610 |

| Average rating | 3.53 |

| Most common genre | Drama (5,032 movies) |

| Most rated movie | Forrest Gump (341 ratings) |

| Date range | 1996-03-29 to 2018-09-24 |



\## 🔧 Transformations



1\. \*\*Timestamps\*\* → datetime: `pd.to\_datetime(timestamp, unit='s')`

2\. \*\*Movie years\*\* extracted from titles: regex `r'\\((\\d{4})\\)'`

3\. \*\*Genres\*\* split for analysis: `str.split('|')`

## 📁 Generated Files (Phase 3 - Spark ETL)

### `user_stats.csv`
Statistics per user calculated from ratings data.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| userId | int | Unique user ID | 148 |
| rating_count | int | Number of ratings by this user | 48 |
| avg_rating | float | Average rating given by this user | 3.74 |
| std_rating | float | Standard deviation of ratings | 0.68 |
| min_rating | float | Minimum rating given | 1.5 |
| max_rating | float | Maximum rating given | 5.0 |

### `movie_stats.csv`
Statistics per movie calculated from ratings data.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| movieId | int | Unique movie ID | 356 |
| rating_count | int | Number of ratings received | 329 |
| avg_rating | float | Average rating | 4.16 |
| std_rating | float | Standard deviation of ratings | 0.83 |
| min_rating | float | Minimum rating received | 0.5 |
| max_rating | float | Maximum rating received | 5.0 |

### `top_movies.csv`
Top 20 most rated movies (by number of ratings).

| Column | Type | Description |
|--------|------|-------------|
| movieId | int | Movie ID |
| rating_count | int | Number of ratings |
| avg_rating | float | Average rating |
| std_rating | float | Standard deviation |
| min_rating | float | Minimum rating |
| max_rating | float | Maximum rating |

### `movies_enriched.csv` (in `data/processed/`)
Movies enriched with genre features and rating statistics.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| movieId | int | Movie ID | 1 |
| title | str | Movie title | Toy Story (1995) |
| genres | str | Pipe-separated genres | Adventure\|Animation\|Children |
| year_str | str | Year extracted from title | 1995 |
| genre_count | int | Number of genres | 5 |
| rating_count | int | Number of ratings received | 215 |
| avg_rating | float | Average rating | 3.92 |
| std_rating | float | Standard deviation | 0.83 |
| min_rating | float | Minimum rating | 0.5 |
| max_rating | float | Maximum rating | 5.0 |

### `genre_counts.csv` (in `data/processed/`)
Number of movies per genre.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| genre | str | Genre name | Drama |
| count | int | Number of movies in this genre | 4361 |

