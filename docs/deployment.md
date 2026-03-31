\# Deployment Guide - Movie Recommendation System



\## Prerequisites



| Requirement        | Version | Description                          |

|--------------------|---------|--------------------------------------|

| Python             | 3.10+   | Programming language                 |

| Docker             | 24.0+   | Containerization                     |

| Git                | 2.40+   | Version control                      |

| RAM                | 8GB+    | Minimum for local deployment         |

| Disk Space         | 10GB+   | For data and models                  |



\---



\## Local Deployment



\### Step 1: Clone the Repository



```bash

git clone https://github.com/souleymanesabary2004/movie-recommendation-system.git

cd movie-recommendation-system



Step 2: Create Virtual Environment



python -m venv .venv

\# On Windows:

.venv\\Scripts\\activate

\# On Linux/Mac:

source .venv/bin/activate





Step 3: Install Dependencies



pip install -r requirements.txt



Step 4: Configure Environment Variables



cp .env.example .env

\# Edit .env with your MySQL credentials





Step 5: Start MySQL Database



docker run --name mysql-movies \\

&#x20; -e MYSQL\_ROOT\_PASSWORD=your\_password \\

&#x20; -v mysql\_data:/var/lib/mysql \\

&#x20; -p 2004:3306 \\

&#x20; -d mysql:8.0



Step 6: Run ETL Pipeline



python src/etl\_pipeline.py



Step 7: Train ML Models



python src/models/train\_als.py

python src/models/train\_knn.py

python src/models/train\_content.py

python src/models/train\_hybrid.py





Step 8: Start the API



uvicorn src.api.main:app --reload





API available at: http://localhost:8000

Documentation at: http://localhost:8000/docs





Step 9: Start the Dashboard



streamlit run src/dashboard/app.py



Dashboard available at: http://localhost:8501



Docker Deployment 



Using Docker Compose



\# Start all services

docker-compose up -d



\# Stop all services

docker-compose down



\# View logs

docker-compose logs -f



\# Rebuild after changes

docker-compose build



Services



Service	Port	URL

API	8000	http://localhost:8000

Dashboard	8501	http://localhost:8501

MySQL	2004	localhost:2004





Production Deployment (AWS/Azure - Planned)



User → Load Balancer → API (EC2/VM) → MySQL (RDS/Azure DB)

&#x20;                        ↓

&#x20;                   Dashboard (EC2/VM)





Configuration Checklist





Configuration Checklist

Item	Status

Environment variables	⏳ Planned

HTTPS/SSL	⏳ Planned

Domain name	⏳ Planned

Database backup	⏳ Planned

Monitoring (Prometheus)	⏳ Planned

Logging (ELK stack)	⏳ Planned

Troubleshooting

Common Issues

Issue	Solution

MySQL connection refused	Check if Docker container is running

Port already in use	Change port in .env and docker-compose.yml

Model file not found	Run training scripts first

Out of memory	Reduce batch size or use smaller dataset





Useful Commands



\# Check Docker containers

docker ps -a



\# View MySQL logs

docker logs mysql-movies



\# Check API health

curl http://localhost:8000/health



\# Run tests

pytest tests/ -v





Environment Variables (.env)



Variable	Description	Default

MYSQL\_ROOT\_PASSWORD	MySQL root password	(required)

MYSQL\_HOST	MySQL host	localhost

MYSQL\_PORT	MySQL port	2004

MYSQL\_DATABASE	MySQL database name	movie\_recommendation

API\_HOST	API host	0.0.0.0

API\_PORT	API port	8000

DASHBOARD\_PORT	Dashboard port	8501









\---



\## Verification Checklist



| Step                                    | Command                                   |

|-----------------------------------------|-------------------------------------------|

| MySQL running                           | `docker ps \\| grep mysql`                 |

| Database initialized                    | `mysql -h localhost -P 2004 -u root -p`   |

| Data loaded                             | `SELECT COUNT(\*) FROM movies;`            |

| API responding                          | `curl http://localhost:8000/health`       |

| Dashboard accessible                    | Open http://localhost:8501                |

| All tests passing                       | `pytest tests/ -v`                        |

