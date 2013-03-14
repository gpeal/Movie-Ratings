import requests
import json
from adapters import Adapter, FilmNotFoundError
from helpers import safe_find_film


class IMDbAdapter(Adapter):
  def get_similar_film_titles(self, title):
    r = requests.get('http://imdbapi.org/?q=%22' + title + '%22&limit=5')
    movies = json.loads(r.text)
    # Check if code is 404
    if isinstance(movies, dict) and movies['code'] == 404:
      raise FilmNotFoundError(title + ' not found on IMDb')
    if movies:
      return [movie['title'] for movie in movies[:5]]
    else:
        raise FilmNotFoundError(title + ' not found on IMDb')

  def get_film_score(self, title):
    title = title.replace('-', '')
    r = requests.get('http://imdbapi.org/?q=%22' + title + '%22&limit=100')
    movies = json.loads(r.text)
    # Check if code is 404
    if isinstance(movies, dict) and movies['code'] == 404:
      raise FilmNotFoundError(title + ' not found on IMDb')

    # Find movie
    movie_titles = [m['title'] for m in movies if 'title' in m]
    found_title = safe_find_film(title, movie_titles)
    # Raise error if not found
    if not found_title:
      raise FilmNotFoundError()
    movie = movies[movie_titles.index(found_title)]

    # Return None if these is no rating
    if not 'rating' in movie:
      return None
    normalized_score = movie['rating'] / 10.0
    return normalized_score

  def __repr__(self):
    return 'IMDb'
