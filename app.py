import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_option_menu import option_menu

# -------------------------
# TMDB API KEY (à modifier)
# -------------------------
API_KEY = "5f53b8fb1a981ad82b5dbf02c605e940"  # Mets ta clé TMDB ici

# Charger les données
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Page config
st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎥", layout="wide")

# Function pour récupérer les posters depuis TMDB
def get_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Image"

# Fonction recommandation
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    movie_recommendations = []
    movie_posters = []
    
    for i in distances[1:16]:  # Top 15 suggestions
        movie_id = movies.iloc[i[0]].movie_id
        movie_recommendations.append(movies.iloc[i[0]].title)
        movie_posters.append(get_poster(movie_id))
    return movie_recommendations, movie_posters

# ------------------- UI --------------------
with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["🏠 Accueil", "🎞️ Recommandations"],
        icons=["house", "film"],
        menu_icon="🎬",
        default_index=0
    )

# Custom CSS Modern UI
st.markdown("""
<style>
    .movie-card {
        background-color: #222;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        color: white;
        transition: transform 0.3s ease;
    }
    .movie-card:hover {
        transform: scale(1.05);
        background-color: #333;
    }
    .movie-title {
        font-weight: bold;
        margin-top: 8px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)


# Page d'accueil
if selected == "🏠 Accueil":
    st.title("🎬 Movie Recommender System")
    st.subheader("Trouvez le film parfait pour votre soirée ! 🍿")
    st.markdown("---")
    st.info("➡️ Cliquez sur **Recommandations** dans le menu pour commencer 🌟")

# Page recommandation
elif selected == "🎞️ Recommandations":
    st.title("🔍 Choisis un film pour commencer")

    selected_movie = st.selectbox("Sélectionner un film :", movies['title'].values)

    if st.button("🎯 Recommander"):
        names, posters = recommend(selected_movie)
        st.subheader("✨ Voici les films que tu vas sûrement adorer :")

        cols = st.columns(5)
        col_index = 0

        for i in range(len(names)):
            with cols[col_index]:
                st.markdown(
                    f"<div class='movie-card'>"
                    f"<img src='{posters[i]}' width='100%'>"
                    f"<div class='movie-title'>{names[i]}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            col_index += 1
            if col_index == 5:
                col_index = 0
                cols = st.columns(5)

