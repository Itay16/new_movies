import json
from abc import ABC

import requests
from _istorage import IStorage

API_KEY = '3863e126'
MOVIES_FILE = 'movie_storage.json'


class StorageJson(IStorage, ABC):
    def add_movie(self):
        """
        Adds a movie to the movie database.
        Loads the information from the JSON file, adds the movie,
        and saves it. The function doesn't need to validate the input.
        """
        new_movie_title = input("Enter the name of the new movie: ")
        ADDRESS = f"http://www.omdbapi.com/?apikey={API_KEY}"
        movie_response = requests.get(f"{ADDRESS}&t={new_movie_title}")
        new_data = movie_response.json()
        try:
            title = new_data['Title']
            year = new_data['Year']
            new_rating = float(new_data['imdbRating'])
            new_movie = {
                'title': title,
                'rating': new_rating,
                'year': year
            }
            with open(MOVIES_FILE, 'r') as file:
                movies = json.load(file)
            movies.append(new_movie)
            with open(MOVIES_FILE, 'w') as file:
                json.dump(movies, file)
            print(f"Added {title} ({year}) with rating {new_rating} to the database!")
        except KeyError:
            print("That movie doesn't exist!")
        except requests.exceptions.RequestException:
            print("Hmm... It doesn't look like you have internet!")

    def delete_movie(self):
        """
        Deletes a movie from the movie database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        title_to_delete = input("Enter the title of the movie you want to delete: ")
        with open(MOVIES_FILE, 'r') as file:
            movies = json.load(file)
        updated_movies = [movie for movie in movies if movie['title'] != title_to_delete]
        if len(updated_movies) == len(movies):
            print(f"{title_to_delete} was not found in the database.")
        else:
            with open(MOVIES_FILE, 'w') as file:
                json.dump(updated_movies, file)
            print(f"{title_to_delete} was removed from the database.")

    def update_movie(self):
        """
        Updates a movie from the movie database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        title_to_update = input("Enter the title of the movie you want to update: ")
        with open(MOVIES_FILE, 'r') as file:
            movies = json.load(file)
        for movie in movies:
            if movie['title'] == title_to_update:
                movie['title'] = input("Enter the new title: ")
                movie['year'] = input("Enter the new year: ")
                movie['rating'] = input("Enter the new rating: ")
                with open(MOVIES_FILE, 'w') as file:
                    json.dump(movies, file)
                print(f"{title_to_update} was updated.")
                return
        print(f"{title_to_update} was not found in the database.")
