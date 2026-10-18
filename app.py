import pickle
from pathlib import Path

import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_PATH = Path(__file__).with_name("movie_list.pkl")


@st.cache_resource
def load_recommender():
    with DATA_PATH.open("rb") as data_file:
        movies = pickle.load(data_file)

    required_columns = {"movie_id", "title", "tags"}
    if not required_columns.issubset(movies.columns):
        raise ValueError(
            f"{DATA_PATH.name} must contain columns: "
            f"{', '.join(sorted(required_columns))}."
        )
    if movies.empty or movies["tags"].isna().any():
        raise ValueError(f"{DATA_PATH.name} must contain movies with non-empty tags.")

    vectorizer = CountVectorizer(max_features=5000, stop_words="english")
    vectors = vectorizer.fit_transform(movies["tags"])
    return movies, vectors


st.set_page_config(page_title="Movie Recommender", page_icon="🎬")
st.title("Movie Recommender")
st.write("Choose a movie to find five recommendations with similar themes and cast.")

movies, vectors = load_recommender()
selected_index = st.selectbox(
    "Choose a movie",
    options=range(len(movies)),
    format_func=lambda index: (
        f"{movies.iloc[index]['title']} ({movies.iloc[index]['movie_id']})"
    ),
)

if st.button("Recommend", type="primary"):
    scores = cosine_similarity(vectors[selected_index], vectors).ravel()
    ranked_indices = scores.argsort()[::-1]
    recommendations = [
        index for index in ranked_indices if index != selected_index
    ][:5]

    st.subheader(f"If you liked {movies.iloc[selected_index]['title']}")
    for index in recommendations:
        movie = movies.iloc[index]
        st.markdown(
            f"- **{movie['title']}** — similarity: {scores[index] * 100:.1f}%"
        )
