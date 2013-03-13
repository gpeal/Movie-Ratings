from metacritic_lib import Metacritic
from adapters import Adapter, FilmNotFoundError
from helpers import safe_find_film

class MetacriticAdapter(Adapter):
  def get_similar_film_titles(self, title):
    meta = Metacritic()
    movies = meta.search(title, 'movie')
    if movies:
      return [movie.title for movie in movies][:5]
    else:
        raise FilmNotFoundError(title + ' not found in metacritic')

  def get_film_score(self, title):
    meta = Metacritic()
    movies = meta.search(title, 'movie')
    # Find movie
    movie_titles = [m.title for m in movies]
    found_title = safe_find_film(title, movie_titles)
    # Raise error if not found
    if not found_title:
      raise FilmNotFoundError()
    movie = movies[movie_titles.index(found_title)]
    return float(movie.metascore) / 100.0

  def __repr__(self):
    return 'Metacritic'
