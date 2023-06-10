from abc import ABC, abstractmethod
import json


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):  # Lists all movies
        with open('movie_storage.json', 'r') as newfile:
            movies = json.load(newfile)
        print(f"\n{len(movies)} movies in total:")
        for movie in movies:
            rating = movie['rating']
            title = movie['title']
            year = movie['year']
            print(f"{title} ({year}): {rating}")
        print('\n')

    @abstractmethod
    def add_movie(self, title, year, rating):  # Adds new movie to file
        pass

    @abstractmethod
    def delete_movie(self, title):  # Deletes existing movie
        pass

    @abstractmethod
    def update_movie(self, title, rating):  # Updates a movie's info
        pass
