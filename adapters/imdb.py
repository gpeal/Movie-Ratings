import requests
import json
from adapters import Adapter, FilmNotFoundError

class IMDbAdapter(Adapter):
  def get_similar_film_titles(self, title):
    r = requests.get('http://imdbapi.org/?q=%22' + title + '%22')
    movies = json.loads(r.text)
    if movies:
      return [movie['title'] for movie in movies[:5]]
    else:
        raise FilmNotFoundError(title + ' not found on IMDb')

  def get_film_score(self, title):
    r = requests.get('http://imdbapi.org/?q=%22' + title + '%22')
    movies = json.loads(r.text)
    if movies:
      return movies[0]['rating'] / 10.0
    else:
      raise FilmNotFoundError(title + ' not found on IMDb')

  def __repr__(self):
    return 'IMDb'