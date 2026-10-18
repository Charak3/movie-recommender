# Movie Recommender

A Streamlit web app that recommends five movies based on the selected movie's
overview, genres, keywords, cast, and director tags.

## Run locally

Requires Python 3.10 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The app needs `movie_list.pkl` beside `app.py`. It rebuilds the sparse
CountVectorizer matrix from the preprocessed tags when it starts, so the
176 MB `similarity.pkl` file is not needed.

## Movie title logos

The app can show official movie title logos from TMDB beside recommendations.
Create a TMDB account and obtain an API Read Access Token from
<https://www.themoviedb.org/settings/api>. Add it to Streamlit secrets:

```toml
TMDB_ACCESS_TOKEN = "your-read-access-token"
```

For Streamlit Community Cloud, open the app's **Manage app → Settings → Secrets**
and add the line there. For local development, save it in
`.streamlit/secrets.toml` beside `app.py`. Never commit the token to GitHub.
Without the token, the app still recommends movies but cannot display the logos.

## Deploy on Streamlit Community Cloud

1. Add `app.py`, `requirements.txt`, `README.md`, and `movie_list.pkl` to a
   GitHub repository.
2. Create an app from that repository in Streamlit Community Cloud and select
   `app.py` as the entry point.
3. Add `TMDB_ACCESS_TOKEN` in the app's **Manage app → Settings → Secrets** to
   enable movie logos.

The `movie_list.pkl` file is about 2.4 MB and can be committed directly. Do not
add `similarity.pkl`; the app does not use it.

This product uses the TMDB API but is not endorsed or certified by TMDB.
