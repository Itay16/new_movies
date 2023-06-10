import json
import requests

from istorage import IStorage

API_KEY = '3863e126'
MOVIES_FILE = 'movie_storage.json'


class StorageJson(IStorage):
    def __init__(self, file_path):  # Initializing new storage
        self.movies = None
        self.file_path = file_path

    def list_movies(self):  # Lists all movies
        """Lists all movies"""
        with open(self.file_path, 'r') as newfile:
            self.movies = json.load(newfile)
        print(f"\n{len(self.movies)} movies in total:")
        for movie in self.movies:
            rating = movie['rating']
            title = movie['title']
            year = movie['year']
            print(f"{title} ({year}): {rating}")
        print('\n')

    def add_movie(self, title, year, rating, poster):  # Adds new movie
        """Adds new movie to file"""
        # Create a new movie dictionary
        ADDRESS = f"http://www.omdbapi.com/?apikey={API_KEY}"
        movie_response = requests.get(f"{ADDRESS}&t={title}")
        new_data = movie_response.json()
        try:
            for info in new_data:
                title = new_data['Title']
                year = new_data['Year']
                new_rating = float(new_data['imdbRating'])
            new_movie = {
                'title': title,
                'rating': new_rating,
                'year': year
            }
            # Add the new movie to the list of movies
            self.movies.append(new_movie)
            # Write the updated data back to the file
            with open("movie_storage.json", "w") as f:
                json.dump(self.movies, f)
            print(f"Added {title} ({year}) with rating {new_rating} to database!")
        except KeyError:
            print("That movie doesn't exist!")
        except ConnectionError:
            print("Hmmm... It doesn't look like you have internet!")

    def delete_movie(self, title):  # Deletes movie from list
        """Deletes movie (if exists in database)"""
        title_to_delete = input("Enter the title of the movie you want to delete: ")
        for movie in self.movies:
            if movie['title'] == title_to_delete:
                self.movies.remove(movie)
                with open(self.file_path, 'w') as f:
                    json.dump(self.movies, f)
                print(f"{movie['title']} was removed from the database.")
                return
        print(f"{title_to_delete} was not found in the database.")

    def update_movie(self, title, notes):  # Updates a movie
        """Updates movie's info"""
        title_to_update = input("Enter the title of the movie you want to update: ")
        with open(self.file_path, 'r') as f:
            for movie in self.movies:
                if movie['title'] == title_to_update:
                    movie['title'] = input("Enter the new title: ")
                    movie['year'] = input("Enter the new year: ")
                    movie['rating'] = input("Enter the new rating: ")
                    print(f"{title_to_update} was updated.")
                    return
        print(f"{title_to_update} was not found in the database.")


storage = StorageJson('movies.json')
print(storage.list_movies())
storage.add_movie('Titanic', '1997', '7.8', 'titanic_poster.jpg')
