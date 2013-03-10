from rottentomatoes import RT

from . import Adapter, FilmNotFoundError

class RTAdapter(Adapter):
    """Rotten Tomatoes Adapter

    Implements the Rotten Tomatoes adapter.

    """
    def __init__(self):
        self.config = {
            'api_key': '8yvmeqtydvquk9bxv4mvemhm',
        }
        self.rt = RT(self.config['api_key'])


    def get_similar_film_titles(self, film_title):
        # Get films
        films = self.rt.search(film_title)[:5]
        # Check if results are empty
        if not films:
            raise FilmNotFoundError()
        # Extract titles
        return [film['title'] for film in films]


    def get_film_score(self, film_title):
        # Get films
        films = self.rt.search(film_title)
        # Find film in recieved list
        titles = [f['title'] for f in films]
        if film_title in titles:
            film = films[titles.index(film_title)]
        # Raise error if not found
        else:
            raise FilmNotFoundError()
        # Return film score if found
        normalized_score = film['ratings']['critics_score'] / 100.0
        return normalized_score


    def __repr__(self):
        return 'Rotten Tomatoes'