from adapters.imdb import IMDbAdapter
from adapters.rotten_tomatoes import RTAdapter
from adapters.metacritic import MetacriticAdapter
import profiler

import csv


def prompt_user():
  film = raw_input('Enter Movie: ')
  with open(film + '.csv', 'wb') as csv_output_file:
    csv_output = csv.DictWriter(csv_output_file, delimiter=',', fieldnames=['Title', 'IMDb', 'Metacritic', 'Rotten Tomatoes', 'User'])
    csv_output.writeheader()
    # create the profile for the film they entered
    profile = profiler.create_profile(film, [metacritic, imdb, rotten_tomatoes])

    # create a profile for 5 similar films to the one the user chose
    similar_film_titles = profile.get_similar_film_titles()
    similar_film_profiles = []
    for similar_film_title in similar_film_titles:
      new_similar_film_profile = profiler.create_profile(similar_film_title, [metacritic, imdb, rotten_tomatoes])
      similar_film_profiles.append(new_similar_film_profile)
      print new_similar_film_profile

    # for each similar film profile, get its similar films so we can get 30 total instead of 5
    for similar_film_profile in similar_film_profiles:
      new_similar_film_titles = similar_film_profile.get_similar_film_titles()
      # if the new similar title isn't in the list of similar titles, add it to the list and create its profile
      # keeping a list of titles helps ensure we don't create the same profile twice
      for new_similar_film_title in new_similar_film_titles:
        if not new_similar_film_title in similar_film_titles:
          similar_film_titles.append(new_similar_film_title)
          new_similar_film_profile = profiler.create_profile(new_similar_film_title, [metacritic, imdb, rotten_tomatoes])
          similar_film_profiles.append(new_similar_film_profile)
          print new_similar_film_profile

    # write all of the similar profiles to the csv file
    for similar_film_profile in similar_film_profiles:
      csv.writerow(similar_film_profile.to_dict())

    import pdb; pdb.set_trace()






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

