# src/utils/logger.py
# Configuration des logs pour le monitoring

import logging
import os
from datetime import datetime

# Créer le dossier logs s'il n'existe pas
os.makedirs("logs", exist_ok=True)


def setup_logger(name, log_file=None):
    """Configure et retourne un logger"""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler pour la console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler pour le fichier
    if log_file is None:
        log_file = f"logs/{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


# Logger principal pour l'application
app_logger = setup_logger("movie_recommendation")

# Logger pour les modèles ML
ml_logger = setup_logger("ml_models", "logs/ml_models.log")

# Logger pour l'ETL
etl_logger = setup_logger("etl_pipeline", "logs/etl_pipeline.log")