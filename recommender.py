import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


def load_data():
    movies = pd.read_csv("./data/movies.csv")
    ratings = pd.read_csv("./data/ratings.csv")
    tags = pd.read_csv("./data/tags.csv")
    return movies, ratings, tags


def clean_genres(movies):
    movies["genres_clean"] = (
        movies["genres"]
        .str.replace("Sci-Fi", "Scifi", regex=False)
        .str.replace("Film-Noir", "FilmNoir", regex=False)
        .str.replace("(no genres listed)", "", regex=False)
        .str.replace("|", " ", regex=False)
    )
    return movies

def prepare_tags(tags):
    tags_grouped = (
        tags.groupby("movieId")["tag"]
        .apply(lambda x: " ".join(x.astype(str)))
        .reset_index()
    )
    return tags_grouped

def calculate_movie_stats(ratings):
    movie_stats = ratings.groupby("movieId")["rating"].agg(["mean", "count"]).reset_index()
    return movie_stats

def add_features(movies, tags_grouped):
    movies = movies.merge(tags_grouped, on="movieId", how="left")
    movies["tag"] = movies["tag"].fillna("")
    movies["tag_clean"] = movies["tag"].str.lower()
    movies["features"] = movies["genres_clean"] + " " + movies["tag_clean"]
    return movies

def add_weighted_rating(movies, movie_stats):
    movies = movies.merge(movie_stats, on="movieId", how="left")
    movies["mean"] = movies["mean"].fillna(0)
    movies["count"] = movies["count"].fillna(0)

    C = movies["mean"].mean()
    m = movies["count"].quantile(0.75)

    movies["weighted_rating"] = (
        (movies["count"] / (movies["count"] + m)) * movies["mean"] +
        (m / (movies["count"] + m)) * C
    )
    return movies


def content_model(movies):
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(movies['features'])

    knn = NearestNeighbors(metric="cosine", algorithm="brute")
    knn.fit(tfidf_matrix)

    movies = movies.reset_index(drop=True)
    indices = pd.Series(movies.index, index=movies["title"])
    return tfidf_matrix, knn, indices


def find_movie(title, movies):
    matches = movies[movies["title"].str.contains(title, case=False, na=False, regex=False)]
    if matches.empty:
        return None
    return matches.iloc[0]["title"]


def recommend(title, movies, tfidf_matrix, knn, indices, n=5):
    matched_title = find_movie(title, movies)
    
    if matched_title is None:
        return f"Movie '{title}' not found."

    idx = indices[matched_title]
    distances, neighbours = knn.kneighbors(tfidf_matrix[idx], n_neighbors=n + 1)
    
    neighbour_indices = neighbours.flatten()[1:]
    neighbour_distances = distances.flatten()[1:]

    results = movies.iloc[neighbour_indices][["title", "genres", "weighted_rating"]].copy()
    results["distances"] = neighbour_distances
    results["similarity"] = 1 - results["distances"]
    results["score"] = (
    0.7 * results["similarity"] +
    0.3 * results["weighted_rating"])

    results = results.sort_values("score", ascending=False).reset_index(drop=True)
    return matched_title, results

def build_recommender():
    movies, ratings, tags = load_data()

    movies = clean_genres(movies)
    tags_grouped = prepare_tags(tags)
    movie_stats = calculate_movie_stats(ratings)

    movies = add_features(movies, tags_grouped)
    movies = add_weighted_rating(movies, movie_stats)
    movies = movies.reset_index(drop=True)

    tfidf_matrix, knn, indices = content_model(movies)

    return movies, tfidf_matrix, knn, indices


