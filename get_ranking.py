from adapters.imdb import Imdb

if __name__ == "__main__":
  imdb = Imdb()
  imdb.get_similar_film_titles("Toy Story")