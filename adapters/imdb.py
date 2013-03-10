import requests
import json
from adapters import Adapter, FilmNotFoundError

class Imdb(object):
  def get_similar_film_titles(self, title):
    r = requests.get('http://imdbapi.org/?q=%22' + title + '%22')
    movies = json.loads(r.text)
    if movies:
      return [movie['title'] for movie in movies[:5]]
    else:
        raise FilmNotFoundError(title + ' not found in IMDb')

Adapter.register(Imdb)