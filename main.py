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


def prompt_user():
  imdb = IMDbAdapter()
  rt = RTAdapter()
  metacritic = MetacriticAdapter()

  film = raw_input('Enter Movie: ')
  profile = profiler.create_profile(film, [metacritic, rt, imdb])

  similar_films = get_similar_films(profile.film)

  # prompt the user to enter a score for each movie
  profiles = []
  print 'Enter all score 0-100'
  print 'Enter s to skip movie'
  print 'Enter d when done'
  print ''
  for film in similar_films:
    score = raw_input('Enter score for ' + film + ': ')
    if score == 's':
      continue
    elif score == 'd':
      break

    # convert the score to a float
    while isinstance(score, str):
      try:
        # if they enter s or d to skip or stop, we need to temporarily convert it to a number
        # and check it afterwards
        if score == 's':
          score = -1
          break
        elif score == 'd':
          score = -2
          break
        score = float(score)
        if score < 0 or score > 100:
          raise ValueError()
      except ValueError:
        score = raw_input("Enter a valid score between 0 and 100: ")
    if score == -1:
      continue
    elif score == -2:
      break

    profile = profiler.FilmProfile(film)
    profile.add_score('User', score / 100)
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
  csv_file = csv.DictWriter(open('output.csv', 'wb'), delimiter=',', fieldnames=['Title', 'User', 'IMDb', 'Metacritic', 'Rotten Tomatoes'])
  csv_file.writeheader()
  for profile in profiles:
    csv_file.writerow(profile.to_dict())










if __name__ == "__main__":
  imdb = IMDbAdapter()
  rotten_tomatoes = RTAdapter()
  metacritic = MetacriticAdapter()

  prompt_user()