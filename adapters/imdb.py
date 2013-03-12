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
    if 'code' in movies.keys() and movies['code'] == 404:
      raise FilmNotFoundError(title + ' not found on IMDb')
    movies = [movie for movie in movies if (movie['title'].replace('-', '').lower() == title.lower())]
    if movies:
      # make sure the movie has a rating (it may not like in the case of '21 And Over')
      if 'rating' in movies[0].keys():
        return movies[0]['rating'] / 10.0
      else:
        raise FilmNotFoundError(title + ' has no rating on IMDb')
    else:
      raise FilmNotFoundError(title + ' not found on IMDb')

  def __repr__(self):
    return 'IMDb'
