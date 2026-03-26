# src/dashboard/app.py
# Point d'entrée principal du dashboard

import streamlit as st
from components import sidebar
from pages import (
    recommendations_page,
    stats_page,
    feedback_page,
    sentiment_page
)

# Configuration de la page
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Barre latérale
page = sidebar()

# Page principale
if page == "Recommandations":
    recommendations_page()
elif page == "Statistiques":
    stats_page()
elif page == "Feedback":
    feedback_page()
elif page == "Sentiment":
    sentiment_page()