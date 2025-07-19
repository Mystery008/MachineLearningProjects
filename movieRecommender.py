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
movies = pd.read_csv("Moviedataset.csv")
import os
import gdown

SIMILARITY_FILE = "similarity.pkl"
FILE_ID = "1odItYnuxRlj9tWCmLgwC9EXHI7SN_f3N"  # You'll add this once the upload finishes
URL = f"https://drive.google.com/uc?id={FILE_ID}"

# Download if missing
if not os.path.exists(SIMILARITY_FILE):
    with st.spinner("Downloading similarity matrix... This may take a minute."):
        gdown.download(URL, SIMILARITY_FILE, quiet=False)

with open(SIMILARITY_FILE, "rb") as f:
    similarity = pickle.load(f)


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
