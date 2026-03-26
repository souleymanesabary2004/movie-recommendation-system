# src/api/main.py
# Point d'entrée principal de l'API

from fastapi import FastAPI
from .endpoints import router

# Créer l'application FastAPI
app = FastAPI(
    title="Movie Recommendation API",
    description="API for movie recommendations using multiple ML models",
    version="1.0.0"
)

# Inclure les routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    """Actions à effectuer au démarrage de l'API"""
    from .dependencies import load_models
    print("Starting Movie Recommendation API...")
    load_models()
    print("API ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Actions à effectuer à l'arrêt de l'API"""
    print("Shutting down Movie Recommendation API...")