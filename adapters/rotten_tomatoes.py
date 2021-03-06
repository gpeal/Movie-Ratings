from rottentomatoes import RT

from . import Adapter, FilmNotFoundError
from helpers import safe_find_film

class RTAdapter(Adapter):
    """Rotten Tomatoes Adapter

    Implements the Rotten Tomatoes adapter.

    """
    def __init__(self):
        self.config = {
            'api_key': '8yvmeqtydvquk9bxv4mvemhm',
        }
        self.rt = RT(self.config['api_key'])


    def get_similar_film_titles(self, title):
        # Get films
        films = self.rt.search(title)[:5]
        # Check if results are empty
        if not films:
            raise FilmNotFoundError()
        # Extract titles
        return [film['title'] for film in films]

    def get_film(self, title):
        # Get films
        films = self.rt.search(title)
        # Find film in recieved list
        film_titles = [f.get('title', None) for f in films]
        found_title = safe_find_film(title, film_titles)
        # Raise error if not found
        if not found_title:
            raise FilmNotFoundError()
        film = films[film_titles.index(found_title)]
        return film

    def get_film_score(self, title):
        film = self.get_film(title)
        # Check if ratings exists
        if not 'ratings' in film:
            return None
        # Return film score
        normalized_score = film['ratings']['critics_score'] / 100.0
        return normalized_score


    def __repr__(self):
        return 'Rotten Tomatoes'