import requests
import json
import metacritic

# uses this api: http://imdbapi.org/
def get_movies_imdb(title):
    r = requests.get('http://imdbapi.org/?q=%22' + title + '%22')
    movies = json.loads(r.text)
    if movies:
        return movies
    else:
        raise LookupError(title + ' not found in IMDb')

def get_movie_title_imdb(movie):
    return movie['title']

def get_movie_rating_imdb(movie):
    return movie['rating']

def get_movies_metacritic(title):
    meta = metacritic.Metacritic()
    movies = meta.search(title)
    if movies:
        return movies
    else:
        raise LookupError(title + ' not found in metacritic')

def get_movie_title_metacritic(movie):
    return movie.title

def get_movie_rating_metacritic(movie):
    return movie.metascore