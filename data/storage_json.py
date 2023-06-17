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
            return data if data is not None else []

    def _write_movies_to_file(self, movies):
        with open(self.filename, 'w') as file:
            json.dump(movies, file)

    def list_movies(self):
        try:
            with open(self.filename, 'r') as file:
                movies = json.load(file)
        except FileNotFoundError:
            return []
        else:
            return movies

    def add_movie(self):
        """Add a movie to the database"""
        title = input("Enter the movie title: ")

        try:
            # Make a request to the movies API to fetch movie details
            response = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}")
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            movie_data = response.json()

            if movie_data.get('Response') == 'True':
                movie = {
                    'title': movie_data['Title'],
                    'year': movie_data['Year'],
                    'rating': movie_data['imdbRating'],
                }

                movies = self._read_movies_from_file()  # Read existing movies from file
                movies.append(movie)  # Add the new movie
                self._write_movies_to_file(movies)  # Write all movies back to file

                print(f"Movie '{movie['title']} ({movie['year']})' added successfully.")
            else:
                print("Movie not found.")
        except ConnectionError:
            print("Sorry, it seems like you're not connected to the internet!")

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
