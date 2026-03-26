# src/dashboard/pages.py
# Pages du dashboard

import streamlit as st
import requests
import pandas as pd

def recommendations_page():
    """Page with personalized recommendations"""
    st.header("Personalized Recommendations")
    
    user_id = st.number_input("User ID", min_value=1, value=1, step=1)
    
    if st.button("Get recommendations"):
        with st.spinner("Loading..."):
            try:
                # Appel API
                r = requests.get(f"http://api:8000/recommendations/{user_id}")
                
                if r.status_code == 200:
                    data = r.json()
                    st.success(f"10 recommendations for user {user_id}")
                    
                    # Afficher les résultats
                    for i, rec in enumerate(data['recommendations'], 1):
                        st.write(f"{i}. **{rec['title']}** (score: {rec['score']:.2f})")
                else:
                    st.error(f"Error {r.status_code}: {r.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

def stats_page():
    """Page with movie statistics"""
    st.header("Movie Statistics")
    
    movie_id = st.number_input("Movie ID", min_value=1, value=356, step=1)
    
    if st.button("View statistics"):
        with st.spinner("Loading..."):
            try:
                r = requests.get(f"http://api:8000/movies/{movie_id}/stats")
                
                if r.status_code == 200:
                    data = r.json()
                    
                    # Afficher les infos
                    st.subheader(f"{data['title']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Rating count", data['rating_count'])
                        st.metric("Average rating", f"{data['avg_rating']:.2f}")
                    with col2:
                        st.metric("Min rating", data['min_rating'])
                        st.metric("Max rating", data['max_rating'])
                    
                    st.metric("Standard deviation", f"{data['std_rating']:.2f}")
                else:
                    st.error(f"Error {r.status_code}: {r.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

def feedback_page():
    """Page to collect user feedback"""
    st.header("Give Feedback")
    
    with st.form("feedback_form"):
        user_id = st.number_input("User ID", min_value=1, value=1)
        movie_id = st.number_input("Movie ID", min_value=1, value=356)
        rating = st.slider("Rating (0-5)", 0.0, 5.0, 4.0, 0.5)
        liked = st.checkbox("I liked this movie")
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            with st.spinner("Sending..."):
                try:
                    payload = {
                        "user_id": user_id,
                        "movie_id": movie_id,
                        "rating": rating,
                        "liked": liked
                    }
                    r = requests.post("http://api:8000/feedback", json=payload)
                    
                    if r.status_code == 200:
                        st.success("Feedback sent successfully!")
                    else:
                        st.error(f"Error {r.status_code}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

def sentiment_page():
    """Page for sentiment analysis"""
    st.header("Sentiment Analysis")
    
    text = st.text_area("Enter text to analyze", 
                        "I love this movie, it's great!")
    
    if st.button("Analyze"):
        with st.spinner("Analyzing..."):
            try:
                r = requests.post("http://api:8000/sentiment", json={"text": text})
                
                if r.status_code == 200:
                    data = r.json()
                    
                    # Afficher le résultat
                    sentiment = data['sentiment']
                    confidence = data['confidence']
                    
                    if sentiment == "positive":
                        st.success(f"Positive sentiment (confidence: {confidence:.2f})")
                    elif sentiment == "negative":
                        st.error(f"Negative sentiment (confidence: {confidence:.2f})")
                    else:
                        st.info(f"Neutral sentiment (confidence: {confidence:.2f})")
                else:
                    st.error(f"Error {r.status_code}")
            except Exception as e:
                st.error(f"Connection error: {e}")