from metacritic_lib import Metacritic
from adapters import Adapter, FilmNotFoundError

class MetacriticAdapter(object):
  def get_similar_film_titles(self, title):
    meta = Metacritic()
    movies = meta.search(title, 'movie')
    if movies:
      return [movie.title for movie in movies][:5]
    else:
        raise LookupError(title + ' not found in metacritic')

  def get_film_score(self, title):
    meta = Metacritic()
    movies = meta.search(title, 'movie')
    movies = [movie for movie in movies if movie.title.lower() == title.lower()][0]
    if movies:
      return float(movies.metascore) / 100.0
    else:
      raise FilmNotFoundError(title + ' not found on IMDb')

  def __repr__(self):
    return 'Metacritic'

Adapter.register(MetacriticAdapter)