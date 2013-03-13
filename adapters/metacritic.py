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
    movies = [movie for movie in movies if movie.title.lower() == title.lower()]
    if not movies:
      raise FilmNotFoundError(title + ' not found on IMDb')

    movie = safe_find_film(movies, title)

    if not movie:
      raise FilmNotFoundError(title + ' not found on IMDb')
    return float(movies[0].metascore) / 100.0

  def __repr__(self):
    return 'Metacritic'
