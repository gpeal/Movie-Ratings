from adapters import FilmNotFoundError
from adapters.imdb import IMDbAdapter
from adapters.rotten_tomatoes import RTAdapter
from adapters.metacritic import MetacriticAdapter

import csv


class FilmProfile(object):
	"""Film Profile

	Contains information about how a paricular film performed.

	"""
	def __init__(self, film):
		self.film = film
		self.scores = []

	def add_score(self, backend, score):
		self.scores.append((backend, score))

	def get_score(self, backend):
		return [score[1] for score in self.scores if score[0] == backend][0]

	def to_dict(self):
		dictionary = dict(self.scores)
		dictionary['Title'] = self.film
		return dictionary

	def __repr__(self):
		score_table = '\n%s Results:\n' % self.film
		for score in self.scores:
			score_table += '%s: %s\n' % (score[0], score[1])
		return score_table

def create_profile(film_title, adapters, adapter_for_title=None, use_given_title=False):
	"""Create Profile

	Return a profile of all given backends for given film title.
	"""
	# Get correct title using given adapter if present
	if use_given_title:
		correct_title = film_title
	else:
		if adapter_for_title:
			correct_title =	get_correct_title(film_title, adapter_for_title)
		# Iterate through adapters to find correct title
		else:
			for adapter in adapters:
				try:
					correct_title =	get_correct_title(film_title, adapter)
					break
				except FilmNotFoundError:
					continue
			# Catch case where no adapter yields a correct title
			try:
				correct_title
			except NameError:
				raise Exception('Correct title could not be determined')
	# Create profile
	profile = FilmProfile(correct_title)
	for adapter in adapters:
		try:
			score = adapter.get_film_score(correct_title)
		except FilmNotFoundError:
			score = None
		profile.add_score(str(adapter), score)
	return profile


def prompt_user_for_title_choice(film_title, film_titles):
	"""Prompt User For Title Choice

	show user list of title matches, and get input choice.

	"""
	while True:
		print 'Title: %s' % (film_title)
		# Print choice prompt
		for i, title in enumerate(film_titles):
			print '%s: %s' % (i+1, title)
		print '0: Not listed'
		# Get user choice
		try:
			choice = int(raw_input('Enter choice: '))
		# Catch incompatible type
		except ValueError:
			print 'Invalid choice!'
			continue
		# Check for bounds
		if choice < 0 or choice > len(film_titles):
			print 'Invalid choice!'
			continue
		# Return valid choice
		if choice == 0:
			return None
		else:
			return film_titles[choice-1]


def get_correct_title(film_title, adapter):
	"""Get Correct Title

	Try to find the correct movie title using the given backend adapter.

	"""
	# Get titles from backend
	film_titles = adapter.get_similar_film_titles(film_title)
	# Check if there was an exact match
	if film_title in film_titles:
		return film_title
	else:
		chosen_title = prompt_user_for_title_choice(film_title, film_titles)
		if not chosen_title:
			raise FilmNotFoundError()
		return chosen_title

if __name__ == "__main__":
	imdb = IMDbAdapter()
	rotten_tomatoes = RTAdapter()
	metacritic = MetacriticAdapter()

	with open('movies.csv', 'rbU') as csv_input_file:
		with open('movies_output.csv', 'wb') as csv_output_file:
			csv_input = csv.reader(csv_input_file)
			csv_output = csv.DictWriter(csv_output_file, delimiter=',', fieldnames=['Title', 'IMDb', 'Metacritic', 'Rotten Tomatoes'])
			csv_output.writeheader()
			for row in csv_input:
				profile = create_profile(row[0], [metacritic, imdb, rotten_tomatoes])
				csv_output.writerow(profile.to_dict())
				print profile

