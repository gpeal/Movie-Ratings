from adapters.imdb import IMDbAdapter
from adapters.rotten_tomatoes import RTAdapter
from adapters.metacritic import MetacriticAdapter
import profiler

import csv

imdb = IMDbAdapter()
rotten_tomatoes = RTAdapter()
metacritic = MetacriticAdapter()

with open('movies.csv', 'rbU') as csv_input_file:
  with open('movies_output.csv', 'wb') as csv_output_file:
    csv_input = csv.reader(csv_input_file)
    csv_output = csv.DictWriter(csv_output_file, delimiter=',', fieldnames=['Title', 'IMDb', 'Metacritic', 'Rotten Tomatoes'])
    csv_output.writeheader()
    for row in csv_input:
      profile = profiler.create_profile(row[0], [metacritic, imdb, rotten_tomatoes])
      csv_output.writerow(profile.to_dict())
      print profile

