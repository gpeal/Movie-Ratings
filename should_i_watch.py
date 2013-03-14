from adapters import FilmNotFoundError
from adapters.imdb import IMDbAdapter
from adapters.rotten_tomatoes import RTAdapter
from adapters.metacritic import MetacriticAdapter
import csv
import profiler
import similar


# takes a list and returns the same list with duplicates removed
def unique(seq):
	seen = set()
	seen_add = seen.add
	return [ x for x in seq if x not in seen and not seen_add(x)]

def get_similar_films(title):
	similar_films = []
	# get the 5 most similar films
	similar_films.extend(similar.get_similar_film_titles(title))
	# get similar films for each of the similar films)
	# Save the second round of similar films into a new array. Otherwise, we will extend
	# the array we are iterating through and it will never end (and go in loops)
	new_similar_films = []
	for film in similar_films:
		new_similar_films.extend(similar.get_similar_film_titles(film))
	similar_films.extend(new_similar_films)
	#uniquify the list
	similar_films = unique(similar_films)
	# remove the original film if it is in the list
	try:
		similar_films.remove(title)
	except ValueError:
		pass
	return similar_films

def create_similar_film_profile(film, adapters):
	while True:
		score = raw_input('Please rate "%s" from 0 to 100 (s = skip movie, d = done): ' % film)
		try:
			# if they enter s or d to skip or stop, we need to temporarily convert it to a number
			# and check it afterwards
			if score == 's':
				return None
			elif score == 'd':
				return False
			score = int(score)
			if score < 0 or score > 100:
				raise ValueError()
			break
		except ValueError:
			continue
	# Create profile
	profile = profiler.FilmProfile(film)
	# Add user score
	profile.add_score('User', float(score) / 100.0)
	# Add score from backend adapters
	print 'Fetching scores from backends'
	for adapter in adapters:
		try:
			score = adapter.get_film_score(profile.film)
		except FilmNotFoundError:
			score = None
		profile.add_score(str(adapter), score)
	return profile

def create_similar_film_profiles(similar_films):
	profiles = []
	# Create adapters to use
	adapters = [
		RTAdapter(),
		IMDbAdapter(),
		MetacriticAdapter()
	]
	for film in similar_films:
		profile = create_similar_film_profile(film, adapters)
		# Handle skip and done
		if not profile:
			if profile == None:
				continue
			elif profile == False:
				break
		# Add profile
		print 'Saving scores'
		profiles.append(profile)
	return profiles

def write_profiles(profiles):
	if not profiles:
		print 'No data to write'
		return
	print 'Saving film profiles to "output.csv"'
	headers = ['Title']
	[headers.append(b) for b in profiles[0].backends]
	with open('output.csv', 'wb') as f:
		csv_file = csv.DictWriter(f, delimiter=',', fieldnames=headers)
		# write the results to a csv
		csv_file.writeheader()
		for profile in profiles:
			csv_file.writerow(profile.to_dict())


if __name__ == "__main__":
	# Get film title
	film_title = raw_input('Enter Movie: ')
	# Get similar films
	print 'Fetching list of similar films'
	similar_films = get_similar_films(film_title)
	print 'Found %s films' % len(similar_films)
	# Create profiles for each film
	profiles = create_similar_film_profiles(similar_films)
	write_profiles(profiles)
	print 'Done'