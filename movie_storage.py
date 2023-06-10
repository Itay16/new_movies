import json
import requests
from _istorage import IStorage

API_KEY = '3863e126'
MOVIES_FILE = 'movie_storage.json'


class StorageJson(IStorage):
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
            for movie in new_data:
                title = new_data['Title']
                year = new_data['Year']
                new_rating = float(new_data['imdbRating'])
            new_movie = {
                'title': title,
                'rating': new_rating,
                'year': year
            }
            # Add the new movie to the list of movies
            MOVIES_FILE.append(new_movie)
            # Write the updated data back to the file
            with open(MOVIES_FILE, "w") as f:
                json.dump(MOVIES_FILE, f)
            print(f"Added {new_movie_title} ({year}) with rating {new_rating} to database!")
        except KeyError:
            print("That movie doesn't exist!")
        except ConnectionError:
            print("Hmm... It doesn't look like you have internet!")

    def delete_movie(self):
        """
        Deletes a movie from the movie database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        title_to_delete = input("Enter the title of the movie you want to delete: ")
        with open(MOVIES_FILE, 'r') as new_file:
            movies = json.load(new_file)
        for movie in movies:
            if movie['title'] == title_to_delete:
                movies.remove(movie)
                with open(MOVIES_FILE, 'w') as f:
                    json.dump(movies, f)
                print(f"{movie['title']} was removed from the database.")
                return
        print(f"{title_to_delete} was not found in the database.")

    def update_movie(self):
        """
        Updates a movie from the movie database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        title_to_update = input("Enter the title of the movie you want to update: ")
        for movie in MOVIES_FILE:
            if movie['title'] == title_to_update:
                movie['title'] = input("Enter the new title: ")
                movie['year'] = input("Enter the new year: ")
                movie['rating'] = input("Enter the new rating: ")
                print(f"{title_to_update} was updated.")
                return
        print(f"{title_to_update} was not found in the database.")
