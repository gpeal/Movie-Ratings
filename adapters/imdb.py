import requests
import json
from adapters import Adapter, FilmNotFoundError

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
    if isinstance(movies, dict) and movies['code'] == 404:
      raise FilmNotFoundError(title + ' not found on IMDb')
    import pdb; pdb.set_trace()

    # pick out the desired movie from the list of returned movies
    # NOTE: returned movies don't always have a title or a ranking
    movies = [movie for movie in movies if ('title' in movie.keys() and 'rating' in movie.keys()and movie['title'].replace('-', '').lower() == title.lower())]
    if movies:
      # make sure the movie has a rating (it may not like in the case of '21 And Over')
      return movies[0]['rating'] / 10.0
    else:
      raise FilmNotFoundError(title + ' not found on IMDb')

  def __repr__(self):
    return 'IMDb'
