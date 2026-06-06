# import require libraries
import streamlit as st
import pickle
import pandas as pd
import requests

# create a function to fetch poster using API through movie_id
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ecf2734685ae7d726c0e8012133d46cf&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path



# create a function ti extract movie name and their poasters image url
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6] # it used to extract only top 5 recommended movies

    recommend_movies = []
    movies_movies_poaster = []
    for i in movies_list:
        movies_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        # fatch poaster from api
        movies_movies_poaster.append(fetch_poster(movies_id))
    return recommend_movies,movies_movies_poaster

st.title('Movie Recommendation System')

movies_dict = pickle.load(open('Movies_dict.pkl','rb'))   # Use Movies_dict.pkl which is our dataset
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))      # Use similarity.pkl which is Vactarixation of Movies_dict dataset use to fatch similarity_score


select_movie_name = st.selectbox(
    'How Would you like to be connected?',
    movies['title'].values
)
selected_movie_id = movies[movies['title'] == select_movie_name].movie_id.values[0]

if st.button('Recommend'):
    # Selected movie
    st.subheader(select_movie_name)
    col_left, col_center, col_right = st.columns([1.2, 1, 1])
    selected_movie_poaster = fetch_poster(selected_movie_id)

    with col_center:
        st.image(
            selected_movie_poaster,
            width=150
        )

    st.markdown("---")

    recommended_movie_names, recommended_movie_posters = recommend(select_movie_name)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(
                recommended_movie_posters[i],
                use_container_width=True
            )

            st.caption(
                recommended_movie_names[i]
            )


    col_left, col_center, col_right = st.columns([1, 1, 1])
    selected_movie_poaster = fatch_poster(selected_movie_id)
    with col_center:

        st.image(
            selected_movie_poaster,
            width=350
        )
