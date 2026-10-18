

The original Kaggle workflow is included in [notebook86c26b4f17.ipynb](./notebook86c26b4f17.ipynb). It expects TMDB 5000 movie and credits CSV files under `/kaggle/input/tmdb-movie-metadata/`; those source CSVs are not included here.

The generated `similarity.pkl` is about 176 MB, exceeds GitHub's standard 100 MB per-file limit, and is not required by the deployed app. The app rebuilds sparse vectors from `movie_list.pkl` at startup instead.
