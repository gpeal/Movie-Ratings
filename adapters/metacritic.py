from metacritic_lib import Metacritic
from adapters import Adapter, FilmNotFoundError

class MetaCriticAdapter(object):
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
    movie = [movie for movie in movies if movie.title == "Toy Story 2"][0]
    import pdb; pdb.set_trace()
    if movie:
      return movie.metascore / 100.0
    else:
      raise FilmNotFoundError(title + ' not found on IMDb')

  def __repr__(self):
    return 'IMDb'

Adapter.register(MetaCriticAdapter)