import streamlit as st
import pickle
import pandas as pd
import requests

# Your TMDB API Key
API_KEY = '57e49669632aa799a391eae8b4c5c288'  # Replace with your actual API key

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Fetch poster using TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url)
    if data.status_code == 200:
        poster_path = data.json().get('poster_path')
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters

# Streamlit UI setup
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommender System 🍿</h1>", unsafe_allow_html=True)

# Movie dropdown
selected_movie = st.selectbox("Search for a movie:", movies['title'].values)

# Recommend button
if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    st.markdown("### 🔥 Top 5 Movie Recommendations")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_column_width=True)
            st.markdown(f"**{names[i]}**", unsafe_allow_html=True)
