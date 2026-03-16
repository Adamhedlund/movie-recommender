import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

movies = pd.read_csv("./data/movies.csv")
ratings = pd.read_csv("./data/ratings.csv")




movies["genres_clean"] = (
    movies["genres"]
    .str.replace("Sci-Fi", "Scifi", regex=False)
    .str.replace("Film-Noir", "FilmNoir", regex=False)
    .str.replace("(no genres listed)", "", regex=False)
    .str.replace("|", " ", regex=False)
)


tfidf = TfidfVectorizer()

tfidf_maxtrix = tfidf.fit_transform(movies['genres_clean'])

knn = NearestNeighbors(metric="cosine", algorithm="brute")
knn.fit(tfidf_maxtrix)


