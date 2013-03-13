import requests
import json
from adapters import Adapter, FilmNotFoundError
from helpers import safe_find_film


class IMDbAdapter(Adapter):
  def get_similar_film_titles(self, title):
    r = requests.get('http://imdbapi.org/?q=%22' + title + '%22&limit=5')
    movies = json.loads(r.text)
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
    # Find film in recieved list
    movie = safe_find_film(movies, title)
    # Raise error if not found
    if not movie:
      raise FilmNotFoundError()
    # Return None if these is no rating
    if not 'rating' in movie:
      return None
    normalized_score = movie['rating'] / 10.0
    return normalized_score

  def __repr__(self):
    return 'IMDb'
