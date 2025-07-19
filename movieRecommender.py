import streamlit as st
import pandas as pd
import pickle
import requests

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# -------------------- TITLE & DESCRIPTION --------------------
st.title("🎬 Movie Recommender System")
st.markdown("Find movies similar to your favorite ones using **content-based filtering**! 🍿")
st.divider()

# -------------------- DATA LOADING --------------------
movies = pd.read_csv("dataset.csv")
similarity = pickle.load(open("similarity.pkl", "rb"))

# -------------------- FUNCTION: Fetch Poster --------------------
def fetch_poster(title):
    api_key = "7b5cdd6e"  # Replace this with your real key
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url).json()

    poster_url = response.get("Poster", "")
    
    # Handle missing or invalid poster
    if not poster_url or poster_url == "N/A":
        return None

    return poster_url


# -------------------- MOVIE SELECTION --------------------
st.markdown("### 🎞️ Select a Movie")
selected_movie = st.selectbox("Choose a movie you like:", movies['title'].values)

# -------------------- RECOMMENDATION LOGIC --------------------
def recommend(title):
    index = movies[movies['title'] == title].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)
    recommendations = []
    posters = []
    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        recommendations.append(movie_title)
        posters.append(fetch_poster(movie_title))
    return recommendations, posters

# -------------------- DISPLAY RECOMMENDATIONS --------------------
if st.button("Recommend 🎯"):
    names, posters = recommend(selected_movie)

    st.markdown("### 📍 Top 5 Recommended Movies")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"**{names[i]}**", unsafe_allow_html=True)
