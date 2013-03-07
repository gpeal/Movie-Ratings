import requests
import json
import metacritic
import sys

# uses this api: http://imdbapi.org/
def get_movie_imdb(title):
    r = requests.get('http://imdbapi.org/?q=%22' + title + '%22')
    movie = json.loads(r.text)
    if movie:
        return movie[0]
    else:
        raise LookupError(title + ' not found in IMDb')

def get_movie_title_imdb(movie):
    return movie['title']

def get_movie_rating_imdb(movie):
    return movie['rating']

def get_movie_metacritic(title):
    meta = metacritic.Metacritic()
    movie = meta.search(title)
    if movie:
        return movie[0]
    else:
        raise LookupError(title + ' not found in metacritic')

def get_movie_title_metacritic(movie):
    return movie.title

def get_movie_rating_metacritic(movie):
    return movie.metascore


if __name__ == '__main__':
    titles = []
    while True:
        title = raw_input("Movie Title: ")
        if title:
            titles.append(title)
        else:
            break

    movies = {'imdb': {}, 'metacritic': {}}

    for title in titles:
        try:
            movies['imdb'][title] = get_movie_imdb(title)
        except LookupError, e:
            print "Error: " +  e.message
            exit()


        try:
            movies['metacritic'][title] = get_movie_metacritic(title)
        except LookupError, e:
            print  "Error: " + e.message
            exit()

    for title in titles:
        print get_movie_title_metacritic(movies['metacritic'][title]) + ' ' + str(get_movie_rating_metacritic(movies['metacritic'][title])) + '\tMetacritic'
        print get_movie_title_imdb(movies['imdb'][title]) + ' ' + str(get_movie_rating_imdb(movies['imdb'][title])) + '\tIMDb'

