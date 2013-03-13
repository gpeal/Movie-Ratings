

def safe_find_film(film_title, film_titles):
	"""Returns index of film with title film_title, in film_titles."""
	# Setup check arrays
	# this supports films being passed in as either a dict or an object
	# if isinstance(films[0], dict):
	# 	titles = [f.get('title', None) for f in films]
	# else:
	# 	titles = [f.title for f in films]

	lowercase_titles = [t.lower() for t in film_titles]
	# Check simple
	if film_title in film_titles:
		return film_titles[film_titles.index(film_title)]
	# Check lower
	if film_title.lower() in lowercase_titles:
		return film_titles[lowercase_titles.index(film_title.lower())]
	# film not found
	return None