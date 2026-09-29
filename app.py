import pickle
import streamlit as st
import requests

st.set_page_config(
    page_title="MovieVerse",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080808, #151515, #080808);
    color: white;
}

.block-container {
    padding-top: 40px;
    padding-left: 5%;
    padding-right: 5%;
}

.title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #ff4b4b;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #bbbbbb;
    font-size: 18px;
    margin-bottom: 40px;
}

.heading {
    font-size: 28px;
    font-weight: bold;
    color: white;
    margin-top: 30px;
    margin-bottom: 20px;
}

.stButton button {
    width: 100%;
    height: 50px;
    background: linear-gradient(90deg, #ff4b4b, #ff7b00);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
}

.stButton button:hover {
    background: linear-gradient(90deg, #ff7b00, #ff4b4b);
}

.movie-name {
    text-align: center;
    color: white;
    font-size: 16px;
    font-weight: bold;
    padding-top: 10px;
    min-height: 50px;
}

.footer {
    text-align: center;
    color: #777777;
    margin-top: 60px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)

    response = requests.get(url)
    data = response.json()

    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path

    return None


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    names = []
    posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id

        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


movies = pickle.load(
    open("model/movie_list.pkl", "rb")
)

similarity = pickle.load(
    open("model/similarity.pkl", "rb")
)


st.markdown(
    '<div class="title">🎬 MovieVerse</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle"> Recommendation System 🍿</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="heading">🔍 Select a Movie</div>',
    unsafe_allow_html=True
)

movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Choose your favorite movie",
    movie_list
)


if st.button("✨ Show Recommendations"):

    names, posters = recommend(selected_movie)

    st.markdown(
        '<div class="heading">🍿 Recommended Movies For You</div>',
        unsafe_allow_html=True
    )

    columns = st.columns(5)

    for column, name, poster in zip(columns, names, posters):

        with column:

            if poster:
                st.image(
                    poster,
                    use_container_width=True
                )
            else:
                st.write("Poster unavailable")

            st.markdown(
                '<div class="movie-name">' + name + '</div>',
                unsafe_allow_html=True
            )


st.markdown(
    '<div class="footer">'
    '🎬 MovieVerse | Built with Python, Streamlit & Machine Learning'
    '</div>',
    unsafe_allow_html=True
)