import json
import requests

API_KEY = '3863e126'
MOVIES_FILE = 'movie_storage.json'


class JsonStorage:
    def __init__(self, filename):
        self.filename = filename

    def _read_movies_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            return []
        else:
            return data

    def _write_movies_to_file(self, movies):
        with open(self.filename, 'w') as file:
            json.dump(movies, file)

    def list_movies(self):
        try:
            with open(self.filename, 'r') as file:
                movies = json.load(file)
                return movies
        except FileNotFoundError:
            return []

    def add_movie(self, movie):
        movies = self._read_movies_from_file()
        movies.append(movie)
        self._write_movies_to_file(movies)

    def delete_movie(self, title):
        movies = self._read_movies_from_file()
        filtered_movies = [movie for movie in movies if movie['title'] != title]
        if len(movies) == len(filtered_movies):
            print(f"\nMovie '{title}' not found in the database.")
        else:
            self._write_movies_to_file(filtered_movies)
            print(f"\n{title} has been deleted from the database.")

    def update_movie(self, title, new_rating):
        movies = self._read_movies_from_file()
        for movie in movies:
            if movie['title'] == title:
                movie['rating'] = new_rating
                self._write_movies_to_file(movies)
                print(f"\n{title} rating has been updated to {new_rating}.")
                break
        else:
            print(f"\nMovie '{title}' not found in the database.")
