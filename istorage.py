from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):  # Lists all movies
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):  # Adds new movie to file
        pass

    @abstractmethod
    def delete_movie(self, title):  # Deletes existing movie
        pass

    @abstractmethod
    def update_movie(self, title, notes):  # Updates a movie's info
        pass
