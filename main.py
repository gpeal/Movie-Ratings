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


def prompt_user():
  imdb = IMDbAdapter()
  rt = RTAdapter()
  metacritic = MetacriticAdapter()

  similar_films = []
  film = raw_input('Enter Movie: ')
  profile = profiler.create_profile(film, [metacritic, rt, imdb])
  # get the 5 most similar films
  similar_films.extend(similar.get_similar_film_titles(profile.film))

  # get similar films for each of the similar films)
  # Save the second round of similar films into a new array. Otherwise, we will extend
  # the array we are iterating through and it will never end (and go in loops)
  new_similar_films = []
  for film in similar_films:
    new_similar_films.extend(similar.get_similar_film_titles(film))
  similar_films.extend(new_similar_films)
  #uniquify the list
  similar_films = unique(similar_films)

  # prompt the user to enter a score for each movie
  profiles = []
  print 'Enter all score 0-100'
  print 'Enter -1 to skip movie'
  print 'Enter -2 to stop collecting'
  for film in similar_films:
    score = float(raw_input('Enter score for ' + film + ': '))
    if score == -1:
      continue
    elif score == -2:
      break

    profile = profiler.FilmProfile(film)
    profile.add_score('user', score / 100)
    profiles.append(profile)

  # populate the scores from the other adapters
  for profile in profiles:
    for adapter in [metacritic, rt, imdb]:
      try:
        score = adapter.get_film_score(profile.film)
      except FilmNotFoundError:
        score = None
      profile.add_score(str(adapter), score)

  # write the results to a csv
  csv_file = csv.DictWriter(open('output.csv', 'wb'), delimiter=',', fieldnames=['Title', 'user', 'IMDb', 'Metacritic', 'Rotten Tomatoes'])
  csv_file.writeheader()
  for profile in profiles:
    csv_file.writerow(profile.to_dict())










if __name__ == "__main__":
  imdb = IMDbAdapter()
  rotten_tomatoes = RTAdapter()
  metacritic = MetacriticAdapter()

  prompt_user()

  # the following code reads a list of movies from movies.csv, creates a profile
  # for each one and exports the results to movies_output.csv
  # with open('movies.csv', 'rbU') as csv_input_file:
  #   with open('movies_output.csv', 'wb') as csv_output_file:
  #     csv_input = csv.reader(csv_input_file)
  #     csv_output = csv.DictWriter(csv_output_file, delimiter=',', fieldnames=['Title', 'IMDb', 'Metacritic', 'Rotten Tomatoes'])
  #     csv_output.writeheader()
  #     for row in csv_input:
  #       profile = profiler.create_profile(row[0], [metacritic, imdb, rotten_tomatoes])
  #       csv_output.writerow(profile.to_dict())
  #       print profile

