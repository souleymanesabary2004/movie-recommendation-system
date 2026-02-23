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

