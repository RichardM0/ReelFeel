import requests
import pandas as pd
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.themoviedb.org/3/movie/popular"

session = requests.Session()
session.params = {"api_key": API_KEY, "language": "en-US"}

def fetch_keywords(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords"
        r = session.get(url, timeout=10).json()
        return movie_id, [kw["name"] for kw in r.get("keywords", [])]
    except:
        return movie_id, []

def fetch_movies(pages):
    movies = []

    for page in range(1, pages + 1):
        r = session.get(BASE_URL, params={"page": page}).json()
        movies.extend(r["results"])

    keyword_map = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_keywords, m["id"]) for m in movies]
        for future in as_completed(futures):
            movie_id, keywords = future.result()
            keyword_map[movie_id] = keywords

    all_movies = []

    for movie in movies:
        all_movies.append({
            "id": movie["id"],
            "title": movie["title"],
            "overview": movie["overview"],
            "popularity": movie["popularity"],
            "poster": movie.get("poster_path"),
            "genre_ids": movie["genre_ids"],
            "vote_avg": movie["vote_average"],
            "keywords": keyword_map.get(movie["id"], [])
        })

    df = pd.DataFrame(all_movies)
    df.to_csv("data/movies.csv", index=False)
    print("Saved movies.csv")

if __name__ == "__main__":
    fetch_movies(pages=250)
