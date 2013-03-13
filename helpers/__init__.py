

def safe_find_film(films, title):
	"""Finds the given film title in the films object"""
	
	# Setup check arrays
	titles = [f['title'] for f in films]
	lowercase_titles = [t.lower() for t in titles]
	# Check simple
	if title in titles:
		return films[titles.index(title)]
	# Check lower
	if title.lower() in lowercase_titles:
		return films[lowercase_titles.index(title.lower())]
	# film not found
	return None