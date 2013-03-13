import abc

class Adapter(object):
	"""Adapter

	Interface to implement movie database backend adapters.

	"""
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def get_similar_film_titles(self, film_title):
		"""Get Film Title

		Return a list of the 5 closest matches of the given title.

		example output:

			[
				'The Matrix',
				'The Matrix Reloaded',
				'The Matrix Revolutions',
				'The Matrix Revisited',
				'Armitage - Dual Matrix'
			]


		"""
		raise NotImplementedError()

	@abc.abstractmethod
	def get_film_score(self, film_title):
		"""Get Score

		Return the score of a given film as a float between 0.0 and 1.0.

		example output:

			0.87
		
		"""
		raise NotImplementedError()

	@abc.abstractmethod
	def __repr__(self):
		raise NotImplementedError()


class FilmNotFoundError(Exception):
	"""Film Not Found Error

	Raise this error when a film is not found using the adaptors.

	"""
	pass

# Adjust namespace for easy imports
from .imdb import *
from .rotten_tomatoes import *
from .metacritic import *