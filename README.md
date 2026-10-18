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

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository and add `app.py`, `requirements.txt`,
   `README.md`, and `movie_list.pkl`.
2. In Streamlit Community Cloud, create an app from that repository and select
   `app.py` as the entry point.
3. Deploy. No API keys or external services are required.

The `movie_list.pkl` file is about 2.4 MB and can be committed directly. Do not
add `similarity.pkl`; the app does not use it.
