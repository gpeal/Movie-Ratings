import json
import requests
from adapters import RTAdapter



def get_similar_film_titles(film_title):
		# use Rotten Tomatoes similar api to get similar films
		# NOTE: this isn't in the library so we have to do it manually
		rt = RTAdapter()
		film = rt.get_film(film_title)
		similar_films_raw = requests.get('http://api.rottentomatoes.com/api/public/v1.0/movies/' + film['id'] + '/similar.json?apikey=8yvmeqtydvquk9bxv4mvemhm&limit=5').text
		similar_films = json.loads(similar_films_raw)['movies']
		return [similar_film['title'] for similar_film in similar_films]