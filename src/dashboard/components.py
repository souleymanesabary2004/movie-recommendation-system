# src/dashboard/components.py
# Composants réutilisables pour le dashboard

import streamlit as st
import requests

def sidebar():
    """Sidebar with navigation and API status"""
    with st.sidebar:
        st.title("Movie Recommender")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["Recommandations", "Statistiques", "Feedback", "Sentiment"]
        )
        
        st.markdown("---")
        st.caption("API Status")
        
        # Vérifier si l'API est en ligne
        try:
            r = requests.get("http://api:8000/", timeout=2)
            if r.status_code == 200:
                st.success("API online")
            else:
                st.error("API error")
        except:
            st.error("API unreachable")
        
        st.caption("Made with Streamlit")
        
        return page

def format_movie(movie_data):
    """Format movie data for display"""
    return f"**{movie_data['title']}** (score: {movie_data['score']:.2f})"