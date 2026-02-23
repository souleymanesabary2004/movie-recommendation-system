# **# Movie Recommendation System**



An End-to-End Big Data \& Machine Learning project using Docker, MySQL, and Python.



---



**## Architecture**



\- \*\*Language:\*\* Python 3.10

\- \*\*Database:\*\* MySQL 8.0 (Dockerized)

\- \*\*ETL (Level 1):\*\* Pandas \& SQLAlchemy

\- \*\*ETL (Level 2):\*\* Apache Spark (PySpark)

\- \*\*Infrastructure:\*\* Docker (Manual Management)



---



**##  Project Structure**



**movie-recommendation-system/**

**│**

**├── src/**

**│ ├── init.py**

**│ ├── init\_db.py**

**│ ├── etl\_pipeline.py**

**│ │**

**│ ├── ingestion/**

**│ │ ├── init.py**

**│ │ ├── ingest\_movies.py**

**│ │ └── ingest\_ratings.py**

**│ │**

**│ └── processing/**

**│ ├── init.py**

**│ └── clean\_movies.py**

**│**

**├── data/**

**│ ├── raw/**

**│ │ ├── movies.csv**

**│ │ ├── ratings.csv**

**│ │ ├── tags.csv**

**│ │ └── links.csv**

**│ │**

**│ └── processed/**

**│ └── movies\_clean.csv**

**│**

**├── notebooks/**

**│ ├── 01\_exploration\_pandas.ipynb**

**│ └── README.md**

**│**

**├── docs/**

**│ └── data\_dictionary.md**

**│**

**├── docker/**

**│**

**├── tests/**

**│ └── init.py**

**│**

**├── .env.example**

**├── .gitignore**

**├── requirements.txt**

**├── LICENSE**

**└── README.md**





**---**



**## ✅ Current Status (February 2026)**



**### Completed**

**- ✅ Docker container with MySQL**

**- ✅ Database schema (movies, ratings tables)**

**- ✅ Secure credentials with `.env`**

**- ✅ Data exploration in Jupyter**

**- ✅ ETL with Pandas (Level 1)**

**- ✅ Spark ingestion scripts (movies, ratings)**

**- ✅ Spark cleaning script (movies)**

**- ✅ Complete documentation**



**### In Progress**

**- ⏳ Spark cleaning script (ratings)**

**- ⏳ Transformation scripts**



**### Planned**

**- ⏳ Machine Learning models**

**- ⏳ FastAPI REST API**

**- ⏳ Streamlit dashboard**



**---**



**## 📊 Dataset: MovieLens**



**- \*\*Movies:\*\* 9,742**

**- \*\*Ratings:\*\* 100,836**

**- \*\*Users:\*\* 610**

**- \*\*Average rating:\*\* 3.53**

**- \*\*Most common genre:\*\* Drama**

**- \*\*Date range:\*\* 1996-2018**



**---**



**## ⚡ Quick Start**



**```bash**

**# Clone**

**git clone https://github.com/yourusername/movie-recommendation-system.git**

**cd movie-recommendation-system**



**# Setup**

**python -m venv .venv**

**.venv\\Scripts\\activate**

**pip install -r requirements.txt**



**# Start MySQL**

**docker run --name mysql-movies -e MYSQL\_ROOT\_PASSWORD=your\_password -v mysql\_data:/var/lib/mysql -p 2004:3306 -d mysql:8.0**



**# Initialize database**

**python src/init\_db.py**



**# Run ETL (Pandas)**

**python src/etl\_pipeline.py**



**# Try Spark**

**python src/ingestion/ingest\_movies.py**



**📚 Documentation**

**See docs/data\_dictionary.md for detailed data documentation.**



**📄 License**

**MIT License - see LICENSE file.**



**👤 Author**

**SOULEYMANE SOUMAHORO**

**GitHub: @souleymanesabary2004**

**LinkedIn:  www.linkedin.com/in/souleymane-soumahoro-b980b438b**

