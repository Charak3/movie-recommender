import pickle
from pathlib import Path

import requests
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_PATH = Path(__file__).with_name("movie_list.pkl")
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


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


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_movie_logo(movie_id: int, access_token: str) -> tuple[str | None, str | None]:
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}/images",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"include_image_language": "en,null"},
            timeout=10,
        )
        response.raise_for_status()
    except requests.HTTPError as error:
        status_code = error.response.status_code if error.response else "unknown"
        return None, f"TMDB returned HTTP {status_code}."
    except requests.RequestException:
        return None, "Could not connect to TMDB."

    try:
        image_data = response.json()
    except requests.exceptions.JSONDecodeError:
        return None, "TMDB returned an invalid response."

    logos = image_data.get("logos") if isinstance(image_data, dict) else None
    if not isinstance(logos, list):
        return None, "TMDB returned invalid logo data."

    logos = sorted(
        (logo for logo in logos if isinstance(logo, dict)),
        key=lambda logo: 0 if logo.get("iso_639_1") == "en" else 1,
    )
    for logo in logos:
        file_path = logo.get("file_path")
        if isinstance(file_path, str) and file_path.startswith("/"):
            return f"{TMDB_IMAGE_BASE_URL}{file_path}", None

    return None, None


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
    try:
        tmdb_access_token = st.secrets["TMDB_ACCESS_TOKEN"]
    except (FileNotFoundError, KeyError):
        tmdb_access_token = None

    logo_errors = []
    if not tmdb_access_token:
        st.info(
            "To show official movie title logos, add a TMDB read access token "
            "as `TMDB_ACCESS_TOKEN` in Streamlit app secrets."
        )

    for index in recommendations:
        movie = movies.iloc[index]
        logo_url = None
        if tmdb_access_token:
            logo_url, logo_error = fetch_movie_logo(
                int(movie["movie_id"]), tmdb_access_token
            )
            if logo_error:
                logo_errors.append(f"{movie['title']}: {logo_error}")

        image_column, details_column = st.columns([1, 3])
        if logo_url:
            image_column.image(logo_url, width=220)
        details_column.markdown(
            f"**{movie['title']}**  \nSimilarity: {scores[index] * 100:.1f}%"
        )

    if logo_errors:
        st.warning(
            "Some movie logos could not be loaded: " + " ".join(logo_errors)
        )

st.caption(
    "This product uses the TMDB API but is not endorsed or certified by TMDB."
)
